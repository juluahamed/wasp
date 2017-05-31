from wasp. __init__ import app, session
from flask import request, redirect, flash, url_for
from wasp.database import db_session
from wasp.models import Picture
from wasp.wasp_utils import login_required
import os

@app.route('/deleteimage/<string:image>')
@login_required
def deleteItemImage(image):
	""" View function for deleting item images"""
	picture = db_session.query(Picture).filter_by(name=image).first()
	if not picture:
		flash('Could not find the image')
		return redirect(url_for('errorNotFound'))
	if session.get('user_id') == picture.item.user_id:
		os.remove(os.path.join(app.config['UPLOAD_FOLDER'], picture.name))
		db_session.delete(picture)
		db_session.commit()
		return redirect(url_for('viewItem', category_id=picture.item.category_id, item_id=picture.item.id))
	else:
		return redirect(url_for('viewItem', category_id=picture.item.category_id, item_id=picture.item.id))
	return redirect(url_for('showCategory'))