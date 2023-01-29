import os
from flask import Flask, flash, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

csrf = CSRFProtect()
app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

csrf.init_app(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.post('/process-file')
def process_file():
    if 'file' not in request.files:
        flash('Please select a file.')
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        flash('Please select a file.')
        return redirect(url_for('index'))

    if file:
        if not allowed_file(file.filename):
            flash('Invalid file type. Please choose one of the accepted below.')
            return redirect(url_for('index'))

        filename = secure_filename(file.filename)

        # proces flle...
        print('processing file.....')

        return redirect(url_for('download_file', name=filename))

    return redirect(url_for('index'))

# if __name__ == '__main__':
#     app.run(debug=True)
