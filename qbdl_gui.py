from flask_socketio import SocketIO, emit
from flask import Flask, render_template, request, session, jsonify
from cryptography.fernet import Fernet
import logging
import os
from qobuz_dl import QobuzDL

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
socketio = SocketIO(app)

app.secret_key = os.environ.get('SECRET_KEY') or os.urandom(24)
encryption_key = os.environ.get('ENCRYPTION_KEY') or Fernet.generate_key()
fernet = Fernet(encryption_key)

def encrypt_password(password):
    return fernet.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    return fernet.decrypt(encrypted_password.encode()).decode()

def download_files(qobuz, url_list):
    total_files = len(url_list)
    for idx, url in enumerate(url_list, start=1):
        qobuz.handle_url(url)
        socketio.emit('progress_update', {'downloaded': idx, 'total': total_files})

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        url = request.form['url']
        download_location = request.form['download_location']
        quality = int(request.form['quality'])
        remember = request.form.get('rememberMe')

        try:
            qobuz = QobuzDL(directory=download_location, quality=quality)
            qobuz.get_tokens()
            qobuz.initialize_client(email, password, qobuz.app_id, qobuz.secrets)
            download_files(qobuz, [url])
        except Exception as e:
            logging.error("An error occurred: " + str(e))
            return jsonify(status='error', message='An internal error occurred. Please try again later.'), 500

        if remember == 'on':
            session['email'] = email
            session['password'] = encrypt_password(password)
            session['download_location'] = download_location
            session['quality'] = quality

        return jsonify(status='completed')

    email = session.get('email', '')
    encrypted_password = session.get('password', '')
    password = decrypt_password(encrypted_password) if encrypted_password else ''
    download_location = session.get('download_location', '')
    quality = session.get('quality', 7)

    return render_template('index.html', email=email, password=password, download_location=download_location, quality=quality)

if __name__ == "__main__":
    socketio.run(app)
