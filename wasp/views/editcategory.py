from wasp. __init__ import app
from flask import render_template, flash, redirect, request
from wasp.database import db_session
from wasp.models import Category
from wasp.wasp_utils import generate_csrf_token, user_owns_category, validate_csfr, generate_csrf_delete_token
from wasp.wasp_utils import allowed_file, rename_file
import os

@app.route('/category/<int:category_id>/edit', methods=['GET','POST'])
@user_owns_category
def editCategory(category_id):
	""" View function for editing category. Performs CSFR validation """
	if request.method == 'POST':
		csfr_token = request.form.get('_csrf_token')
		validate_csfr(csfr_token)
		catName = request.form.get('catName')

		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part in the request')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		categories = db_session.query(Category).all()
		if file and allowed_file(file.filename):
			filename = rename_file(catName,file.filename)
			print filename
			#user = db_session.query(User).filter_by(id=session['user_id']).one()
			category = db_session.query(Category).filter_by(id=category_id).one()
			category.name = catName
			old_filename = category.picture
			category.picture = filename
			db_session.add(category)
			db_session.commit()
			os.remove(os.path.join(app.config['UPLOAD_FOLDER'], old_filename))
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			flash('Category %s edited!' %catName)
			return render_template('category.html', categories=categories)

		category = db_session.query(Category).filter_by(id=category_id).one()
		category.name = catName
		db_session.add(category)
		db_session.commit()
		return render_template('category.html', categories=categories)
	app.jinja_env.globals['csrf_token'] = generate_csrf_token
	app.jinja_env.globals['csrf_delete_token'] = generate_csrf_delete_token
	category = db_session.query(Category).filter_by(id=category_id).one()
	print category.name
	return render_template('editcategory.html', category=category)

