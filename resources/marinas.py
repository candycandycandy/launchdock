from flask import jsonify, Blueprint
from flask.ext.restful import (Resource, Api, reqparse, inputs, 
								fields, marshal, marshal_with,
								url_for)
import models


marina_fields = {
	'id': fields.Integer,
	'name': fields.String,
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
	def post(self):
		args = self.reqparse.parse_args()
		marina = models.Marina.create(**args)
		return add_company(marina)


class Marina(Resource):
	def get(self, id):
		return jsonify({'name': 'Snug Harbor South', 'company': 1}) #jsonify - turns what's in the parenthesis into a json response

	def put(self, id):
		return jsonify({'name': 'Snug Harbor South', 'company': 1})

	def delete(self, id):
		return jsonify({'name': 'Snug Harbor South', 'company': 1})

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

