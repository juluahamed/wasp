from wasp. __init__ import app
from flask import render_template

@app.route('/error404')
def errorNotFound():
	"""View function to return a custom Not Found page"""
	return render_template('errornotfound.html')
