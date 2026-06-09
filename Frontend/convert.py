from html_to_dash import parse_html
from bs4 import BeautifulSoup
import os

# =====================================
# CONFIGURACIÓN
# =====================================

html_file_directory = "templates"
python_file_directory = "pages"

os.makedirs(python_file_directory, exist_ok=True)

# =====================================
# OBTENER HTML
# =====================================

files = [
    file for file in os.listdir(html_file_directory)
    if file.endswith('.html')
]

# =====================================
# CONVERTIR
# =====================================

for file in files:

    with open(
        f"{html_file_directory}/{file}",
        "r",
        encoding="utf8"
    ) as f:

        html_content = f.read()

        soup = BeautifulSoup(
            html_content,
            "html.parser"
        )

        body = soup.find("body")

        if body is None:
            body = soup

        # =====================================
        # CONVERTIR HTML -> DASH
        # =====================================

        parsed = parse_html(
            str(body),
            if_return=True,
            enable_dash_svg=True
        )

        # =====================================
        # NOMBRE DE PÁGINA
        # =====================================

        page_name = file.replace(".html", "")

        page_path = "/"

        if page_name.lower() != "index":
            page_path = f"/{page_name}"

        # =====================================
        # CREAR ARCHIVO DASH
        # =====================================

        final_code = f'''
import dash
from dash import html, dcc

dash.register_page(
    __name__,
    path="{page_path}"
)

layout = {parsed}
'''

        output_path = os.path.join(
            python_file_directory,
            file.replace(".html", ".py")
        )

        with open(
            output_path,
            "w",
            encoding="utf8"
        ) as output_file:

            output_file.write(final_code)

        print(f" Convertido: {file}")

print("\\n Conversión terminada")