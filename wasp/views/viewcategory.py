from wasp. __init__ import app, session
from flask import render_template
from wasp.database import db_session
from wasp.models import User, Category, Item, Picture

@app.route('/category/<int:category_id>')
@app.route('/category/<int:category_id>/view')
def viewCategory(category_id):
	all_items = db_session.query(Item).filter_by(category_id=category_id).all()
	return render_template('viewcategory.html', items=all_items)