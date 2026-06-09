import os
import io
import asyncio
from datetime import datetime
from pypdf import PdfReader
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.adk.agents import Agent
from pinecone import Pinecone
import psycopg2
import pandas as pd

from google.api_core import retry

is_retriable = lambda e: (isinstance(e, genai.errors.APIError) and e.code in {429, 503})

genai.models.Models.generate_content = retry.Retry(
    predicate=is_retriable)(genai.models.Models.generate_content)

load_dotenv()

pinecone_api_key = os.getenv("PINECONE_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY2")
pinecone_index = os.getenv("PINECONE_INDEX", "litigios")

AGENT_MODEL = "gemini-2.5-flash"
#AGENT_MODEL = "ollama/gemma3"
#EMBEDDING_MODEL = "ollama/embeddinggemma"

llm_client = genai.Client(api_key=google_api_key)

pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index(pinecone_index)

def GeminiEmbeddingFunction(texts, embedding_task):
    response = llm_client.models.embed_content(
        model="gemini-embedding-2",
        #model=LiteLlm(EMBEDDING_MODEL),
        contents=texts,
        config=types.EmbedContentConfig(
            task_type=embedding_task,
            output_dimensionality=1024, # Sin comillas, es un entero
        ),
    )
    return [e.values for e in response.embeddings]

def pinecone_search(query: str) -> str:
    """
    Busca en la base de datos interna información relevante sobre una consulta.
    Retorna el texto encontrado para que el agente lo analice.
    """
    query_embedding = GeminiEmbeddingFunction([query], "RETRIEVAL_QUERY")[0]
    results = index.query(
    vector=query_embedding,
    top_k=15,
    include_metadata=True
)
    
    relevant_documents = [match['metadata']['page_content'] for match in results['matches']]
    
    # IMPORTANTE: Devolvemos un solo string con todo el contexto
    return "\n\n".join(relevant_documents)

def obtener_esquema_db() -> str:

    try:

        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )

        query = """
        SELECT
            table_name,
            column_name,
            data_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name;
        """

        df = pd.read_sql_query(query, conn)

        conn.close()

        return df.to_string(index=False)

    except Exception as e:
        return str(e)

#Consulta base de datos Postgres
def consultar_liverpool(sql_query: str) -> str:

    if not sql_query.strip().lower().startswith("select"):
        return "Solo se permiten consultas SELECT."

    try:

        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )

        df = pd.read_sql_query(sql_query, conn)

        conn.close()

        if df.empty:
            return "La consulta no devolvió resultados."

        return df.to_string(index=False)

    except Exception as e:
        return f"Error SQL: {str(e)}"
    
    
async def ingest_uploaded_file(tool_context, department: str = "Legal") -> str:
    """Retrieves the file, extracts original name, and indexes it into Pinecone."""
    
    # 1. Attempt to find original filename from message parts
    display_name = None
    found_part = None

    # Iterating through parts to find the file and its name
    for part in tool_context.user_content.parts:
        # Check if this part has file_data
        if hasattr(part, 'file_data') and part.file_data:
            found_part = part
            # Capture the original filename from the URI
            if part.file_data.file_uri:
                display_name = part.file_data.file_uri.split('/')[-1]
            break
        elif hasattr(part, 'inline_data') and part.inline_data:
            found_part = part
            break

    if not found_part:
        # Fallback to existing artifacts if no new file is in the current message
        artifact_names = await tool_context.list_artifacts()
        if not artifact_names:
            return "No files found to process. Please upload a document."
        display_name = artifact_names[-1]
    else:
        # Save the new file using its original name
        final_save_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}_{display_name or 'upload.pdf'}"
        await tool_context.save_artifact(final_save_name, found_part)
        display_name = final_save_name

    # 2. Load and extract PDF content
    artifact = await tool_context.load_artifact(display_name)
    raw_data = artifact.inline_data.data

    # PDF Text Extraction
    full_text = ""
    try:
        pdf_stream = io.BytesIO(raw_data)
        reader = PdfReader(pdf_stream)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
    except Exception as e:
        return f"Error parsing PDF: {str(e)}"

    # Chunking and Pinecone Upsert with Metadata
    chunk_size = 1000
    overlap = 200
    text_chunks = [full_text[i : i + chunk_size] for i in range(0, len(full_text), chunk_size - overlap)]

    for i in range(0, len(text_chunks), 32):
        batch = text_chunks[i : i + 32]
        embeddings = GeminiEmbeddingFunction(batch, "RETRIEVAL_DOCUMENT")

        vectors = []
        for j, (text, embed) in enumerate(zip(batch, embeddings)):
            vectors.append({
                "id": f"{display_name}-{i+j}",
                "values": embed,
                "metadata": {
                    "page_content": text,
                    "source": display_name, # Original filename is now here
                    "dept": department
                }
            })
        index.upsert(vectors=vectors)

    return f"Successfully indexed '{display_name}' into the database."


async def routing_callback(callback_context, **kwargs):
    """Detects uploads in the user message to route to the Librarian."""
    user_content = callback_context.user_content
    
    # Check for file parts in the current message
    has_file = any(part.inline_data or part.file_data for part in user_content.parts)

    if has_file:
        callback_context.next_agent = "Librarian"
    else:
        callback_context.next_agent = "Researcher"
    return


librarian_agent = Agent(
    name="Librarian",
    instruction="Index the user's uploaded file into Pinecone using the ingest tool.",
    tools=[ingest_uploaded_file]
)

researcher_agent = Agent(
    name="Researcher",
    instruction="""


You are an AI analyst specialized in litigation and business analytics.

You can:

- Analyze indexed legal PDFs using Pinecone.
- Query PostgreSQL Liverpool sales database.
- Generate SQL queries automatically.
- Compare legal and commercial information.
- Create tables and summaries.
- Answer in Spanish.
- Litigation analysis
- Liverpool sales analytics
- SQL business intelligence
- Google Trends analysis
- Brand performance analysis

IMPORTANT:
DATABASE SCHEMA:

fact_ventas:
- numero_lead
- descripcion
- indice_desempeno
- revenue
- avg_market_share
- devoluciones
- renovo
- calif_prome_prod
- fecha
- denominacion
- total_sales

fact_trends:
- indice_trend
- categoria
- fecha
- keyword

dim_marca:
- no_reg
- clase
- denominacion
- categoria
- titular
- descripcion
- id_marca
- tipo

dim_tiempo:
- dia
- mes
- anio
- fecha

TOOLS:

1. pinecone_search:
Searches legal PDFs.

2. obtener_esquema_db:
Gets PostgreSQL schema.

3. consultar_liverpool:
Executes SQL SELECT queries.

RULES:

- ALWAYS use consultar_liverpool for database questions.
- ALWAYS generate SQL automatically.
- ALWAYS answer in Spanish.
- Use tables when useful.
- Analyze KPIs and trends.
- Compare brands when requested.
- Use Pinecone only for litigation or PDF questions.
- Use markdown tables whenever comparing entities.
- Use bullets for insights.
- Use executive summaries.
- Keep answers clean and professional.
- Highlight important KPIs.
- Structure responses with titles and sections.
""",
   tools=[
    pinecone_search,
    obtener_esquema_db,
    consultar_liverpool
]
)


root_agent = Agent(
    name="Orchestrator",
    model=AGENT_MODEL,
    #model=LiteLlm(AGENT_MODEL),
    instruction="""
    You are the system coordinator. Analyze the user's input:
    1. If the user has UPLOADED a file, delegate to the 'Librarian' sub-agent.
    2. If the user is ASKING a question about internal data, delegate to the 'Researcher' sub-agent.
    3. If they do both, first call the Librarian, then the Researcher.
    """,
    sub_agents=[librarian_agent, researcher_agent],
    before_agent_callback=routing_callback
)


