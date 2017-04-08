from wasp. __init__ import app, session
from flask import render_template, flash, redirect, url_for
from wasp.database import db_session
from wasp.models import Picture
from wasp.wasp_utils import check_category, check_item

@app.route('/category/<int:category_id>/item/<int:item_id>')
@app.route('/category/<int:category_id>/item/<int:item_id>/view')
def viewItem(category_id, item_id):
	category = check_category(category_id)
	if category is None:
		flash('Could not find the category')
		return redirect(url_for('errorNotFound'))
	item = check_item(item_id, category_id)
	if item is None:
		flash('Could not find the item')
		return redirect(url_for('errorNotFound'))

	#item = db_session.query(Item).filter_by(id=item_id).one()
	pictures = db_session.query(Picture.name).filter_by(item_id=item.id).order_by(Picture.id.desc()).all()
	if pictures == []:
		default_picture = "sample_image.png"
	else:
		default_picture = pictures[0].name

	#print picture
	return render_template('viewitem.html', item=item, pictures=pictures, default_picture=default_picture)