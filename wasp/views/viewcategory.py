from wasp. __init__ import app, session
from flask import render_template, flash, redirect, url_for,jsonify
from wasp.database import db_session
from wasp.models import Item, Picture
from wasp.wasp_utils import check_category, check_item


# API Endpoints for viewCategory
@app.route('/category/<int:category_id>/JSON')
@app.route('/category/<int:category_id>/view/JSON')
def viewCategoryJSON(category_id):
	category = check_category(category_id)
	if category is None:
		return jsonify(error=[{'e_response': "No Category Found"}])
	all_items = db_session.query(Item).filter_by(category_id=category_id).all()
	return jsonify(CategorylItems = [i.serialize for i in all_items])
	
@app.route('/category/<int:category_id>')
@app.route('/category/<int:category_id>/view')
def viewCategory(category_id):
	"""View Function that returns details (Items) for a category """
	category = check_category(category_id)
	if category is None:
		flash('Could not find the category')
		return redirect(url_for('errorNotFound'))
	final_items=[]

	all_items = db_session.query(Item).filter_by(category_id=category_id).all()
	for item in all_items:
		picture = db_session.query(Picture.name).filter_by(item_id=item.id).order_by(Picture.id.desc()).first()
		if not picture:
			picture_name = "sample_image.jpg"
		else:
			picture_name= picture.name
		tmp = {
			'id': item.id,
			'category_id': item.category_id,
			'picture_name': picture_name,
			'name': item.name,
			'description': item.description,
			'time_created': item.time_created

		}
		final_items.append(tmp)
	return render_template('viewcategory.html', items=final_items)
