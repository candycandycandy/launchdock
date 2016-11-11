from flask import jsonify, Blueprint
from flask.ext.restful import (Resource, Api, reqparse, inputs, 
								fields, marshal, marshal_with,
								url_for)
from auth import auth
import models

marina_fields = {
	'id': fields.Integer,
	'name': fields.String,
	'address': fields.String,
	'for_company': fields.String,
	'marinas': fields.List(fields.String)
}



def add_company(marina):
	marina.for_company = [url_for('resources.companies.company', id=marina.company.id)]
	return marina

def marina_or_404(marina_id):
	try:
		marina = models.Marina.get(models.Marina.id==marina_id)
	except models.Marina.DoesNotExist:
		abort(404)
	else:
		return marina

class MarinaList(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'name',
			required=True,
			help='No marina name provided',
			location=['form', 'json']
		)
		self.reqparse.add_argument(
			'address',
			required=True,
			help='No marina address provided',
			location=['form', 'json']
		)
		self.reqparse.add_argument(
			'company',
			required=True, 
			# nullable=True
			# type = inputs.positive/float
			# default=''
			help='No marina company provided',
			location=['form', 'json']
		)
		super().__init__()

	def get(self):
		marinas = [marshal(add_company(marina), marina_fields)
					for marina in models.Marina.select()] # select all of the 
		# marinas from the database and put it in marinas
		return jsonify({'marinas': marinas})

	@marshal_with(marina_fields)
	@auth.login_required
	def post(self):
		args = self.reqparse.parse_args()
		marina = models.Marina.create(**args)
		return add_company(marina), 201, {'Location': url_for
				('resources.marinas.marina', id=marina.id)}


class Marina(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'name',
			required=True,
			help='No marina name provided',
			location=['form', 'json']
		)
		self.reqparse.add_argument(
			'company',
			required=True, 
			# nullable=True
			# type = inputs.positive/float
			# default=''
			help='No marina company provided',
			location=['form', 'json']
		)
		super().__init__()

	@marshal_with(marina_fields)
	def get(self, id):
		return add_company(marina_or_404(id)) 

	# update record
	@marshal_with(marina_fields)
	@auth.login_required
	def put(self, id):
		args = self.reqparse.parse_args() # reqprase - parses arguments for us out of request
		query = models.Marina.update(**args).where(models.Marina.id==id)
		query.execute()
		#jsonify - turns what's in the parenthesis into a json response
		return (add_marinas(models.Marina.get(models.Marina.id==id)), 200, 
				{'Location': url_for('resources.marinas.marina', id=id)})

	@auth.login_required
	def delete(self, id):
		query = models.Marina.delete().where(models.Marina.id==id)
		query.execute()
		#jsonify - turns what's in the parenthesis into a json response
		return ('', 204, {'Location': url_for('resources.marinas.marinas')})

# made the api blueprint
marinas_api = Blueprint('resources.marinas', __name__)

# created api
api = Api(marinas_api)

# adding a resource to the api
# adding a CompanyList
# url is how to access it in the api
# endpoint to name it
api.add_resource(
	MarinaList,
	'/marinas',
	endpoint='marinas'
	)
api.add_resource(
	Marina,
	'/marinas/<int:id>',
	endpoint='marina'
	)

