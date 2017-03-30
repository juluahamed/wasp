from wasp. __init__ import app
from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploadedFile(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)