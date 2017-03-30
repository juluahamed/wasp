from wasp. __init__ import app, session
from flask import render_template
from wasp.database import db_session
from wasp.models import User
import random
import string

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    session['state'] = state
    #return "The current session state is %s" % session['state']
    return render_template('login.html', STATE=state)