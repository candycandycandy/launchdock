from flask import Flask, g, jsonify
from auth import auth
from flask import render_template
from flask_limiter import Limiter
from flask_limiter.util import get_ipaddr

import config
import models
from resources.companies import companies_api
from resources.marinas import marinas_api
from resources.users import users_api

app = Flask(__name__)
app.register_blueprint(companies_api, url_prefix='/api/v1')
app.register_blueprint(marinas_api, url_prefix='/api/v1')
app.register_blueprint(users_api, url_prefix='/api/v1')

limiter = Limiter(app, global_limits=[config.DEFAULT_RATE], key_func=get_ipaddr)
limiter.limit('40/day')(users_api)
limiter.limit(config.DEFAULT_RATE, per_method=True,
							methods=['post', 'put', 'delete'](companies_api)
# limiter.exempt(companies_api)
# limiter.exempt(marinas_api)

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/api/v1/users/token', methods=['GET'])
@auth.login_required
def get_auth_token():
	token = g.user.generate_auth_token()
	return jsonify({'token': token.decode('ascii')})


if __name__ == '__main__':
	models.initialize()
	app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT) #, port=8000, host=0.0.0.0)

#course=company
#reviews=marinas