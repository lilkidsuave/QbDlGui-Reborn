from flask import Flask, render_template, request, session, jsonify
from cryptography.fernet import Fernet
import logging
import os
from qobuz_dl import QobuzDL

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Auto-generate a secret key and an encryption key
app.secret_key = os.environ.get('SECRET_KEY') or os.urandom(24)
encryption_key = os.environ.get('ENCRYPTION_KEY') or Fernet.generate_key()
fernet = Fernet(encryption_key)

qobuz_dl = None  # Initialize QobuzDL instance globally

def encrypt_password(password):
    return fernet.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    return fernet.decrypt(encrypted_password.encode()).decode()

@app.route('/', methods=['GET', 'POST'])
def index():
    global qobuz_dl

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        url = request.form['url']
        download_location = request.form['download_location']
        quality = int(request.form['quality'])
        remember = request.form.get('rememberMe')
        search_type = request.form.get('searchType')  # Get search type from form

        try:
            qobuz_dl = QobuzDL(
                directory=download_location,
                quality=quality
            )
            qobuz_dl.get_tokens()
            qobuz_dl.initialize_client(email, password, qobuz_dl.app_id, qobuz_dl.secrets)
            # Handle search based on type
            results = qobuz_dl.search_by_type(url, search_type, limit=10)
            return render_template('index.html', email=email, password=password,
                                   download_location=download_location, quality=quality,
                                   search_results=results)
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

# Route to handle AJAX search requests
@app.route('/search', methods=['GET'])
def search():
    global qobuz_dl

    query = request.args.get('query')
    search_type = request.args.get('searchType')

    if query and search_type and qobuz_dl:
        try:
            results = qobuz_dl.search_by_type(query, search_type, limit=10)
            return jsonify(results)
        except Exception as e:
            logging.error(f"An error occurred during search: {str(e)}")
            return jsonify([])  # Return empty list on error

    return jsonify([])  # Return empty list if no query or search type provided

if __name__ == '__main__':
    app.run(debug=True)
