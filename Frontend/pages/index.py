
import dash
from dash import html, dcc

dash.register_page(
    __name__,
    path="/"
)

layout = html.Div(
    children=[
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

        html.Main(
            className="flex flex-col flex-1 ml-64 min-h-screen",
            children=[
                html.Header(
                    className="top-0 z-40 sticky flex justify-between items-center bg-surface/80 dark:bg-surface/80 backdrop-blur-md px-8 w-full h-16 docked full-width",
                    children=[
                        html.Div(
                            className="flex items-center gap-8",
                            children=[
                                html.Span(
                                    className="font-headline font-bold text-[#E10098] text-2xl tracking-tighter",
                                    children=["LIVERPOOL"],
                                ),
                                html.Nav(
                                    className="flex gap-6",
                                    children=[

                                        dcc.Link("Inicio", href="/",
                                            className="text-[#E10098] font-bold"
                                        ),
                                        dcc.Link("Dashboards", href="/dashboard"),
                                        dcc.Link("Semáforo", href="/semaforo"),
                                        dcc.Link("Análisis Predictivo",href="/modelo")
                                    
                                    ]
                                )
                            ],
                        ),
                        html.Div(
                            className="border rounded-full border-outline-variant/20 w-8 h-8 overflow-hidden",
                            children=[
                                html.Img(
                                    alt="Executive User Profile",
                                    className="w-full h-full object-cover",
                                    **{
                                     "data-alt": "Professional corporate headshot of a Hispanic male executive in a smart casual attire, soft studio lighting, professional background"
                                    },
                                    src="https://lh3.googleusercontent.com/aida-public/AB6AXuCEIr3ftZSeGFF6m3zKpWlpSrRXxjYX8M4kZLZ4Djv5-Y5NwPk6I1HfXsHreNGyT5y8cG2gBTbQFB00XRy7WQq4YLlUSlVZl71NPE1QkVntFy51VPaO6raFuVTlrHrO37_sQ4a0U5lGwfmndYjzLQ2HKy2ECcuxaDKx_ppPLgxc-jB3iNes-0IuD4Nwer3VPfbjDTqY6m1ikRUWrSzo8bdK8ypScUci60q9IE_S2ljm_uVTpZMjpz4e-eeTm1dRBo3SyNPVTepNvRs"
                                )
                            ],
                        ),
                    ],
                ),
            
        
                html.Div(
                    className="flex-1 px-10 py-12",
                    children=[
                        html.Section(
                            className="mb-16 max-w-4xl",
                            children=[
                                html.H1(
                                    className="mb-4 font-manrope font-bold text-[3.5rem] text-on-surface leading-[1.1] tracking-tight",
                                    children=[
                                        "Decisiones inteligentes para la ",
                                        html.Span(
                                            className="text-[#E10098]",
                                            children=["renovación de marcas"],
                                        ),
                                    ],
                                ),
                                html.P(
                                    className="max-w-2xl font-body text-secondary text-xl leading-relaxed",
                                    children=[
                                        "Potenciamos la estrategia comercial de Liverpool con analítica avanzada de datos y modelos predictivos para optimizar el ciclo de vida de cada aliado estratégico."
                                    ],
                                ),
                            ],
                        ),
                        html.Div(
                            className="gap-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3",
                            children=[
                                html.Div(
                                    className="group flex flex-col bg-surface-container-lowest hover:bg-primary/5 p-8 rounded-xl h-full transition-all cursor-pointer",
                                    children=[
                                        html.Div(
                                            className="mb-6 rounded-lg aspect-video overflow-hidden",
                                            children=[
                                                html.Img(
                                                    alt="Dashboard",
                                                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500",
                                                    **{
                                                        "data-alt": "Modern data visualization dashboard on a tablet screen, glowing charts and clean interface in a professional office setting"
                                                    },
                                                    src="https://lh3.googleusercontent.com/aida-public/AB6AXuAjsjVx_sLotxe5KTODqI_MIZxX7jMft0BeQdyzmQ3yvZMmMIoY4wCefJnmYyHEN-T3_gGhgeCunK-9FSOb3POj4Z_iiGjubTiDBBb-yNktUbBVyobR68H-cbZtX9RtRkT7pvdVau_bV3UAIKHDa0DzNr4wXtSkkQmmOD7_GbTcbmg2zC4AUFuuXiABYZIBKUWIhFbMVoMUTd1KlopHdCZ5ah2oWX7PkMpVOlcE0kXaBBtfrgVyfX7bePFlXn0dQ4JZXtXKQzORsv8"
                                                )
                                            ],
                                        ),
                                        html.Div(
                                            className="flex items-center gap-2 mb-2 text-secondary",
                                            children=[
                                                html.Span(
                                                    className="font-semibold text-[0.75rem] uppercase tracking-widest",
                                                    children=["Visualización Global"],
                                                ),
                                            ],
                                        ),
                                        html.H3(
                                            className="mb-2 font-manrope font-bold text-on-surface text-xl",
                                            children=["Dashboard General"],
                                        ),
                                        html.P(
                                            className="mb-6 text-secondary text-sm leading-relaxed",
                                            children=[
                                                "Vista unificada de indicadores clave y rendimiento omnicanal del ecosistema Liverpool."
                                            ],
                                        ),
                                       dcc.Link(
                                            html.Button(
                                                "Explorar Datos",
                                                className="bg-[#E10098] text-white px-6 py-3 rounded-xl"
                                            ),
                                            href="/dashboard"
                                        ),
                                    ],
                                ), 
                                html.Div(
                                    className="group flex flex-col bg-surface-container-lowest hover:bg-primary/5 p-8 rounded-xl h-full transition-all cursor-pointer",
                                    children=[
                                        html.Div(
                                            className="mb-6 rounded-lg aspect-video overflow-hidden",
                                            children=[
                                                html.Img(
                                                    alt="Semáforo",
                                                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500",
                                                    **{
                                                        "data-alt": "Close up of a professional digital alert interface with soft blurred green, yellow and red glowing status indicators"
                                                    },
                                                    src="https://tse2.mm.bing.net/th/id/OIP.WDWqCl-Dqw9B5GklfY89EgHaGh?r=0&rs=1&pid=ImgDetMain&o=7&rm=3"
                                                )
                                            ],
                                        ),
                                        html.Div(
                                            className="flex items-center gap-2 mb-2 text-secondary",
                                            children=[
                                                html.Span(
                                                    className="font-semibold text-[0.75rem] uppercase tracking-widest",
                                                    children=["Alertas Tempranas"],
                                                ),
                                            ],
                                        ),
                                        html.H3(
                                            className="mb-2 font-manrope font-bold text-on-surface text-xl",
                                            children=["Semáforo de Riesgo"],
                                        ),
                                        html.P(
                                            className="mb-6 text-secondary text-sm leading-relaxed",
                                            children=[
                                                "Identificación proactiva de marcas con bajo desempeño o riesgo de desincorporación."
                                            ],
                                        ),
                                       dcc.Link(
                                            html.Button(
                                                "Monitorear marcas",
                                                className="bg-[#E10098] text-white px-6 py-3 rounded-xl"
                                            ),
                                            href="/semaforo"
                                        ),
                                    ],
                                ),
                                html.Div(
                                    className="group flex flex-col bg-surface-container-lowest hover:bg-primary/5 p-8 rounded-xl h-full transition-all cursor-pointer",
                                    children=[
                                        html.Div(
                                            className="mb-6 rounded-lg aspect-video overflow-hidden",
                                            children=[
                                                html.Img(
                                                    alt="Marcas Top",
                                                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500",
                                                    **{
                                                        "data-alt": "High-end luxury retail environment with soft focus, elegant store layout and premium branding atmosphere"
                                                    },
                                                    src="https://static.vecteezy.com/system/resources/previews/042/409/059/original/red-arrow-graph-drop-arrow-down-with-bar-graph-on-red-background-money-losing-stock-crisis-and-finance-concept-vector.jpg"
                                                )
                                            ],
                                        ),
                                        html.Div(
                                            className="flex items-center gap-2 mb-2 text-secondary",
                                            children=[
                                                html.Span(
                                                    className="font-semibold text-[0.75rem] uppercase tracking-widest",
                                                    children=["Líderes en Revenue"],
                                                ),
                                            ],
                                        ),
                                        html.H3(
                                            className="mb-2 font-manrope font-bold text-on-surface text-xl",
                                            children=["Marcas Top"],
                                        ),
                                        html.P(
                                            className="mb-6 text-secondary text-sm leading-relaxed",
                                            children=[
                                                "Ranking dinámico de socios comerciales con mayor impacto en el GMV y tráfico."
                                            ],
                                        ),
                                        dcc.Link(
                                            html.Button(
                                                "Ver Ranking",
                                                className="bg-[#E10098] text-white px-6 py-3 rounded-xl"
                                            ),
                                            href="/semaforo"
                                        ),
                                    ],
                                ),
                                html.Div(
                                    className="group flex flex-col bg-surface-container-lowest hover:bg-primary/5 p-8 rounded-xl h-full transition-all cursor-pointer",
                                    children=[
                                        html.Div(
                                            className="mb-6 rounded-lg aspect-video overflow-hidden",
                                            children=[
                                                html.Img(
                                                    alt="Análisis Predictivo",
                                                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500",
                                                    **{
                                                        "data-alt": "Abstract network of light connections and nodes, representing artificial intelligence and future projections in deep blue and pink"
                                                    },
                                                    src="https://th.bing.com/th/id/R.98ec377e7ae610b968e58fca03b52bed?rik=fcIPiX345lY1BQ&pid=ImgRaw&r=0"
                                                )
                                            ],
                                        ),
                                        html.Div(
                                            className="flex items-center gap-2 mb-2 text-secondary",
                                            children=[
                                                html.Span(
                                                    className="font-semibold text-[0.75rem] uppercase tracking-widest",
                                                    children=["Modelado IA"],
                                                ),
                                            ],
                                        ),
                                        html.H3(
                                            className="mb-2 font-manrope font-bold text-on-surface text-xl",
                                            children=["Análisis Predictivo"],
                                        ),
                                        html.P(
                                            className="mb-6 text-secondary text-sm leading-relaxed",
                                            children=[
                                                "Proyecciones de mercado y comportamiento de consumo para anticipar la demanda futura."
                                            ],
                                        ),
                                        dcc.Link(
                                            html.Button(
                                                "Generar Modelo",
                                                className="bg-[#E10098] text-white px-6 py-3 rounded-xl"
                                            ),
                                            href="/modelo"
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        html.Footer(
                            className="flex flex-wrap justify-between items-center gap-8 mt-20 pt-10 border-surface-container-high border-t",
                            children=[
                                html.Div(
                                    className="flex items-center gap-4",
                                    children=[
                                        html.Div(
                                            className="flex justify-center items-center bg-secondary-container/20 rounded-xl w-12 h-12",
                                            children=[
                                                html.Span(
                                                    className="text-[#E10098] material-symbols-outlined",
                                                    children=["verified"],
                                                )
                                            ],
                                        ),
                                        html.Div(
                                            children=[
                                                html.P(
                                                    className="font-bold text-[0.75rem] text-secondary uppercase tracking-wider",
                                                    children=["Última Actualización"],
                                                ),
                                                html.P(
                                                    className="font-semibold text-on-surface",
                                                    children=[
                                                        "Hoy, 09:42 AM — Central de Datos"
                                                    ],
                                                ),
                                            ]
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ]
)