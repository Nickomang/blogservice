from flask import Flask, request, jsonify, redirect, url_for
from flask_basicauth import BasicAuth
from secrets import password
import json
import os


app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'nicolas'
app.config['BASIC_AUTH_PASSWORD'] = password

basic_auth = BasicAuth(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() == 'json'

@app.route("/posts")
def posts():
    with open('posts.json', 'r') as json_file:
        res = json.load(json_file)
    return jsonify(res)

@app.route("/upload", methods=['GET', 'POST'])
@basic_auth.required
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'NO FILE'
        file = request.files['file']
        if file.filename == '':
            return 'FILENAME BLANK'
            return redirect(url_for('posts'))
        if file and allowed_file(file.filename):
            file.save('posts.json')
    return redirect(url_for('posts'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)