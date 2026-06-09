import dash
from dash import html, dcc, Input, Output, State, callback
import requests

dash.register_page(
    __name__,
    path="/chat"
)

# =========================
# LAYOUT
# =========================

layout = html.Div(

    children=[

        # ================= SIDEBAR =================

        html.Aside(
            className="top-0 left-0 z-50 fixed flex flex-col bg-[#E10098] shadow-xl px-4 py-8 w-64 h-full",

            children=[

                html.Div(
                    className="mb-10 px-2",

                    children=[

                        html.Div(
                            className="flex items-center gap-3",

                            children=[

                                html.Div(
                                    className="flex justify-center items-center bg-white/20 rounded-full w-10 h-10",

                                    children=[
                                        html.Img(
                                            src="https://lh3.googleusercontent.com/aida-public/AB6AXuDQ4Q4r4_bH9zmIdQZfDdKYR00HNOo6NcNleQhLVJS1OQykgXwRbXZ1mFkfshzNGze5VllfAG_YpfzFMaTqG8ACGTC0162mr0_m1LYRIEWTKKhk9lN7kE_bl2tUpQuNGs-tstgC483mGoWNnQV-ybkla9fyN2ez9Sx1ZDbTPQ3zJ7RPqaMe3vgfniF1PS5H7f_xRwxV8ros8NIHO_oJG9XAY81_IZafems7S8-WQLSaxrENpqEvsPjc_l0HyRkfMH1EkMcClOJ5LjM",
                                            className="w-8 h-8 rounded-full"
                                        )
                                    ]
                                ),

                                html.Div([
                                    html.H1(
                                        "LIVERBOT",
                                        className="font-black text-white tracking-widest"
                                    ),

                                    html.P(
                                        "AI Assistant",
                                        className="text-white/70 text-xs"
                                    )
                                ])
                            ]
                        )
                    ]
                ),

                html.Nav(
                    className="flex-1 space-y-2",

                    children=[

                        dcc.Link(
                            "Inicio",
                            href="/",
                            className="block text-white py-2"
                        ),

                        dcc.Link(
                            "Dashboards",
                            href="/dashboard",
                            className="block text-white py-2"
                        ),

                        dcc.Link(
                            "Modelo Predictivo",
                            href="/modelo",
                            className="block text-white py-2"
                        ),

                        dcc.Link(
                            "Chat",
                            href="/chat",
                            className="block text-white py-2 font-bold"
                        ),
                    ]
                )
            ]
        ),

        # ================= MAIN =================

        html.Main(

            className="ml-64 min-h-screen bg-gray-100",

            children=[

                # HEADER

                html.Div(
                    className="bg-white shadow px-10 h-16 flex items-center",

                    children=[

                        html.H1(
                            "LIVERPOOL AI CHAT",
                            className="text-2xl font-bold text-[#E10098]"
                        )
                    ]
                ),

                # CONTENIDO

                html.Div(

                    className="p-10",

                    children=[

                        html.Div(

                            className="bg-white rounded-3xl shadow-xl p-8",

                            children=[

                                html.H2(
                                    "Chat Inteligente de Litigios",
                                    className="text-3xl font-bold mb-6"
                                ),

                                # CHAT BOX
                                dcc.Loading( 
                                    id="loading_chat",
                                    type="circle",
                                    color="#E10098",
                                    children=[
                                        
                                        dcc.Markdown(
                                            id="respuesta_chat",

                                            className="""
                                            bg-gray-50
                                            border
                                            rounded-2xl
                                            p-6
                                            h-[400px]
                                            overflow-y-auto
                                            whitespace-pre-wrap
                                            text-gray-1200
                                            """,
                                            style={
                                            "fontSize": "28px",
                                            "lineHeight": "1.6"
                                            },

                                            children="Hola, soy Liverbot IA. Pregúntame sobre litigios, marcas, ventas o sube tus archivos que requieras para una nueva investigación o prediccion."
                                        ),
                                

                                        # INPUT

                                        html.Div(

                                            className="flex gap-4 mt-6",

                                            children=[

                                                dcc.Input(
                                                    id="pregunta_input",
                                                    type="text",
                                                    placeholder="Escribe tu pregunta...",

                                                    className="""
                                                    flex-1
                                                    border
                                                    rounded-xl
                                                    p-4
                                                    text-lg
                                                    h-16
                                                    """
                                                ),

                                                 html.Button(
                                                    "Enviar",
                                                    id="btn_enviar",
                                                    n_clicks=0,

                                                    className="""
                                                    bg-[#E10098]
                                                    text-white
                                                    px-8
                                                    rounded-xl
                                                    font-bold
                                                    hover:opacity-90
                                                    """
                                                ),
                                            ],
                                        ), 
                                    ],
                                ),   
                            ]
                        )
                    ]
                )
            ]
        )
    ]
),
# =========================
# CALLBACK
# =========================

@callback(
    Output("respuesta_chat", "children"),
    Input("btn_enviar", "n_clicks"),
    State("pregunta_input", "value"),
    prevent_initial_call=True
)
def responder(n, pregunta):

    if not n:
        return "Hola, soy Liverbot IA. Pregúntame sobre litigios, marcas, ventas o sube tus archivos que requieras para una nueva investigación o prdiccion"

    if not isinstance(pregunta, str) or not pregunta.strip():
        return "Escribe una pregunta."

    try:
        
        response = requests.post(
            "http://127.0.0.1:5001/chat",
            json={"message": pregunta},
            timeout=30
        )
        data = response.json()

        print("JSON RECIBIDO:", data)

        if "error" in data:
            return f"ERROR BACKEND: {data['error']}"

        return data.get("response", "Sin respuesta del servidor")

    except requests.exceptions.Timeout:
        return "El servidor tardó demasiado en responder."

    except Exception as e:
        return f"ERROR DE CONEXIÓN: {str(e)}"
