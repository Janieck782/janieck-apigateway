import os
import requests
from flask import Flask, redirect, render_template, request, send_from_directory, url_for, jsonify
from flask_cors import CORS  # Importa la extensión Flask-CORS

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas de la aplicación


@app.route('/')
def index():
    print('Request for index page received')
    return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/hello', methods=['POST'])
def hello():
    name = request.form.get('name')

    if name:
        print('Request for hello page received with name=%s' % name)
        return render_template('hello.html', name=name)
    else:
        print('Request for hello page received with no name or blank name -- redirecting')
        return redirect(url_for('index'))


# Configura la URL de la API de Buda
BUDA_API_URL = "https://www.buda.com/api/v2/markets/BTC-CLP/trades"


@app.route('/api', methods=['GET'])
def proxy():
    date = request.args.get('date')

    try:
        date_in_milliseconds = int(date) * 1000
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400

    # Construye la URL de la API de Buda con el timestamp
    params = {
        "timestamp": date_in_milliseconds*1000,
        "limit": 1
    }

    try:
        # Realiza una solicitud a la API de Buda usando requests
        response = requests.get(BUDA_API_URL, params=params)

        if response.status_code == 200:
            # Si la solicitud fue exitosa, devuelve la respuesta
            return jsonify(response.json())
        else:
            return jsonify({"error": f"API returned a non-successful status code: {response.status_code}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run()
