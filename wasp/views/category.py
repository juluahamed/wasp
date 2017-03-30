from wasp. __init__ import app, session
from flask import render_template
from wasp.database import db_session
from wasp.models import User, Category

@app.route('/category')
def showCategory():
	categories = db_session.query(Category).all()
	return render_template('category.html', categories=categories)
