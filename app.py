from flask import Flask 
from flask import render_template
import config
import models
from resources.companies import companies_api
from resources.marinas import marinas_api
from resources.users import users_api

app = Flask(__name__)
app.register_blueprint(companies_api, url_prefix='/api/v1')
app.register_blueprint(marinas_api, url_prefix='/api/v1')
app.register_blueprint(users_api, url_prefix='/api/v1')


@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')




if __name__ == '__main__':
	models.initialize()
	app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT) #, port=8000, host=0.0.0.0)

#course=company
#reviews=marinas
