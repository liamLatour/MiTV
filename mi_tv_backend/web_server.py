from flask import Flask, send_from_directory
from flask_cors import CORS

# run with: waitress-serve --host 127.0.0.1 --port=80 --threads=12 web_server:app

app = Flask(__name__)
CORS(app)

# Serves flutter app

@app.route('/<path:name>')
def render_page_web(name):
    return send_from_directory("static", 'index.html')

@app.route('/')
def page_web():
    return send_from_directory("static", 'index.html')

@app.route('/static/<path:name>')
def return_flutter_doc(name):
    return send_from_directory("static", name)

if __name__ == '__main__':
    app.run()