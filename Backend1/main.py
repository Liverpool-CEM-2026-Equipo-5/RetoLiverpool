import joblib
import json
import os
import pandas as pd

from dotenv import load_dotenv
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any

from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool

import google.genai as genai
from google.genai import types


# ==========================================
# MODELOS PYDANTIC
# ==========================================

class RenovationPredictionModel(BaseModel):
    ventas_totales: int
    ingresos: float
    antiguedad_marca: int
    numero_leads_web: int
    calificacion_promedio_productos: float
    numero_devoluciones: int
    participacion_mercado: float
    participacion_mercado_promedio: float


class GeminiChatModel(BaseModel):
    prompt: str


# ==========================================
# VARIABLES DE ENTORNO
# ==========================================

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

GOOGLE_GENAI_API_KEY = os.getenv("GOOGLE_GENAI_API_KEY")

conn_string = (
    f"host={DB_HOST} "
    f"port={DB_PORT} "
    f"dbname={DB_NAME} "
    f"user={DB_USER} "
    f"password={DB_PASSWORD}"
)


# ==========================================
# CONEXIÓN POSTGRESQL
# ==========================================

pool = AsyncConnectionPool(
    conninfo=conn_string,
    open=False
)


# ==========================================
# CLIENTE GEMINI
# ==========================================

client = genai.Client(
    api_key=GOOGLE_GENAI_API_KEY
)


# ==========================================
# FUNCIONES AUXILIARES
# ==========================================

async def get_schema_description() -> str:

    async with pool.connection() as conn:

        conn.row_factory = dict_row

        async with conn.cursor() as cur:

            await cur.execute("""
                SELECT table_name, column_name, data_type
                FROM information_schema.columns
                WHERE table_schema = 'public'
                ORDER BY table_name, ordinal_position
            """)

            rows = await cur.fetchall()

    tables: Dict[str, Any] = {}

    for row in rows:

        table_name = row["table_name"]

        col = f"{row['column_name']} ({row['data_type']})"

        tables.setdefault(table_name, []).append(col)

    lines = ["Esquema de la base de datos:"]

    for table, cols in tables.items():

        lines.append(f"- {table}:")

        for col in cols:

            lines.append(f"  - {col}")

    return "\n".join(lines)


def is_safe_query(query: str) -> bool:

    normalized = query.strip().lower()

    forbidden = (
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "truncate",
        "create",
        "grant",
        "revoke",
        "copy"
    )

    if not normalized.startswith("select"):
        return False

    return not any(word in normalized for word in forbidden)


async def query_database(query: str) -> str:

    if not is_safe_query(query):

        return "Error: Solo se permiten consultas SELECT."

    try:

        async with pool.connection() as conn:

            conn.row_factory = dict_row

            async with conn.cursor() as cur:

                await cur.execute(query)

                rows = await cur.fetchall()

                return json.dumps(rows, default=str)

    except Exception as e:

        return f"Error SQL: {str(e)}"


def predict_renovation_tool(
    ventas_totales: int,
    ingresos: float,
    antiguedad_marca: int,
    numero_leads_web: int,
    calificacion_promedio_productos: float,
    numero_devoluciones: int,
    participacion_mercado: float,
    participacion_mercado_promedio: float,
) -> str:

    input_data = pd.DataFrame([{
        "ventas_totales": ventas_totales,
        "ingresos": ingresos,
        "antiguedad_marca": antiguedad_marca,
        "numero_leads_web": numero_leads_web,
        "calificacion_promedio_productos": calificacion_promedio_productos,
        "numero_devoluciones": numero_devoluciones,
        "participacion_mercado": participacion_mercado,
        "participacion_mercado_promedio": participacion_mercado_promedio,
    }])

    prediction = app.state.model.predict(input_data)[0]

    return f"Predicción: {prediction}"


async def chat_with_gemini(
    prompt: str,
    schema_description: str
) -> str:

    MODEL = "gemini-2.5-flash"

    SYSTEM_PROMPT = """
    Eres un experto en bases de datos,
    machine learning y análisis de datos.
    """

    config = types.GenerateContentConfig(
        system_instruction=f"{SYSTEM_PROMPT}\n{schema_description}",
        tools=[
            query_database,
            predict_renovation_tool
        ],
    )

    response = await client.aio.models.generate_content(
        model=MODEL,
        config=config,
        contents=prompt,
    )

    return response.text


# ==========================================
# LIFESPAN
# ==========================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    await pool.open()

    app.state.schema_description = (
        await get_schema_description()
    )

    app.state.model = joblib.load(
        "modelo_renovacion.joblib"
    )

    print("PostgreSQL conectado")
    print("Modelo cargado")

    yield

    await pool.close()

    print("Pool cerrado")


# ==========================================
# APP FASTAPI
# ==========================================

app = FastAPI(
    lifespan=lifespan
)


# ==========================================
# ENDPOINTS GET
# ==========================================

@app.get("/")
def get_index():

    return {
        "mensaje": "Backend conectado a PostgreSQL"
    }


@app.get("/test_db")
async def test_db():

    async with pool.connection() as conn:

        async with conn.cursor() as cur:

            await cur.execute(
                "SELECT version();"
            )

            version = await cur.fetchone()

            return {
                "postgres_version": version
            }


@app.get("/dim_marca")
async def get_dim_marca():

    async with pool.connection() as conn:

        conn.row_factory = dict_row

        async with conn.cursor() as cur:

            await cur.execute("""
                SELECT *
                FROM dim_marca
                LIMIT 10
            """)

            rows = await cur.fetchall()

            return rows


@app.get("/fact_ventas")
async def get_fact_ventas():

    async with pool.connection() as conn:

        conn.row_factory = dict_row

        async with conn.cursor() as cur:

            await cur.execute("""
                SELECT *
                FROM fact_ventas
                LIMIT 10
            """)

            rows = await cur.fetchall()

            return rows


@app.get("/fact_trends")
async def get_fact_trends():

    async with pool.connection() as conn:

        conn.row_factory = dict_row

        async with conn.cursor() as cur:

            await cur.execute("""
                SELECT *
                FROM fact_trends
                LIMIT 10
            """)

            rows = await cur.fetchall()

            return rows
# ==========================================
# ENDPOINTS POST
# ==========================================

@app.post("/predict_brand_renovation")
async def predict_brand_renovation(
    data: RenovationPredictionModel
):

    pred_df = pd.DataFrame([
        data.model_dump()
    ])

    predicted_class = (
        app.state.model.predict(pred_df)[0]
    )

    probability = (
        app.state.model.predict_proba(pred_df)[0]
    )

    return {
        "renovacion": str(predicted_class),
        "probabilidad": probability.tolist()
    }


@app.post("/chat")
async def chat(
    prompt: GeminiChatModel
):

    response = await chat_with_gemini(
        prompt.prompt,
        app.state.schema_description
    )

    return {
        "response": response
    }


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        reload=True
    )