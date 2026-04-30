from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Esta ruta carga la página principal del juego
@app.route('/')
def index():
    # Flask buscará automáticamente 'index.html' dentro de la carpeta /templates
    return render_template('index.html')

# Esta ruta opcional sirve para que el juego pueda guardar datos (dinero, misiones)
@app.route('/sync', methods=['POST'])
def sync():
    data = request.json
    # Aquí podrías guardar el progreso en una base de datos más adelante
    return jsonify({"status": "success", "received": data})

if __name__ == '__main__':
    # host='0.0.0.0' es fundamental para que puedas entrar desde tu celular
    # usando la dirección IP de tu computadora.
    app.run(debug=True, host='0.0.0.0', port=5000)
