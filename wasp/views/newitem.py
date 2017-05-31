# -*- coding: utf-8 -*-
from wasp. __init__ import app, session, UPLOAD_FOLDER
from flask import request, redirect, flash, url_for,render_template
from wasp.database import db_session
from wasp.models import Category, Item, Picture
from wasp.wasp_utils import allowed_file, rename_file, login_required, validate_csfr, generate_csrf_token
import os

@app.route('/newitem', methods=['GET','POST'])
@login_required
def newItem():
	""" View function to create new Item. Performs CSFR validation """
	if request.method == 'POST':
		csfr_token = request.form.get('_csrf_token')
		validate_csfr(csfr_token)
		catName = request.form.get('catName')
		itemName = request.form.get('itemName')
		itemDescription = request.form.get('itemDescription')

		# Field validations are already performed at client side with JS
		# Catches empty field value in case of forged post request
		if not catName or not itemName or not itemDescription:
			return redirect(request.url)


		
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part in the request')
			return redirect(request.url)
		file = request.files['file']
		
		# if user does not select file, browser also
		# submit a empty part without filename
		
		if not itemName:
			return redirect(request.url)

		# Find the id of next item and its image in db and use it in rename the file 
		# accordingly for storage
		item_id = db_session.query(Item.id).order_by(Item.id.desc()).first()
		pic_num = db_session.query(Picture.id).order_by(Picture.id.desc()).first()
		if item_id is None:
			item_id = 0
		else:
			item_id = item_id[0]

		if pic_num is None:
			pic_num = 0
		else:
			pic_num = pic_num[0]
		
		item_id += 1
		pic_num += 1
		print item_id,pic_num

		if file:
			if allowed_file(file.filename):
				filename = rename_file(itemName,file.filename,catName,item_id,pic_num)
				category = db_session.query(Category.id).filter_by(name=catName).one()
				new_item = Item(name=itemName, description=itemDescription, category_id = category.id, user_id=session['user_id'])
				db_session.add(new_item)
				db_session.commit()
				new_picture = Picture(name=filename, item_id=new_item.id, user_id = session['user_id'])
				db_session.add(new_picture)
				db_session.commit()
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				flash('New Item %s added!' %itemName)
				return redirect(url_for('showCategory'))
			else:
				flash("Invalid format")
				return redirect(request.url)
		else:
			category = db_session.query(Category.id).filter_by(name=catName).one()
			new_item = Item(name=itemName, description=itemDescription, category_id = category.id, user_id=session['user_id'])
			db_session.add(new_item)
			db_session.commit()
			flash('New Item %s added!' %itemName)
			return redirect(url_for('showCategory'))
	else:
		app.jinja_env.globals['csrf_token'] = generate_csrf_token
		categories=db_session.query(Category.name).all()

		# To make this list JSON serializable for autocomplete functionality in template
		categories = [category[0] for category in categories]
		return render_template('newitem.html', categories=categories)

