# -*- coding: utf-8 -*-
from wasp. __init__ import app, session, UPLOAD_FOLDER
from flask import request, redirect, flash, url_for,render_template
from wasp.database import db_session
from wasp.models import Category, Item, Picture
from wasp.wasp_utils import allowed_file, rename_file
import os

@app.route('/newitem', methods=['GET','POST'])
def newItem():
	print "Just at the begining"
	print session.get('_flashes', [])
	if not session.get('username'):
		flash('You should be logged in to add new items. Log In here')
		return redirect(url_for('showLogin'))

	if request.method == 'POST':
		print "inside post"
		print session.get('_flashes', [])

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
		print "Just before storage IDs"
		print session.get('_flashes', [])
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
			print "Inside If file"
			print session.get('_flashes', [])
			if allowed_file(file.filename):
				print "Inside allowed file"
				print session.get('_flashes', [])
				filename = rename_file(itemName,file.filename,catName,item_id,pic_num)
				print filename
				#user = db_session.query(User).filter_by(id=session['user_id']).one()
				category = db_session.query(Category.id).filter_by(name=catName).one()
				new_item = Item(name=itemName, description=itemDescription, category_id = category.id, user_id=session['user_id'])
				db_session.add(new_item)
				db_session.commit()
				print new_item.id

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
			print new_item.id
			return redirect(url_for('showCategory'))
	else:
		categories=db_session.query(Category.name).all()
		# To make this list JSON serializable for autocomplete functionality in template
		categories = [category[0] for category in categories]
		return render_template('newitem.html', categories=categories)

