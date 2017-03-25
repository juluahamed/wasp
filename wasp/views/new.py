from wasp. __init__ import app
from flask import render_template
from wasp.database import db_session
from wasp.models import User, Category

@app.route('/new')
def New():
	#q = User(name='pranthan', email='killmadi@x.com')
	#db_session.add(q)
	#db_session.commit()

	#a = db_session.query(User).filter_by(id=1).one()
	#new_category = Category(name='Movie', user_id=a.id)
	#db_session.add(new_category)
	#db_session.commit()
	a = db_session.query(Category).all()
	return render_template('category.html', names=a)
