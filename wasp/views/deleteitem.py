from wasp. __init__ import app
from flask import redirect, url_for, request
from wasp.database import db_session
from wasp.models import Item, Picture, Like
from wasp.wasp_utils import user_owns_post, validate_delete_csfr
import os

@app.route('/category/<int:category_id>/item/<int:item_id>/delete', methods=['POST'])
@user_owns_post
def deleteItem(category_id, item_id):
	""" View function for deleting item. Performs CSFR validation """
	if request.method == 'POST':
		csfr_delete_token = request.form.get('_csrf_delete_token')
		validate_delete_csfr(csfr_delete_token)
		item = db_session.query(Item).filter_by(id=item_id, category_id=category_id).first()
		db_session.delete(item)
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
		return redirect(url_for('viewCategory', category_id=category_id))