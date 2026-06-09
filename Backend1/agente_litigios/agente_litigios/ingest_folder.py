from pathlib import Path
from datetime import datetime
from pypdf import PdfReader
import unicodedata
import re

# Importa funciones desde agent.py
from agent import GeminiEmbeddingFunction, index


def ingest_folder(folder_path="Litigios"):

    folder = Path(folder_path)
    pdf_files = list(folder.glob("*.pdf"))

    print(f"\nPDFs encontrados: {len(pdf_files)}")

    for pdf in pdf_files:

        print(f"\nLeyendo: {pdf.name}")

        full_text = ""

        # -------------------------
        # EXTRAER TEXTO DEL PDF
        # -------------------------

        try:
            reader = PdfReader(str(pdf))

            for page in reader.pages:

                text = page.extract_text()

                if text:
                    full_text += text + "\n"

        except Exception as e:

            print(f"Error leyendo {pdf.name}")
            print(e)
            continue


        if not full_text.strip():

            print(f"Sin texto extraído: {pdf.name}")
            continue


        # -------------------------
        # LIMPIAR NOMBRE DEL PDF
        # (para IDs válidos Pinecone)
        # -------------------------

        safe_name = unicodedata.normalize(
            "NFKD",
            pdf.stem
        )

        safe_name = (
            safe_name
            .encode("ascii", "ignore")
            .decode("ascii")
        )

        safe_name = re.sub(
            r"[^a-zA-Z0-9_-]",
            "_",
            safe_name
        )


        # -------------------------
        # DIVIDIR TEXTO EN CHUNKS
        # -------------------------

        chunk_size = 1000
        overlap = 200

        chunks = [

            full_text[i:i + chunk_size]

            for i in range(
                0,
                len(full_text),
                chunk_size - overlap
            )

        ]


        try:

            # -------------------------
            # GENERAR EMBEDDINGS
            # -------------------------

            for start in range(0, len(chunks), 32):

                batch = chunks[start:start+32]

                embeddings = GeminiEmbeddingFunction(
                    batch,
                    "RETRIEVAL_DOCUMENT"
                )

                vectors = []

                for j, (chunk, embedding) in enumerate(
                    zip(batch, embeddings)
                ):

                    vectors.append({

                        "id":
                        f"{safe_name}-{start+j}",

                        "values":
                        embedding,

                        "metadata": {

                            "page_content":
                            chunk,

                            "source":
                            pdf.name,

                            "folder":
                            folder_path,

                            "fecha_indexacion":
                            str(datetime.now()),

                            "tipo":
                            "litigio"

                        }

                    })


                # -------------------------
                # SUBIR A PINECONE
                # -------------------------

                index.upsert(
                    vectors=vectors
                )


            print(
                f"Indexado correctamente: {pdf.name}"
            )


        except Exception as e:

            print(
                f"Error indexando {pdf.name}"
            )

            print(e)

            continue


    print(
        "\n================================="
    )

    print(
        "TODOS LOS PDFs FUERON PROCESADOS"
    )

    print(
        "=================================\n"
    )


if __name__ == "__main__":

    ingest_folder()
    
    