from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
from werkzeug.utils import secure_filename

# Configuración de Flask y Flask-Login
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_clave_secreta'  # Cambia esto por una clave secreta segura
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'psd', 'jpg', 'jpeg', 'png'}
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Clase de Usuario para Flask-Login
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Cargar usuario
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == 'mi_contraseña':  # Cambia la contraseña por una segura
            user = User('1')
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')

# Página principal donde el usuario elige archivo PSD y el partido
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        # Procesamiento de los archivos subidos
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Aquí puedes agregar la lógica para manipular el archivo PSD con GIMP o similar
        # También deberías procesar los datos de Flashscore según el partido seleccionado
        
        return redirect(url_for('preview'))
    
    return render_template('index.html')

# Previsualización del archivo PSD modificado
@app.route('/preview')
@login_required
def preview():
    # Lógica para mostrar la previsualización del archivo PSD
    # Asumiendo que has guardado el archivo de alguna forma
    return render_template('preview.html')

# Desconectar sesión de usuario
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Verifica si el archivo tiene una extensión permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

if __name__ == '__main__':
    app.run(debug=True)
