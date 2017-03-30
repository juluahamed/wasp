from flask import flash 
from werkzeug.utils import secure_filename
import string

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
	if '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
		return True
	else:
		flash('Invalid file. Accepted file formats : .jpg, jpeg, png')
		return False

def rename_file(*args):
	filename = secure_filename(args[1])
	filename = filename.replace(' ', '_')
	if len(args) == 2:
		return args[0]+'.'+ filename.rsplit('.', 1)[1].lower()
	else:
		return args[0]+ '_' + args[2]+ '_' + str(args[3]) + '_' + str(args[4]) +'.'+ filename.rsplit('.', 1)[1].lower()


