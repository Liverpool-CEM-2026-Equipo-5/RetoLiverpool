from dash import Dash, html, page_container

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    external_scripts=[
        "https://cdn.tailwindcss.com"
    ]
)

app.layout = html.Div([
    page_container
])

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8050,
        debug=False,
        use_reloader=False
    )