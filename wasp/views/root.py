from wasp. __init__ import app, session
from flask import render_template
from wasp.database import db_session
from wasp.models import User

@app.route('/')
@app.route('/hot')
def showRoot():
	#q = User(name='kumaran', email='kumarappan@x.com', picture=' ')
	#db_session.add(q)
	#db_session.commit()
	a = db_session.query(User).all()
	return render_template('root.html', names=a)
