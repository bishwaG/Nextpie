## decorative for api token

from functools import wraps
from flask import request
from app.base.models import User


## Function for token validation (checking againset the User.key database column)
def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):

		token = None

		if 'X-API-KEY' in request.headers:
	    		token = request.headers['X-API-KEY']

		if not token:
	    		return {'message' : 'Unauthorized access (missing token).'}, 403

		record = User.query.filter_by(key=token).first()

		#if token != 'mytoken':
		if not record:
	    		return {'message' : 'Your token is wrong, wrong, wrong!!!'}, 401
		elif not record.enable_api:
			return {'message' : 'User does not have API access!!!'}, 401
			
		#print('TOKEN: {}'.format(token))
		return f(*args, **kwargs)

	return decorated
