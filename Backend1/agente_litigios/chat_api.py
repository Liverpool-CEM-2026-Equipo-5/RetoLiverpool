from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback
import asyncio
from asgiref.sync import async_to_sync
import uuid
# =========================
# AGENTE
# =========================

from agent import root_agent

# =========================
# GOOGLE ADK
# =========================

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# =========================
# FLASK
# =========================

server = Flask(__name__)
CORS(server)

# =========================
# ADK SESSION
# =========================

session_service = InMemorySessionService()

runner = Runner(
    agent=root_agent,
    app_name="liverpool_ai",
    session_service=session_service
)

USER_ID = "usuario_liverpool"
SESSION_ID = str(uuid.uuid4())

async def setup_session():

    await session_service.create_session(
        app_name="liverpool_ai",
        user_id=USER_ID,
        session_id=SESSION_ID
    )

    print("SESION CREADA:", SESSION_ID)

# EJECUTAR LA CREACIÓN DE LA SESIÓN
asyncio.run(setup_session())
# =========================
# CHAT ENDPOINT
# =========================

@server.route('/chat', methods=['POST'])
def chat():

    try:

        data = request.get_json(silent=True) or {}

        pregunta = data.get("message")

        async def run_agent():

            content = types.Content(
                role="user",
                parts=[
                    types.Part(text=pregunta)
                ]
            )

            respuesta_final = "El agente no generó ninguna respuesta."

            events = runner.run_async(
                user_id=USER_ID,
                session_id=SESSION_ID,
                new_message=content
            )

            respuesta_final = None

            async for event in events:
                if event.content and event.content.parts:
                    part = event.content.parts[0]
                    if hasattr(part, "text") and part.text:
                        respuesta_final = part.text

            return respuesta_final
        
        
        respuesta = async_to_sync(run_agent)()

        print("RESPUESTA GENERADA:", repr(respuesta))

        return jsonify({
         "response": respuesta
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })

# =========================
# RUN SERVER
# =========================

if __name__ == "__main__":

    try:

        print("INICIANDO CHAT API...")

        server.run(
            host="127.0.0.1",
            port=5001,
            debug=False
        )

    except Exception as e:

        print("\nERROR AL INICIAR:\n")

        traceback.print_exc()
