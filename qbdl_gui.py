from flask import Flask, render_template, request
import logging
from qobuz_dl import QobuzDL

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        url = request.form['url']
        download_location = request.form['download_location']
        quality = int(request.form['quality'])

        qobuz = QobuzDL(
            directory=download_location,
            quality=quality
        )
        qobuz.get_tokens()
        qobuz.initialize_client(email, password, qobuz.app_id, qobuz.secrets)
        qobuz.handle_url(url)

        return "Download started!"
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    
