from flask import Flask, render_template, flash, request, redirect, url_for,send_file
import os
from werkzeug.utils import secure_filename
import sys
import subprocess
from zipfile import ZipFile,ZIP_LZMA
import shutil
import uuid

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'wav'}

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    print(uuid.uuid1(), file=sys.stderr)
    #print('Hello world!', file=sys.stderr)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        #print(temp, file=sys.stderr)
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        upload_dir =f"./uploads/{uuid.uuid1()}" 
        os.makedirs(upload_dir)
        files = request.files.getlist('file')
        
        for i in range(len(files)):
            file = files[i]
            if not allowed_file(file.filename):
                return '''
                    <!doctype html>
                    <title>Upload new File</title>
                    <h1>Arquivo Invalido</h1>
                    </form>
                ''' 
            filename = secure_filename(file.filename)
            file.save(os.path.join(upload_dir, filename))

        subprocess.run(["audio_convertio", upload_dir,"wav","mp3"])
        zipObj = ZipFile(f"{upload_dir}/converted.zip", 'w',ZIP_LZMA)
        for i in range(len(files)):
            file = files[i]
            filename = f"{upload_dir}/{secure_filename(file.filename).split('.')[0]}.mp3"
            zipObj.write(filename)
            os.remove(f"{upload_dir}/{secure_filename(file.filename)}") 
            os.remove(f"{upload_dir}/{secure_filename(file.filename).split('.')[0]}.mp3") 
        # close the Zip File
        zipObj.close()
        return send_file(f'{upload_dir}/converted.zip',mimetype='application/x-zip', as_attachment=True)
    return render_template('index.html')



