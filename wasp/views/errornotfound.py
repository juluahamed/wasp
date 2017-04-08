from wasp. __init__ import app, session
from flask import request, redirect, flash, url_for,render_template

@app.route('/error404')
def errorNotFound():
	return render_template('errornotfound.html')
