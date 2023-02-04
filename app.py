import os
import time
from flask import Flask, flash, redirect, url_for, request, render_template, send_from_directory
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect
from rembg import remove

UPLOAD_FOLDER = './static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
SECRET_KEY = os.urandom(32)

csrf = CSRFProtect()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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

        # save the file
        file.save(os.path.join(app.config['UPLOAD_FOLDER'] + '/rinsed/', filename))

        input_path = filename
        output_filename = 'rinsed_' + filename
        output_path = os.path.join(app.config['UPLOAD_FOLDER'] + 'rinsed/', output_filename)

        print(output_path)

        with open(input_path, 'rb') as i:
            with open(output_path, 'wb') as o:
                input = i.read()
                output = remove(input)
                o.write(output)

                return send_from_directory(app.config["UPLOAD_FOLDER"], output_path)

    flash('No file provided.')
    return redirect(request.url)

# if __name__ == '__main__':
#     app.run(debug=True)
