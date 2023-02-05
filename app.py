import os
import time
from flask import Flask, flash, redirect, request, render_template, send_file
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect
from rembg import remove

UPLOAD_FOLDER = './static/uploads/'
UPLOAD_FOLDER_RINSED = './static/uploads/rinsed/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
SECRET_KEY = os.urandom(32)

csrf = CSRFProtect()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_RINSED'] = UPLOAD_FOLDER_RINSED
app.config['SECRET_KEY'] = SECRET_KEY

csrf.init_app(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.get('/')
def index_get():
    return render_template('index.html')

@app.post('/')
def index_post():
    if 'file' not in request.files:
        flash('Please select a file.')
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        flash('Please select a file.')
        return redirect(request.url)

    if file:
        if not allowed_file(file.filename):
            flash('Invalid file type. Please choose one of the accepted types.')
            return redirect(request.url)

        filename = secure_filename(file.filename)
        filename = str(time.time()).replace(".", "") + '_' + filename

        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)

        output_filename = 'rinsed_' + filename
        output_path = os.path.join(app.config['UPLOAD_FOLDER_RINSED'], output_filename)

        with open(input_path, 'rb') as i:
            with open(output_path, 'wb') as o:
                input = i.read()
                output = remove(input)
                o.write(output)

                return send_file(output_path, as_attachment=True)

    flash('No file provided.')
    return redirect(request.url)
