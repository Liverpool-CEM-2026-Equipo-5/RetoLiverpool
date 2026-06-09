from datetime import date
import os
import dash
from dash import html, dcc, Input, Output, State, callback
import requests
import base64
import io
from dash import dash_table
import pandas as pd

dash.register_page(__name__, path="/modelo")




# =========================
# LAYOUT COMPLETO (IGUAL A SEMÁFORO)
# =========================
layout = html.Div([

    # ================= SIDEBAR =================
    html.Aside(
            className="top-0 left-0 z-50 fixed flex flex-col bg-gradient-to-b from-[#E10098] to-[#b00075] shadow-2xl border-r border-white/10 px-4 py-8 w-64 h-full",
            children=[
                html.Div(
                    className="mb-10 px-2 pt-2",
                    children=[
                        html.Div(
                            className="flex items-center gap-3 p-3 rounded-2xl bg-white/10 backdrop-blur-md border border-white/10",
                            children=[
                                html.Div(
                                    className="flex justify-center items-center bg-white/20 rounded-xl w-10 h-10 overflow-hidden",
                                    children=[
                                        html.Img(
                                            src="https://lh3.googleusercontent.com/aida-public/AB6AXuDQ4Q4r4_bH9zmIdQZfDdKYR00HNOo6NcNleQhLVJS1OQykgXwRbXZ1mFkfshzNGze5VllfAG_YpfzFMaTqG8ACGTC0162mr0_m1LYRIEWTKKhk9lN7kE_bl2tUpQuNGs-tstgC483mGoWNnQV-ybkla9fyN2ez9Sx1ZDbTPQ3zJ7RPqaMe3vgfniF1PS5H7f_xRwxV8ros8NIHO_oJG9XAY81_IZafems7S8-WQLSaxrENpqEvsPjc_l0HyRkfMH1EkMcClOJ5LjM",
                                            alt="Liverbot AI",
                                            **{"data-alt": "Cybernetic robot avatar"}
                                        )
                                    ],
                                ),
                                html.Div(
                                    children=[
                                        html.H1(
                                            "LIVERBOT",
                                            className="font-headline font-black text-[1.5rem] text-white tracking-widest"
                                        ),
                                        html.P(
                                            "AI Assistant",
                                            className="text-white/80 text-[0.7rem]"
                                        ),
                                    ]
                                ),
                            ],
                        )
                    ],
                ),

                html.Nav(
                    className="flex-1 space-y-1 overflow-y-auto no-scrollbar",
                    children=[
                        dcc.Link(
                            href="/chat",
                            className="flex items-center gap-3 px-4 py-3 rounded-xl bg-white text-[#E10098] font-semibold shadow-md hover:scale-[1.02] transition",
                            children=[
                                html.Span("Chat"),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    className="mt-auto pt-6 border-t border-white/10 text-white/70 text-xs px-2",
                    children="v1.0 • AI Assistant",
                ),
            ]
        ),
    

    # ================= MAIN =================
    html.Main(
        className="flex flex-col flex-1 ml-64 min-h-screen bg-gray-50",

        children=[

            # HEADER
            html.Header(
                className="top-0 z-40 sticky flex justify-between items-center bg-white shadow px-8 w-full h-16",
                children=[

                    html.Div(
                        className="flex items-center gap-8",
                        children=[

                            html.Span(
                                "LIVERPOOL",
                                className="font-bold text-[#E10098] text-2xl"
                            ),

                            html.Nav(
                                className="flex gap-6",
                                children=[

                                    dcc.Link("Inicio", href="/"),
                                    dcc.Link("Dashboards", href="/dashboard"),
                                    dcc.Link("Semáforo", href="/semaforo"),
                                    dcc.Link(
                                        "Análisis Predictivo",
                                        href="/modelo",
                                        className="text-[#E10098] font-bold"
                                    ),
                                ]
                            )
                        ]
                    )
                ]
            ),

            # ================= CONTENIDO =================
            html.Div(
                className="p-10",

                children=[

                    html.H2(
                        "Modelo Predictivo de Renovación de Marcas",
                        className="text-3xl font-bold mb-6"
                    ),

                    html.Div(
                        className="grid grid-cols-2 gap-4",

                        children=[

                            dcc.Input(id="Total_Sales", type="number",
                                      placeholder="Total Sales",
                                      className= """
                                        flex-1
                                        border
                                        rounded-xl
                                        p-4
                                        text-lg
                                        h-16"""),

                            dcc.Input(id="Revenue", type="number",
                                      placeholder="Revenue",
                                      className= """
                                        flex-1
                                        border
                                        rounded-xl
                                        p-4
                                        text-lg
                                        h-16"""),

                            dcc.Input(id="Antiguedad_Marca", type="number",
                                      placeholder="Antiguedad de la Marca",
                                      className= """
                                        flex-1
                                        border
                                        rounded-xl
                                        p-4
                                        text-lg
                                        h-16"""),

                            dcc.Input(id="Numero_Leads_Web", type="number",
                                      placeholder="Numero de Leads",
                                      className= """
                                        flex-1
                                        border
                                        rounded-xl
                                        p-4
                                        text-lg
                                        h-16"""),

                            dcc.Input(id="Calificacion_Promedio_Productos", type="number",
                                      placeholder="Calificación Promedio de Producto",
                                      className= """
                                        flex-1
                                        border
                                        rounded-xl
                                        p-4
                                        text-lg
                                        h-16"""),

                            dcc.Input(id="Numero_Devoluciones", type="number",
                                      placeholder="Número de Devoluciones",
                                      className= """
                                        flex-1
                                        border
                                        rounded-xl
                                        p-4
                                        text-lg
                                        h-16"""),
                            dcc.Input(id="Crecimiento_Total_Sales", type="number",
                                      placeholder="Crecimiento Total Sales",
                                      className= """
                                        flex-1
                                        border
                                        rounded-xl
                                        p-4
                                        text-lg
                                        h-16"""),
                        ]
                    ),

                    html.Button(
                        "Generar Predicción",
                        id="btnPrediccion",
                        n_clicks=0,
                        className="bg-[#E10098] text-white px-6 py-3 rounded mt-6"
                    ),

                    html.Div(
                        className="mt-10",
                        children=[

                            html.H3("Resultado", className="text-xl font-bold"),

                            html.Div(id="resultado",
                                     className="text-3xl font-bold text-[#E10098] mt-4"),

                            html.Div(id="probabilidades",
                                     className="mt-4 space-y-3"),
                        ]
                    ),
                    
                    
                    # ===== INICIO NUEVO BLOQUE BATCH =====
                    
                    html.Hr(className="my-10"),

                    html.H2(
                        "Predicción Batch por Excel",
                        className="text-2xl font-bold mb-4"
                    ),

                    dcc.Upload(
                        id="upload-batch",
                        children=html.Div([
                            "📄 Arrastra un archivo Excel o haz clic aquí"
                        ]),
                        className="""
                            border-2
                            border-dashed
                            border-[#E10098]
                            rounded-xl
                            p-8
                            bg-white
                            text-center
                            cursor-pointer
                        """
                    ),

                    html.Button(
                        "Procesar Batch",
                        id="btnBatch",
                        n_clicks=0,
                        className="bg-[#E10098] text-white px-6 py-3 rounded mt-6"
                    ),

                    html.Div(
                    id="resultado_batch",
                    className="mt-4"
                    ),

                    dcc.Download(id="download-batch"),

                     # ===== FIN NUEVO BLOQUE BATCH =====
                ]
            )
        ]
    )
])

# =========================
# CALLBACK
# =========================
@callback(
    Output("resultado", "children"),
    Output("probabilidades", "children"),
    Input("btnPrediccion", "n_clicks"),

    State("Total_Sales", "value"),
    State("Revenue", "value"),
    State("Antiguedad_Marca", "value"),
    State("Numero_Leads_Web", "value"),
    State("Calificacion_Promedio_Productos", "value"),
    State("Numero_Devoluciones", "value"),
    State("Crecimiento_Total_Sales", "value"),
)
def predecir(
    n,
    total_sales,
    revenue,
    antiguedad,
    leads,
    calificacion,
    devoluciones,
    crecimiento_sales
):
    if not n:
        return "", ""

    payload = {
    "Total Sales": total_sales or 0,
    "Revenue": revenue or 0,
    "Antigüedad de la Marca": antiguedad or 0,
    "Número de Leads en Web": leads or 0,
    "Calificación Promedio de Productos": calificacion or 0,
    "Número de Devoluciones": devoluciones or 0,
    "Crecimiento Total Sales": crecimiento_sales or 0
    }

    try:

        resp = requests.post(
            "http://127.0.0.1:8001/predict",
            json=payload,
            timeout=15
        )

        data = resp.json()

        print("STATUS:", resp.status_code)
        print("RESPUESTA:", data)

    except Exception as e:

        return (
            "ERROR CONEXIÓN",
            html.Div(str(e), className="text-red-600")
        )

    return (
        data.get("resultado", "Sin resultado"),

        html.Div([

            html.Div(
                f"SI renueva: {data.get('probabilidad_si', 0)}%",
                className="bg-green-100 text-green-700 p-4 rounded font-bold"
            ),

            html.Div(
                f"NO renueva: {data.get('probabilidad_no', 0)}%",
                className="bg-red-100 text-red-700 p-4 rounded font-bold"
            )

        ])
    )
# ====================================
# NUEVO CALLBACK BATCH
# ====================================
@callback(
    Output("resultado_batch", "children"),
    Input("btnBatch", "n_clicks"),
    State("upload-batch", "contents"),
    State("upload-batch", "filename"),
    prevent_initial_call=True
)
def procesar_batch(n, contents, filename):

    if not contents:
        return html.Div("Sube un archivo primero", className="text-red-600")

    try:
       
        _, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)

        files = {
            "file": (
                filename,
                io.BytesIO(decoded),
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        }

        response = requests.post(
            "http://127.0.0.1:8001/predict_batch",
            files=files,
            timeout=120
        )

        data = response.json()

        if response.status_code != 200:
            return html.Div(f"Error backend: {data}", className="text-red-600")

        df = pd.DataFrame(data["data"], columns=data["columns"])

        counts = df["Prediccion"].value_counts()
        si = counts.get("Renueva", 0)
        no = counts.get("No Renueva", 0)

        # 🔥 GRÁFICA
        import plotly.express as px

        fig = px.bar(
            x=["Renueva", "No Renueva"],
            y=[si, no],
            labels={"x": "Resultado", "y": "Cantidad"},
            title="Distribución de renovación de marcas",
            color_discrete_sequence=["#E10098"]
        )

        return html.Div([

            # 📊 TABLA
            dash_table.DataTable(
                columns=[{"name": c, "id": c} for c in data["columns"]],
                data=[dict(zip(data["columns"], row)) for row in data["data"]],
                page_size=len(data["data"]),  # 👈 aquí el cambio
                style_table={"overflowX": "auto"},
                style_cell={"textAlign": "left", "padding": "10px"},
                style_header={"fontWeight": "bold", "backgroundColor": "#f3f3f3"},
            ),

            html.Hr(),

            # 📈 RESUMEN
            html.Div([
                html.H4("Resumen de resultados"),
                html.P(f"Renueva: {si}", className="text-green-600 font-bold"),
                html.P(f"No Renueva: {no}", className="text-red-600 font-bold"),
            ]),

            # 📊 GRÁFICA
           dcc.Graph(figure=fig)
        ])
        
    except Exception as e:
        return html.Div(f"Error: {str(e)}", className="text-red-600")
    
