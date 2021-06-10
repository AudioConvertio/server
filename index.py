from flask import Flask, render_template, flash, request, redirect, url_for,send_file
import os
from werkzeug.utils import secure_filename
import sys
import subprocess

app = Flask(__name__)

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    print('Hello world!', file=sys.stderr)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        temp = file.save(os.path.join('./uploads', 'converted.wav'))
        print(temp, file=sys.stderr)
        subprocess.run(["audio_convertio", "uploads","wav","mp3"])
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        return send_file('./uploads/converted.mp3',mimetype='audio/mp3', as_attachment=True)
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            return redirect(url_for('download_file', name=filename))
    return render_template('index.html')



