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


@app.route('/api', methods=['GET'])
def proxy():
    date = request.args.get('date')
    try:
        date_in_milliseconds = int(date) * 1000
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400

    url = f"https://www.buda.com/api/v2/markets/BTC-CLP/trades?timestamp={date_in_milliseconds}&limit=1"
    response = requests.get(url)

    if response.status_code == 200:
        try:
            json_data = response.json()
            return jsonify(json_data)
        except ValueError:
            return jsonify({"error": "Invalid JSON response from the API"}), 500
    else:
        return jsonify({"error": f"API returned a non-successful status code: {response.status_code}"}), 500


if __name__ == '__main__':
    app.run()
