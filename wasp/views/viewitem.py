from wasp. __init__ import app, session
from flask import render_template, flash, redirect, url_for, jsonify
from wasp.database import db_session
from wasp.models import Picture, Like
from wasp.wasp_utils import check_category, check_item


# API Endpoints for viewItem
@app.route('/category/<int:category_id>/item/<int:item_id>/JSON')
@app.route('/category/<int:category_id>/item/<int:item_id>/view/JSON')
def viewItemJSON(category_id, item_id):
	category = check_category(category_id)
	if category is None:
		return jsonify(error=[{'e_response': "No Category Found"}])
	item = check_item(item_id, category_id)
	if item is None:
		return jsonify(error=[{'e_response': "No Items Found"}])
	pictures = db_session.query(Picture).filter_by(item_id=item.id).order_by(Picture.id.desc()).all()
	return jsonify(Items = [item.serialize], Pictures=[p.serialize for p in pictures])

@app.route('/category/<int:category_id>/item/<int:item_id>')
@app.route('/category/<int:category_id>/item/<int:item_id>/view')
def viewItem(category_id, item_id):
	""" View function for displaying item"""
	category = check_category(category_id)
	if category is None:
		flash('Could not find the category')
		return redirect(url_for('errorNotFound'))
	item = check_item(item_id, category_id)
	if item is None:
		flash('Could not find the item')
		return redirect(url_for('errorNotFound'))
	
	likes = db_session.query(Like).filter_by(category_id =item.category.id, item_id=item.id).count()

	if session.get('user_id'):
		liked = db_session.query(Like).filter_by(category_id =item.category.id, item_id=item.id, user_id = session.get('user_id')).first()
	else:
		liked = False

	pictures = db_session.query(Picture.name).filter_by(item_id=item.id).order_by(Picture.id.desc()).all()
	if pictures == []:
		default_picture = "sample_image.jpg"
	else:
		default_picture = pictures[0].name

	return render_template('viewitem.html', item=item, pictures=pictures, default_picture=default_picture, liked=liked, likes=likes)