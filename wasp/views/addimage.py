from wasp. __init__ import app, session, UPLOAD_FOLDER
from flask import request, redirect, flash, url_for,render_template
from wasp.database import db_session
from wasp.models import Category,Item, Picture
from wasp.wasp_utils import allowed_file, rename_file, check_category, check_item, login_required
import os

@app.route('/category/<int:category_id>/item/<int:item_id>/addimage', methods=['GET','POST'])
@login_required
def addImage(category_id, item_id):
	""" View function for adding new images to item """
	if request.method == 'POST':
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

		pic_num = db_session.query(Picture.id).order_by(Picture.id.desc()).first()
		
		if pic_num is None:
			pic_num = 0
		else:
			pic_num = pic_num[0]
		
		pic_num += 1
		
		# If file is present, store the meta data in the db and store the image in the file directory
		if file and allowed_file(file.filename):
			item = check_item(item_id, category_id)

			filename = rename_file(item.name, file.filename, item.category.name, item_id, pic_num)
			new_picture = Picture(name=filename, item_id=item_id, user_id=session['user_id'])
			db_session.add(new_picture)
			db_session.commit()
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			flash('Picture upload successful')
			return redirect(url_for('viewItem', item_id= item_id, category_id=item.category.id))
		else:
			flash('Invalid file format')
			return redirect(request.url)
	else:
		category = check_category(category_id)
		if category is None:
			flash('We could not find that category')
			return redirect(url_for('errorNotFound'))
		item = check_item(item_id,category_id)
		if item is None:
			flash('We could not find that item')
			return redirect(url_for('errorNotFound'))
		return render_template('addimage.html', item_id=item_id, category_id=category_id)

