from flask import Flask, render_template, flash, redirect, request, redirect, session, url_for
import os, db, http.client, json, requests, time, threading

app = Flask(__name__)
app.secret_key = 'pro1'

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'app', 'templates')

app.template_folder = template_dir
app.static_folder = 'static'

# Define la variable de la URL base del servicio de AUTH y Registro
service = "http://service:5000"
#localhost, service para contenedor

# Rutas de la aplicación
# Ruta principal que requiere inicio de sesión
@app.route('/home')
def home():
    if 'username' in session:
        users = db.get_all_users()
        return render_template('index.html', users=users)
    else:
        return redirect(url_for('login'))

@app.route('/logout', methods=['POST'])
def logout():
    # Eliminar las variables de sesión
    session.clear()

    # Redirigir a la página principal (def home():)
    return redirect(url_for('home'))

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Obtener los datos del formulario de inicio de sesión
        username = request.form['username']
        password = request.form['password']

        # Verificar la autenticación del usuario
        authenticated = False
        user_role = None
        user_id = 0
        user_email = ""

        with open('users.json') as f:
            users = db.get_all_users()

            for user in users:
                if user['username'] == username and user['password'] == password:
                    authenticated = True
                    user_role = user['role']
                    user_id = user['id']
                    user_email = user['email']
                    break

        if authenticated:
            # Autenticación exitosa, redirigir según el rol del usuario
            session['state'] = 0
            session['auth'] = 0
            if user_role == 'admin':
                session['username'] = username
                session['role'] = user_role
                session['id'] = user_id
                session['email'] = user_email
                return redirect(url_for('admin'))
            elif user_role == 'manager':
                session['username'] = username
                session['role'] = user_role
                session['id'] = user_id
                session['email'] = user_email
                return redirect(url_for('manager'))

        # Autenticación fallida, mostrar un mensaje de error
        error_message = 'Nombre de usuario o contraseña incorrectos'
        return render_template('login.html', error_message=error_message)

    # Si el método de solicitud es GET, mostrar el formulario de inicio de sesión
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    # Obtener los datos del formulario de registro
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    # Verificar si el nombre de usuario o el correo electrónico ya existen en la base de datos
    if check_existing_user(username, email) == True:
        # Si el nombre de usuario o el correo electrónico ya existen, mostrar un mensaje de error
        print("User Exist.")
        session['reg'] = "El nombre de usuario o el correo electrónico ya están en uso. Por favor, elija otros."
        flash('El nombre de usuario o el correo electrónico ya están en uso. Por favor, elija otros.', 'error')
        return redirect(url_for('login'))
    else:
        print("New User.")
        # Crear un diccionario con los datos del nuevo usuario
        user_data = {
            'username': username,
            'email': email,
            'password': password
        }

        # Insertar el nuevo usuario en la base de datos
        db.insert_user(user_data)
        
        # Redirigir a la página de inicio de sesión o mostrar un mensaje de éxito
        flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')

        data = {'email': email}
        url = service + "/register"
        response = requests.post(url, json=data)
        if response.status_code == 200:
            session['reg'] = response.json()['message']
            print("", session['reg'])
        else:
            print("Failed to register.")

        # Redirigir a la página de inicio de sesión o mostrar un mensaje de éxito
        return redirect(url_for('login'))

def check_existing_user(username, email):
    users = db.get_all_users()

    for user in users:
        if user['username'] == username or user['email'] == email:
            return True

    return False

@app.route('/admin')
def admin():
    # Verificar si el usuario tiene una sesión iniciada y si es el rol correcto
    if session['role'] == 'admin':
        users = db.get_all_users()
        return render_template('admin.html', users=users)
    else:
        return redirect(url_for('login'))

@app.route('/manager')
def manager():
    # Verificar si el usuario tiene una sesión iniciada y si es el rol correcto
    if session.get('role') == 'manager':
        if session['state'] == 0:
            data = {'state': session['state'], 'email': session.get('email')}
            url = service + "/auth"
            response = requests.post(url, json=data)
            if response.status_code == 200:
                session['state'] = response.json()['state']
                print("Obtained state:", session['state'])
            else:
                print("Failed to obtain token.")

            schedule_reset_token()
            return redirect(url_for('auth'))
        if session['state'] != 0 and session['auth'] == 0:
            return redirect(url_for('auth'))
        if session['state'] != 0 and session['auth'] == 1:
            user_id = session.get('id')
            items = db.get_inventory_by_user_id(user_id)
            return render_template('index.html', items=items)
    else:
        return redirect(url_for('login'))

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    # Verificar si el usuario tiene una sesión iniciada y si es el rol correcto
    if session.get('role') == 'manager':
        if request.method == 'POST':
            # Obtener el token ingresado por el usuario
            entered_token = request.form['token']
            
            url = service + "/verify"
            data = {'entered_token': entered_token, 'email': session.get('email')}
            response = requests.post(url, json=data)
            if response.status_code == 200:
                session['auth'] = response.json()['auth']
                print("Obtained auth:", session['auth'])
            else:
                print("Failed to auth.")

            # Verificar si el token ingresado coincide con el token almacenado en la sesión
            if session['auth'] == 1:
                # Token válido, redirigir al usuario al "manager"
                return redirect(url_for('manager'))
            else:
                # Token inválido, mostrar mensaje de error
                error_message = 'CODIGO INVALIDO'
                return render_template('auth.html', error_message=error_message)

        # Método GET, mostrar formulario para ingresar el token
        return render_template('auth.html')

    else:
        return redirect(url_for('login'))

def schedule_reset_token():
    print("Iniciando cuenta regresiva")
    threading.Timer(45, lambda: None).start()

# Rutas para usuarios
@app.route('/user', methods=['POST'])
def add_user():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    if username and email and password:
        user_data = {
            "username": username,
            "email": email,
            "password": password
        }
        db.insert_user(user_data)

    return redirect(url_for('admin'))

@app.route('/delete/user/<int:user_id>')
def delete_user(user_id):
    db.delete_user(user_id)
    return redirect(url_for('admin'))

@app.route('/edit/user/<int:user_id>', methods=['POST'])
def edit_user(user_id):
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    if user_id and username and email and password:
        user_data = {
            "id": user_id,
            "username": username,
            "email": email,
            "password": password
        }
        db.update_user(user_id, user_data)

    return redirect(url_for('admin'))

# Rutas para inventario
@app.route('/item', methods=['POST'])
def add_item():
    user_id = request.form['userid']
    name = request.form['item_name']
    stock = request.form['stock']
    price = request.form['price']

    if user_id and name and stock and price:
        inventory_data = {
            "userid": user_id,
            "name": name,
            "stock": stock,
            "price": price
        }
        db.insert_inventory(inventory_data)

    return redirect(url_for('manager'))

@app.route('/delete/item/<int:item_id>')
def delete_item(item_id):
    db.delete_inventory(item_id)
    return redirect(url_for('manager'))

@app.route('/edit/item/<int:item_id>', methods=['POST'])
def edit_item(item_id):
    user_id = request.form['userid']
    name = request.form['item_name']
    stock = request.form['stock']
    price = request.form['price']

    if item_id and user_id and name and stock and price:
        inventory_data = {
            "id": item_id,
            "userid": user_id,
            "name": name,
            "stock": stock,
            "price": price
        }
        db.update_inventory(item_id, inventory_data)

    return redirect(url_for('manager'))

# Rutas para autenticación
@app.route('/auth', methods=['POST'])
def add_auth():
    token = request.form['token']
    user_id = request.form['user_id']

    if token and user_id:
        auth_data = {
            "token": token,
            "userid": user_id
        }
        db.insert_auth(auth_data)

    return redirect(url_for('home'))



@app.route('/delete/auth/<int:auth_id>')
def delete_auth(auth_id):
    db.delete_auth(auth_id)
    return redirect(url_for('home'))

@app.route('/edit/auth/<int:auth_id>', methods=['POST'])
def edit_auth(auth_id):
    token = request.form['token']
    user_id = request.form['user_id']

    if auth_id and token and user_id:
        auth_data = {
            "id": auth_id,
            "token": token,
            "userid": user_id
        }
        db.update_auth(auth_id, auth_data)

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True)