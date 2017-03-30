from wasp. __init__ import app, session
from flask import render_template
from wasp.database import db_session
from wasp.models import Item, Picture

@app.route('/category/<int:category_id>/item/<int:item_id>')
@app.route('/category/<int:category_id>/item/<int:item_id>/view')
def viewItem(category_id, item_id):
	item = db_session.query(Item).filter_by(id=item_id).one()
	picture = db_session.query(Picture.name).filter_by(item_id=item.id).order_by(Picture.id.desc()).first()
	if picture is None:
		picture="sample_image.png"
	else:
		picture= picture[0]

	print picture
	return render_template('viewitem.html', item=item, picture=picture)