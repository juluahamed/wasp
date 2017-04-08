from wasp. __init__ import app, session
from flask import render_template, flash, redirect, url_for
from wasp.database import db_session
from wasp.models import Picture, Item
from wasp.wasp_utils import check_category, check_item

@app.route('/category/<int:category_id>/item/<int:item_id>/edit')
def editItem(category_id, item_id):
	item = db_session.query(Item).filter_by(id=item_id, category_id=category_id).first()
	return render_template('edititem.html', item=item)
