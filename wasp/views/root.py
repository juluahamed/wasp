from wasp. __init__ import app
from flask import render_template
from wasp.database import db_session
from wasp.models import Like, Picture, Item
from sqlalchemy import func

@app.route('/')
@app.route('/hot')
def showRoot():
	"""View function for '/' and '/hot' URL. Displays most liked 8 items"""
	most_liked = db_session.query(Like.item_id,func.count(Like.item_id).label('item_count')).group_by(Like.item_id).order_by('item_count DESC').limit(8).all()
	hot_items = [db_session.query(Item).filter_by(id=id[0]).one() for id in most_liked]
	final_items=[]
	for item in hot_items:
		picture = db_session.query(Picture.name).filter_by(item_id=item.id).order_by(Picture.id.desc()).first()
		if not picture:
			picture_name = "sample_image.jpg"
		else:
			picture_name= picture.name
		tmp = {
			'id': item.id,
			'category_id': item.category_id,
			'picture_name': picture_name,
			'name': item.name,
			'description': item.description,
			'time_created': item.time_created

		}
		final_items.append(tmp)
	return render_template('root.html', items=final_items) 
