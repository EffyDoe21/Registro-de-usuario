from flask import Flask, render_template, redirect, request, session
from flask_mysqldb import MySQL

app = Flask(__name__, template_folder='template')
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'login'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

# Función para verificar las credenciales del usuario y otros datos
def verificar_credenciales(correo, password):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuarios WHERE correo = %s AND password = %s', 
                (correo, password))
    account = cur.fetchone()
    cur.close()
    return account

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin():
    if 'logueado' in session and session['logueado']:
        return render_template('admin.html')
    else:
        return redirect('/')

@app.route('/acceso-login', methods=["POST"])
def login():
    if request.method == 'POST':
        correo = request.form.get('txtCorreo')
        password = request.form.get('txtPassword')


        # Verificar las credenciales del usuario y otros datos
        account = verificar_credenciales(correo, password)

        if account:
            # Si las credenciales son correctas, iniciar sesión y redirigir al panel de administración
            session['logueado'] = True
            session['id'] = account['id']
            return redirect('/admin')
        else:
            # Si las credenciales son incorrectas, volver a la página de inicio de sesión con un mensaje de error
            return render_template('index.html', mensaje="Credenciales incorrectas")


#Registro del usuario
@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/crear-registro', methods=["GET","POST"])
def crear_registro():
    if request.method == 'POST':
        correo = request.form.get('txtCorreo')
        password = request.form.get('txtPassword')
        city= request.form.get('txtCity')
        name = request.form.get('txtName')
        lastname = request.form.get('txtLastname')
        date = request.form.get('txtDate')
        
        cur= mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios (correo, password, name, lastname, date, city) VALUES (%s, %s, %s, %s, %s, %s)", (correo, password, name, lastname, date, city))
        mysql.connection.commit()
        
        return render_template("index.html", mensaje2="User successfully registered")
#------------------------------------------------

if __name__ == '__main__':
    app.secret_key = 'Estefania_BQ'
    app.run()
