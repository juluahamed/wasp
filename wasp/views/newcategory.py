from wasp. __init__ import app, session, UPLOAD_FOLDER
from flask import request, redirect, flash, url_for,render_template
from wasp.database import db_session
from wasp.models import Category
from wasp.wasp_utils import allowed_file, rename_file, login_required, generate_csrf_token, validate_csfr
import os

@app.route('/newcategory', methods=['GET','POST'])
@login_required
def newCategory():
	""" View Function to create a new category. Performs CSFR validation """
	if request.method == 'POST':
		csfr_token = request.form.get('_csrf_token')
		validate_csfr(csfr_token)
		catName = request.form.get('catName')
		
		# Check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part in the request')
			return redirect(request.url)
		
		file = request.files['file']
		
		# If user does not select file, browser also
		# submit a empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		
		if not catName:
			return redirect(request.url)

		if file and allowed_file(file.filename):
			filename = rename_file(catName,file.filename)
			new_category = Category(name=catName, user_id=session['user_id'], picture=filename)
			db_session.add(new_category)
			db_session.commit()
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			flash('New category %s added!' %catName)
			return redirect(url_for('showCategory'))
		else:
			return redirect(request.url)
	else:
		app.jinja_env.globals['csrf_token'] = generate_csrf_token
		return render_template('newcategory.html')



