from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Obtener la ruta absoluta del directorio actual
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Lista de archivos JSON
files = ["lab1.json", "lab2.json", "imagen1.json", "imagen2.json"]
data = []

# Cargar los archivos JSON
for file in files:
    file_path = os.path.join(BASE_DIR, file)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            json_data = json.load(f)
            if isinstance(json_data, list):  # Si el JSON es una lista, la extendemos
                data.extend(json_data)
            else:
                data.append(json_data)
    except FileNotFoundError:
        print(f"Advertencia: No se encontró {file}")

@app.route('/get_study', methods=['POST'])
def get_study():
    request_data = request.get_json()
    study_number = request_data.get("study_number")

    if not study_number:
        return jsonify({"error": "El parámetro study_number es obligatorio"}), 400

    for record in data:
        if isinstance(record, dict) and record.get("study_number") == study_number:
            return jsonify(record)

    return jsonify({"error": "No se encontró el estudio"}), 404

# Ejecutar la aplicación
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
