from wasp. __init__ import app, session, UPLOAD_FOLDER
from flask import request, redirect, flash, url_for,render_template
from wasp.database import db_session
from wasp.models import Category, Picture
from wasp.wasp_utils import allowed_file, rename_file, login_required
import os

@app.route('/deleteimage/<string:image>')
@login_required
def deleteItemImage(image):
	picture = db_session.query(Picture).filter_by(name=image).first()
	print "logged in"
	print picture
	if not picture:
		flash('Could not find the image')
		return redirect(url_for('errorNotFound'))
	if session.get('user_id') == picture.item.user_id:
		db_session.delete(picture)
		db_session.commit()
		return redirect(url_for('viewItem', category_id=picture.item.category_id, item_id=picture.item.id))
		print "hambamaba"
	else:
		return redirect(url_for('viewItem', category_id=picture.item.category_id, item_id=picture.item.id))
	return redirect(url_for('showCategory'))