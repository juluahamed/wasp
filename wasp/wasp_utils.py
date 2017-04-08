from flask import flash, redirect, url_for
from __init__ import session
from werkzeug.utils import secure_filename
from database import db_session
from models import Category,Item
from functools import wraps
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

def check_category(category_id):
	return db_session.query(Category).filter_by(id=category_id).first()

def check_item(item_id, category_id):
	return db_session.query(Item).filter_by(id=item_id, category_id=category_id).first()

def login_required(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		if session.get('username'):
			return func(*args, **kwargs)
		else:
			flash('You should be logged in to perform this operation')
			return redirect(url_for('showLogin'))
	return wrapper



