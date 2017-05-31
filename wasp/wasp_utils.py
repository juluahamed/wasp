from flask import flash, redirect, url_for, abort
from __init__ import session
from werkzeug.utils import secure_filename
from database import db_session
from models import Category,Item
from functools import wraps
import string
import random

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# Check if uploaded file is of allowed extension
def allowed_file(filename):
	if '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
		return True
	else:
		flash('Invalid file. Accepted file formats : .jpg, jpeg, png')
		return False

# Rename the uploading file
def rename_file(*args):
	filename = secure_filename(args[1])
	filename = filename.replace(' ', '_')
	
	if len(args) == 2:
		return args[0]+'.'+ filename.rsplit('.', 1)[1].lower()
	else:
		return args[0]+ '_' + args[2]+ '_' + str(args[3]) + '_' + str(args[4]) +'.'+ filename.rsplit('.', 1)[1].lower()

# Check if category exsists
def check_category(category_id):
	return db_session.query(Category).filter_by(id=category_id).first()

# Check If item exsists
def check_item(item_id, category_id):
	return db_session.query(Item).filter_by(id=item_id, category_id=category_id).first()

# Check if user is logged in. Else Redirect
def login_required(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		if session.get('username'):
			return func(*args, **kwargs)
		else:
			flash('You should be logged in to perform this operation')
			return redirect(url_for('showLogin'))
	return wrapper

# Check if the logged in user is the owner of the post. Else Forbid operation
def user_owns_post(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		item = db_session.query(Item).filter_by(id=kwargs['item_id'], category_id=kwargs['category_id']).first()
		if item and session.get('user_id') == item.user_id:
			return func(*args, **kwargs)
		else:
			abort(403)
	return wrapper

# Check if the logged in user created the category. Else forbid operation
def user_owns_category(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		category = db_session.query(Category).filter_by(id=kwargs['category_id']).first()
		if category and session.get('user_id') == category.user_id:
			return func(*args, **kwargs)
		else:
			abort(403)
	return wrapper

# Create token for CSFR protection
def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = ''.join(random.choice(string.lowercase) for x in range(10))
    return session['_csrf_token']

# Create token for delete operation for CSFR protection 
def generate_csrf_delete_token():
	if '_csrf_delete_token' not in session:
		session['_csrf_delete_token'] = ''.join(random.choice(string.lowercase) for x in range(10))
	return session['_csrf_delete_token']

# Validate CSFR token
def validate_csfr(csrf_token):
	token = session.pop('_csrf_token', None)
	if not token or token != csrf_token:
		abort(403)

# Validate delete CSFR token
def validate_delete_csfr(csrf_delete_token):
	token = session.pop('_csrf_delete_token', None)
	if not token or token != csrf_delete_token:
		abort(403)



