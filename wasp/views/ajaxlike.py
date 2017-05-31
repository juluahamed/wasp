from wasp. __init__ import app, session
from flask import request
from wasp.database import db_session
from wasp.models import Like
from wasp.wasp_utils import login_required


@app.route('/ajaxlike', methods=['POST'])
@login_required
def ajaxLike():
	""" Ajax request handler for validating and updating database for likes on items"""
	if request.method == 'POST':
		new_like = Like(category_id= request.json['category_id'], item_id= request.json['item_id'], user_id=request.json['user_id'] )
		if request.json['status'] != "None":
			exsisting_like = db_session.query(Like).filter_by(category_id= request.json['category_id'], item_id= request.json['item_id'], user_id=request.json['user_id']).first()
			db_session.delete(exsisting_like)
			db_session.commit()
			return 'Deleted'
		db_session.add(new_like)
		db_session.commit()
		return 'Liked'