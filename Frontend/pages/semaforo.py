
import dash
from dash import html, dcc

dash.register_page(
    __name__,
    path="/semaforo"
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
                    className="top-0 z-40 sticky flex justify-between items-center bg-surface/80 backdrop-blur-md px-8 w-full h-16",
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

                                        dcc.Link("Inicio", href="/"),
                                        dcc.Link("Dashboards", href="/dashboard"),
                                        dcc.Link("Semáforo", href="/semaforo",
                                            className="text-[#E10098] font-bold"
                                        ),
                                        dcc.Link("Análisis Predictivo",href="/modelo")
                                    
                                    ]
                                )
                            ],
                        ),
                    ],
                ),
                html.Div(
                    className="gap-9 grid grid-cols-1 lg:grid-cols-4",
                    children=[
                        html.Div(
                            className="relative lg:col-span-4 bg-surface-container-lowest p-2 rounded-2xl overflow-hidden",
                            children=[
                                html.Div(
                                    className="bg-white shadow-sm p-4 border-2 border-black/12 rounded-2xl",
                                    children=[
                                        html.Div(
                                            className="flex justify-center items-center",
                                            children=[
                                                html.Iframe(
                                                    src="https://public.tableau.com/views/Semaforodeliverpool/Semaforodevencimiento?:showVizHome=no&:embed=true&:display_count=n",
                                                    style={
                                                        "width": "100%",
                                                        "height": "1200px",
                                                        "border": "none",
                                                        "borderRadius": "20px"
                                                     }
                                                )
                                            ]
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    className="gap-9 grid grid-cols-1 lg:grid-cols-4",
                    children=[
                        html.Div(
                            className="relative lg:col-span-4 bg-surface-container-lowest p-3 rounded-x2 overflow-hidden",
                            children=[
                                html.Div(
                                    className="bg-white shadow-sm p 3 border-7 border-black/12 rounded-6x1",
                                    children=[
                                        html.Div(
                                            className="flex justify-center items-center",
                                            children=[
                                                html.Iframe(
                                                    src="https://public.tableau.com/views/Topmarcasporrevenue/TopRevenue2?:showVizHome=no&:embed=true&:display_count=n&:origin=viz_share_link",
                                                    style={
                                                        "width": "100%",
                                                        "height": "1200px",
                                                        "border": "none",
                                                        "borderRadius": "40px"
                                                    },
                                                )
                                             ],
                                        ),
                                    ]
                                ),
                            ]
                        ),
                    ]
                ),
            ]
        )
    ]
)

        
    
