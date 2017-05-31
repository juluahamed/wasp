from wasp. __init__ import app, session
from flask import redirect, url_for, request
from wasp.database import db_session
from wasp.models import Category, Item, Picture, Like
from wasp.wasp_utils import validate_delete_csfr
from wasp.wasp_utils import user_owns_category
import os

@app.route('/category/<int:category_id>/delete', methods=['POST'])
@user_owns_category
def deleteCategory(category_id):
	""" View function for deleting category. Performs CSFR validation"""
	if request.method == 'POST':
		csfr_delete_token = request.form.get('_csrf_delete_token')
		validate_delete_csfr(csfr_delete_token)
		category = db_session.query(Category).filter_by(id=category_id).first()
		os.remove(os.path.join(app.config['UPLOAD_FOLDER'], category.picture))
		items =db_session.query(Item).filter_by(category_id=category_id).all()
		for i in items:
			item_id = i.id
			db_session.delete(i)
			db_session.commit()
			pictures= db_session.query(Picture).filter_by(item_id=item_id).all()
			for p in pictures:
				db_session.delete(p)
				db_session.commit()
				os.remove(os.path.join(app.config['UPLOAD_FOLDER'], p.name))
			likes = db_session.query(Like).filter_by(item_id=item_id, category_id=category_id).all()
			for l in likes:
				db_session.delete(l)
				db_session.commit()
		db_session.delete(category)
		db_session.commit()
		return redirect(url_for('showCategory'))
