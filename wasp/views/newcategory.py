from wasp. __init__ import app, session, UPLOAD_FOLDER
from flask import request, redirect, flash, url_for,render_template
from wasp.database import db_session
from wasp.models import Category
from wasp.wasp_utils import allowed_file, rename_file, login_required
import os

@app.route('/newcategory', methods=['GET','POST'])
@login_required
def newCategory():
	#if not session.get('username'):
		#flash('You should be logged in to add new categories. Log in here')
		#return redirect(url_for('showLogin'))
	
	if request.method == 'POST':
		catName = request.form.get('catName')
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part in the request')
			return redirect(request.url)
		file = request.files['file']
		# if user does not select file, browser also
		# submit a empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		
		if not catName:
			return redirect(request.url)

		if file and allowed_file(file.filename):
			filename = rename_file(catName,file.filename)
			print filename
			#user = db_session.query(User).filter_by(id=session['user_id']).one()
			new_category = Category(name=catName, user_id=session['user_id'], picture=filename)
			db_session.add(new_category)
			db_session.commit()
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			flash('New category %s added!' %catName)
			return redirect(url_for('showCategory'))
		else:
			return redirect(request.url)
	else:
		return render_template('newcategory.html')



