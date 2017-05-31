from wasp. __init__ import app
from flask import render_template, redirect, url_for, request
from wasp.database import db_session
from wasp.models import Item
from wasp.wasp_utils import generate_csrf_token, user_owns_post, validate_csfr, generate_csrf_delete_token

@app.route('/category/<int:category_id>/item/<int:item_id>/edit', methods=['GET','POST'])
@user_owns_post
def editItem(category_id, item_id):
	""" View function for editing Item. Performs CSFR validation """
	if request.method == 'POST':
		csfr_token = request.form.get('_csrf_token')
		validate_csfr(csfr_token)
		catName = request.form.get('catName')
		itemName = request.form.get('itemName')
		itemDescription = request.form.get('itemDescription')
		item = db_session.query(Item).filter_by(id=item_id, category_id=category_id).first()
		item.name = itemName
		item.description = itemDescription
		db_session.add(item)
		db_session.commit()
		return redirect(url_for('viewItem', item_id=item_id, category_id=category_id))
	app.jinja_env.globals['csrf_token'] = generate_csrf_token
	app.jinja_env.globals['csrf_delete_token'] = generate_csrf_delete_token
	item = db_session.query(Item).filter_by(id=item_id, category_id=category_id).first()
	return render_template('edititem.html', item=item)

