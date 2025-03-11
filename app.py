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
    if os.path.exists(file_path):  # Verifica si el archivo existe
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data.append(json.load(f))
        except Exception as e:
            print(f"⚠️ Error al cargar {file}: {e}")
    else:
        print(f"⚠️ Archivo no encontrado: {file}")

@app.route('/get-order', methods=['POST'])
def get_order():
    req_data = request.get_json()
    if not req_data or "study_number" not in req_data:
        return jsonify({"error": "No se proporcionó un número de estudio"}), 400

    study_number = req_data["study_number"]

    # Buscar el JSON correspondiente
    for record in data:
        if record.get("study_number") == study_number:  
            return jsonify(record)

    return jsonify({"error": "Número de estudio no encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)
