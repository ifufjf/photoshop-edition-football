import subprocess
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Configuración de la clave secreta para la sesión (necesaria para la autenticación)
app.secret_key = 'una_clave_secreta_aqui'

# Página de login para proteger el acceso
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == 'tu_contraseña_segura':  # Asegúrate de cambiar la contraseña
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return 'Contraseña incorrecta, intenta de nuevo.', 401

    return render_template('login.html')

# Redirigir si no está autenticado
@app.before_request
def verificar_autenticacion():
    if 'logged_in' not in session and request.endpoint != 'login':
        return redirect(url_for('login'))

# Ruta principal para cargar la página
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para obtener todos los partidos de la página principal de Flashscore
@app.route('/obtener-partidos', methods=['GET'])
def obtener_partidos():
    url = "https://www.flashscore.com"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    partidos = []
    # Aquí haces scraping para extraer los partidos de Flashscore
    for partido in soup.find_all('div', class_='event__match'):
        nombre_partido = partido.find('span', class_='event__title').text.strip()
        partido_id = partido.get('data-eventid')
        
        partidos.append({'id': partido_id, 'nombre': nombre_partido})

    return jsonify({'partidos': partidos})

# Ruta para obtener datos de un partido específico
@app.route('/obtener-datos-flashscore', methods=['GET'])
def obtener_datos_flashscore():
    partido_id = request.args.get('partidoId')  # Obtiene el identificador del partido

    # Aquí haces scraping para obtener los datos de ese partido
    url = f"https://www.flashscore.com/match/{partido_id}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extraer algunos datos del partido
    competencia = soup.find('div', class_='competition-name').text.strip()
    resultado = soup.find('div', class_='scoreboard').text.strip()
    equipos = soup.find('div', class_='teams').text.strip()

    return jsonify({
        'competencia': competencia,
        'resultado': resultado,
        'equipos': equipos
    })

# Ruta para editar el PSD con los datos de Flashscore
@app.route('/editar-psd', methods=['POST'])
def editar_psd():
    data = request.json
    competencia = data.get('competencia')
    resultado = data.get('resultado')
    equipos = data.get('equipos')

    # Llamar al script de GIMP para manipular el PSD
    psd_path = "ruta/del/archivo.psd"
    texto_agua = f"{competencia} - {resultado} - {equipos}"
    imagen_fondo = "ruta/del/fondo.png"
    
    subprocess.run(['python3', 'gimp_script.py', psd_path, texto_agua, imagen_fondo])

    # Responder con la URL de la previsualización
    preview_url = "/static/psd-preview.png"
    return jsonify({"mensaje": "PSD editado exitosamente", "preview_url": preview_url})

if __name__ == '__main__':
    app.run(debug=True)
