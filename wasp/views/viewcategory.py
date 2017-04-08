from wasp. __init__ import app, session
from flask import render_template, flash, redirect, url_for
from wasp.database import db_session
from wasp.models import Item
from wasp.wasp_utils import check_category, check_item

@app.route('/category/<int:category_id>')
@app.route('/category/<int:category_id>/view')
def viewCategory(category_id):
	category = check_category(category_id)
	if category is None:
		flash('Could not find the category')
		return redirect(url_for('errorNotFound'))

	all_items = db_session.query(Item).filter_by(category_id=category_id).all()
	return render_template('viewcategory.html', items=all_items)