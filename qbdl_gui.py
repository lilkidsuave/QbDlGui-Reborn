from flask import Flask, render_template, request, session, jsonify
import logging
from qobuz_dl import QobuzDL

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.secret_key = '%8Yn+K9_t:L;EiZ9;G=CMCba5%u4}5STN$(,QRi/Fcn;M0d5jdp9,iv?KzD!,}neh]mK{:8ix5!!v9=aY3T[_WR;&:T52Q!XEWA/Fbuq+T-5a&9bBQPK)-]Q[5b'

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
            qobuz = QobuzDL(
                directory=download_location,
                quality=quality
            )
            qobuz.get_tokens()
            qobuz.initialize_client(email, password, qobuz.app_id, qobuz.secrets)
            qobuz.handle_url(url)
        except Exception as e:
            logging.error("An error occurred: " + str(e))
            return jsonify(status='error', message=str(e)), 500

        if remember == 'on':
            session['email'] = email
            session['password'] = password
            session['download_location'] = download_location
            session['quality'] = quality

        return jsonify(status='completed')

    email = session.get('email', '')
    download_location = session.get('download_location', '')
    quality = session.get('quality', 7)

    return render_template('index.html', email=email, download_location=download_location, quality=quality)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
