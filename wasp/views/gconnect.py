from wasp.__init__ import app, session
from flask import request, render_template, make_response, redirect,flash
from wasp.database import db_session
from wasp.models import User
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError 
import json
import httplib2
import requests

CLIENT_ID = json.loads(
	open('/vagrant/wasp/wasp/client_secrets.json', 'r').read())['web']['client_id']

@app.route('/gconnect', methods=['POST'])
def gconnect():
	"""View function to handle google authentication via Oauth2"""
	
	# Check if state token recieved is valid
	if request.args.get('state') != session['state']:
		response = make_response(json.dumps('Invalid state parameters'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	# Obtain auth code send via ajax
	code = request.data

	# Update authorization code in to a credential object
	try:
		oauth_flow = flow_from_clientsecrets('/vagrant/wasp/wasp/client_secrets.json', scope='')
		oauth_flow.redirect_uri = 'postmessage'
		credentials = oauth_flow.step2_exchange(code)
	except FlowExchangeError:
		response = make_response(json.dumps('Failed toupgrade authorization code'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Check access_token is valid
	access_token = credentials.access_token
	url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' %access_token)
	h = httplib2.Http()
	result = json.loads(h.request(url, 'GET')[1])

	# If error in access_token info
	if result.get('error') is not None:
		response = make_response(json.dumps(result.get('error')), 500)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Verify access token is used for intended user
	g_id = credentials.id_token['sub']
	if result['user_id'] != g_id:
		response = make_response(json.dumps("Token's user ID doesn't match given user ID."), 401)
		#print "Token's client ID does not match app's."
		response.headers['Content-Type'] = 'application/json'
		return response

	# Verify token is valid for this client/app
	if result['issued_to'] != CLIENT_ID:
		response = make_response(json.dumps("Token's client ID doesnt match that of app"), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	#session['access_token'] = credentials.access_token
	stored_credentials = session.get('credentials')
	stored_g_id = session.get('g_id')
	if stored_credentials is not None and stored_g_id == g_id:
		response = make_response(json.dumps('Current user already connected'), 200)
		return response

	# Store the access token for later use
	session['access_token'] = credentials.access_token
	session['g_id'] = g_id
	#session['credentials'] = credentials

	# Get user info 
	userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
	params = {'access_token': credentials.access_token, 'alt': 'json'}
	answer = requests.get(userinfo_url, params=params)

	data =answer.json()

	session['username'] = data['name']
	session['picture'] = data['picture']
	session['email'] = data['email']
	session['provider'] = 'google'

	user_id = getUserID(session['email'])
	if not user_id:
		user_id = createUser(session)
	session['user_id'] = user_id

	flash("You are now logged in as %s" % session['username'])
	output = "Login successful"
	return output


# Helper functions

def createUser(session):
	newUser = User(name=session['username'], email=session['email'],
					 picture=session['picture'])
	db_session.add(newUser)
	db_session.commit()
	user = db_session.query(User).filter_by(email=session['email']).one()
	return user.id


def getUserInfo(user_id):
    user = db_session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = db_session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None





