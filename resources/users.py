from flask import jsonify, Blueprint, abort, make_response, json
from flask.ext.restful import (Resource, Api, reqparse, inputs, 
								fields, marshal, marshal_with,
								url_for)
import models

user_fields = {
	'username': fields.String
}

class UserList(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'username',
			required=True,
			help='No user name provided',
			location=['form', 'json']
		)
		self.reqparse.add_argument(
			'password',
			required=True,
			help='No password provided',
			location=['form', 'json']
		)
		self.reqparse.add_argument(
			'verify_password',
			required=True,
			help='No password verifiation provided',
			location=['form', 'json']
		)
		self.reqparse.add_argument(
			'email',
			required=True,
			help='No email provided',
			location=['form', 'json']
		)
		super().__init__()

	def post(self):
		args = self.reqparse.parse_args()
		if args.get('password') == args.get('verify_password'):
			user = models.User.create_user(**args)
			return marshal(user, user_fields), 201
		return make_response(
			json.dumps({
				'error': 'Password and password verification do not match'}), 400)

# made the api blueprint
users_api = Blueprint('resources.users', __name__)

# created api
api = Api(users_api)

# adding a resource to the api
# adding a CompanyList
# url is how to access it in the api
# endpoint to name it
api.add_resource(
	UserList,
	'/users',
	endpoint='users'
)
# api.add_resource(
# 	User,
# 	'/users/<int:id>',
# 	endpoint='user'
# 	)
