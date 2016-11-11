import json
from flask import jsonify, Blueprint, abort, g, make_response
from flask.ext.restful import (Resource, Api, reqparse, inputs, 
								fields, marshal, marshal_with,
								url_for)
from auth import auth
import models

company_fields = {
	'id': fields.Integer,
	'name': fields.String,
	'address': fields.String,
	'marinas': fields.List(fields.String)
}

#
def add_marinas(company):
	company.marinas = [url_for('resources.marinas.marina', id=marina.id)
						for marina in company.marinas]
	return company

#
def company_or_404(company_id):
	try:
		company = models.Company.get(models.Company.id==company_id)
	except models.Company.DoesNotExist:
		abort(404)
	else:
		return company


class CompanyList(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'name',
			required=True,
			help='No company name provided',
			location=['form', 'json']
		)
		self.reqparse.add_argument(
			'address',
			required=True,
			help='No company address provided',
			location=['form', 'json']
		)
		super().__init__()

	def get(self):
		companies = [marshal(add_marinas(company), company_fields)
					for company in models.Company.select()] # select all of the 
		# companies from the database and put it in companies
		return jsonify({'companies': companies})

	@marshal_with(company_fields)
	@auth.login_required
	def post(self):
		args = self.reqparse.parse_args()
		company = models.Company.create(
			created_by = g.user,
			**args
		)
		return add_marinas(company), 201, {'Location': url_for
				('resources.companies.company', id=company.id)}


class Company(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'name',
			required=True,
			help='No company name provided',
			location=['form', 'json']
		)
		self.reqparse.add_argument(
			'address',
			required=True,
			help='No company address provided',
			location=['form', 'json']
		)
		super().__init__()

	@marshal_with(company_fields)
	def get(self, id):
		return add_marinas(company_or_404(id)) 

	# update record
	@marshal_with(company_fields)
	@auth.login_required
	def put(self, id):
		args = self.reqparse.parse_args() # reqprase - parses arguments for us out of request
		try:
			company = models.Company.select().where(
				models.Company.created_by == g.user,
				models.Company.id == id
			).get()
		except models.Company.DoesNotExist:
			return make_response(json.dumps(
				{'error': 'That company doesnt exist or isnt editable' }
			), 403)

		query = models.Company.update(**args).where(models.Company.id==id)
		query.execute()
		return (add_marinas(models.Company.get(models.Company.id==id)), 200, 
				{'Location': url_for('resources.companies.company', id=id)})

	@auth.login_required
	def delete(self, id):
		query = models.Company.delete().where(models.Company.id==id)
		query.execute()
		#jsonify - turns what's in the parenthesis into a json response
		return ('', 204, {'Location': url_for('resources.companies.companies')})

# made the api blueprint
companies_api = Blueprint('resources.companies', __name__)

# created api
api = Api(companies_api)

# adding a resource to the api
# adding a CompanyList
# url is how to access it in the api
# endpoint to name it
api.add_resource(
	CompanyList,
	'/companies',
	endpoint='companies'
	)
api.add_resource(
	Company,
	'/companies/<int:id>',
	endpoint='company'
	)
