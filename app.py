from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib
import numpy as np
import os

app = Flask(__name__)
CORS(app) # Importar CORS para permitir solicitudes desde otros orígenes
modelo = joblib.load('modelo_carne.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/prediccion-carne', methods=['POST'])
def predecir_carne():
    try:
        data = request.get_json()
        campos = ['hamburguesas', 'tacos', 'bolillos', 'burritos', 'gringas', 'baguettes']
        if not all(c in data for c in campos):
            return jsonify({'error': 'Faltan campos'}), 400

        entrada = np.array([[data[c] for c in campos]])
        prediccion = modelo.predict(entrada)[0]
        return jsonify({'prediccion_carne_kg': round(prediccion, 2)})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
