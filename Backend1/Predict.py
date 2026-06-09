from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
import os
import logging
import traceback
from flask import send_file
from io import BytesIO
import openpyxl


# =========================
# CONFIGURACIÓN FLASK
# =========================
server = Flask(__name__)
CORS(server)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# =========================
# RUTA DEL MODELO
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "decision_tree_model.joblib")

# =========================
# CARGA DEL MODELO
# =========================
model = None

try:
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        logging.info("✅ Modelo cargado correctamente")
    else:
        logging.error(f"❌ No se encontró el modelo en: {model_path}")
except Exception as e:
    logging.exception(f"❌ Error cargando el modelo: {e}")

# =========================
# FEATURES
# =========================

FEATURES = [
    "Total Sales",
    "Revenue",
    "Antigüedad de la Marca",
    "Número de Leads en Web",
    "Calificación Promedio de Productos",
    "Número de Devoluciones",
    "Crecimiento Total Sales"
]
# =========================
# HEALTH CHECK
# =========================
@server.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "API activa",
        "model_loaded": model is not None
    })

# =========================
# PREDICT ENDPOINT
# =========================
@server.route("/predict", methods=["POST"])
def predict():

    if model is None:
        return jsonify({"error": "Modelo no cargado"}), 500

    try:
        data = request.get_json(force=True)

        # Validación básica de datos
        missing = [f for f in FEATURES if f not in data]
        if missing:
            return jsonify({
                "error": "Faltan features",
                "missing": missing
            }), 400

        # DataFrame en orden correcto
        df = pd.DataFrame([[data[f] for f in FEATURES]], columns=FEATURES)

        # Predicción
        prediction = model.predict(df)[0]
        probs = model.predict_proba(df)[0]

        return jsonify({
            "resultado": (
                "Se sugiere que la marca se renueve"
                if int(prediction) == 1
                else "Se predice que la marca no renovara"
            ),
            "probabilidad_si": round(float(probs[1]) * 100, 2),
            "probabilidad_no": round(float(probs[0]) * 100, 2)
        })

    except Exception as e:
        logging.exception(f"Error en /predict: {e}")
        return jsonify({"error": str(e)}), 500
    
 # =========================
# PREDICT ENDPOINT BATCH
# =========================

@server.route("/predict_batch", methods=["POST"])
def predict_batch():

    if model is None:
        return jsonify({"error": "Modelo no cargado"}), 500

    try:
        if "file" not in request.files:
            return jsonify({"error": "No se recibió archivo"}), 400

        file = request.files["file"]

        df = pd.read_excel(file, engine="openpyxl")

        missing = [f for f in FEATURES if f not in df.columns]
        if missing:
            return jsonify({"error": "Faltan columnas", "missing": missing}), 400

        X_batch = df[FEATURES]

        predicciones = model.predict(X_batch)
        probabilidades = model.predict_proba(X_batch)

        df["Prediccion"] = ["Renueva" if p == 1 else "No Renueva" for p in predicciones]
        df["Probabilidad_SI"] = [round(p[1]*100, 2) for p in probabilidades]
        df["Probabilidad_NO"] = [round(p[0]*100, 2) for p in probabilidades]

        # 👇 en vez de Excel, regresamos JSON tipo Colab
        return jsonify({
            "columns": df.columns.tolist(),
            "data": df.head(50).values.tolist()  # limitamos para frontend
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# RUN SERVER
# =========================

if __name__ == "__main__":

    try:

        print("INICIANDO MODELO PREDICTIVO API...")

        server.run(
            host="0.0.0.0",
            port=8001,
            debug=True
        )

    except Exception as e:

        print("\nERROR AL INICIAR:\n")

        traceback.print_exc()