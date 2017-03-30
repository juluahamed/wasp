from wasp.__init__ import app, session
from flask import request, render_template, make_response, redirect,flash
import httplib2
import json

@app.route('/gdisconnect')
def gdisconnect():
	access_token = session.get('access_token')
	uname = session.get('username')
	print uname
	print access_token;
	if not access_token:
		response = make_response(
			json.dumps('Current user not connected.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
	h = httplib2.Http()
	result = h.request(url, 'GET')[0]

	if result['status'] != '200':
		# For whatever reason, the given token was invalid.
		response = make_response(
			json.dumps('Failed to revoke token for given user.'), 400)
		response.headers['Content-Type'] = 'application/json'
		[session.pop(k, None) for k, _ in session.items()]
		return response
	#Clearing out session data
	[session.pop(k, None) for k, _ in session.items()]
	return redirect(request.referrer)