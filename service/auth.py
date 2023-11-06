import os, random, string, smtplib, flask, json, threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import request, jsonify, render_template
from flask import Flask

app = Flask(__name__)

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'service', 'templates')

app.template_folder = template_dir

# Obtén la ruta del directorio actual
current_directory = os.path.dirname(os.path.abspath(__file__))

# Enviar correo electrónico de registro al gerente de la aplicación
def send_register_email(email):
    # Configurar los detalles del correo electrónico
    sender_email = 'pro1auth@gmail.com'  # Tu dirección de correo electrónico
    sender_password = 'pllrpnwshfgdhmcv'  # Tu contraseña de correo electrónico

    subject = 'Registro en Manager App'
    message = 'Saludos, te has registrado en Manager App.'

    # Crear el mensaje de correo electrónico
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    # Enviar el correo electrónico usando SMTP
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)

# Enviar correo electrónico con el token al usuario manager
def send_token_email(email, token):
    # Configurar los detalles del correo electrónico
    sender_email = 'pro1auth@gmail.com'  # Tu dirección de correo electrónico
    sender_password = 'pllrpnwshfgdhmcv'  # Tu contraseña de correo electrónico

    subject = 'Token de autenticación'
    message = f'Su token de autenticación es: {token}'

    # Crear el mensaje de correo electrónico
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    # Enviar el correo electrónico usando SMTP
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)

# Generar un token de 6 caracteres que solo contenga letras mayúsculas y dígitos
def generate_token():
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=6))

@app.route('/', methods=['GET', 'POST'])
def home():
    message = 'El servicio se está ejecutando.'
    return render_template('home.html', message=message)

@app.route('/auth', methods=['POST'])
def auth_process():
    data = request.json
    state = data.get('state')
    email = data.get('email')

    if state == 0:
        # Generar un token y almacenarlo en la sesión
        token = generate_token()
        print("service: " + token)

        # Enviar el token al correo electrónico del usuario manager
        send_token_email(email, token)

        # Cargar los datos actuales desde el archivo JSON
        data = load_data()

        # Actualizar el token en los datos correspondientes al email
        for item in data:
            if item['email'] == email:
                item['token'] = token
                break
        else:
            # Si no se encontró el email, agregar un nuevo registro
            data.append({'email': email, 'token': token})

        # Guardar los datos actualizados en el archivo JSON
        save_data(data)
        schedule_reset_token(email)

        return jsonify({'state': 1})
    else:
        return

@app.route('/register', methods=['POST'])
def send_register_email_route():
    data = request.json
    email = data.get('email')

    send_register_email(email)

    return jsonify({'message': 'Registro Exitoso'})

@app.route('/verify', methods=['POST'])
def verify():
    data = request.json
    email = data.get('email')
    entered_token = data.get('entered_token')
    token = 0
    auth = 0

    # Cargar los datos actuales desde el archivo JSON
    data = load_data()

    # Actualizar el token en los datos correspondientes al email
    for item in data:
        if item['email'] == email:
            token= item['token']
            break

    # Verificar si el token ingresado coincide con el token almacenado en la sesión
    if entered_token == token:
        # Token válido, redirigir al usuario al "manager"
        auth = 1
    else:
        # Token inválido, mostrar mensaje de error
        auth = 0

    return jsonify({'auth': auth})

#FUNCIONES DE MANEJO DE DATOS
# Obtén la ruta del directorio actual
current_directory = os.path.dirname(os.path.abspath(__file__))

# Construye la ruta relativa al archivo users.json
auth_json_path = os.path.join(current_directory, 'auth.json')

def load_data():
    with open(auth_json_path, 'r') as file:
        data = json.load(file)
    return data

def save_data(data):
    with open(auth_json_path, 'w') as file:
        json.dump(data, file, indent=4)

def reset_token(email):
    # Cargar los datos actuales desde el archivo JSON
    data = load_data()

    # Restablecer el token a 0 para el email correspondiente
    for item in data:
        if item['email'] == email:
            item['token'] = 0
            break

    # Guardar los datos actualizados en el archivo JSON
    save_data(data)

    print(f"Token expirado para: {email}")

# Llamar a la función reset_token después de 45 segundos
def schedule_reset_token(email):
    print(f"Iniciando cuenta regresiva para: {email}")
    threading.Timer(50, reset_token, args=(email,)).start()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)