from wasp. __init__ import app, session
from flask import render_template, jsonify
from wasp.database import db_session
from wasp.models import Category

# JSON endpoint for retrieving different categories
@app.route('/category/JSON')
def showCategoryJSON():
	categories = db_session.query(Category).all()
	return jsonify(Categories=[c.serialize for c in categories])



@app.route('/category')
def showCategory():
	""" View function for showing different categories"""
	categories = db_session.query(Category).all()
	return render_template('category.html', categories=categories)
