from wasp. __init__ import app, session
from flask import render_template
import random
import string

@app.route('/login')
def showLogin():
	"""View function returns the login page. Creates anti-forgery state token"""
	state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
	session['state'] = state
	return render_template('login.html', STATE=state)