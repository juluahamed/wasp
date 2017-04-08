from wasp. __init__ import app
from flask import send_from_directory
from wasp.wasp_utils import login_required

@app.route('/uploads/<filename>')
@login_required
def uploadedFile(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)