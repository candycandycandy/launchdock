from flask import Flask 
from flask import render_template
import models
from resources.companies import companies_api
from resources.marinas import marinas_api


DEBUG = True
HOST ='0.0.0.0'
PORT = 8000

app = Flask(__name__)
app.register_blueprint(companies_api, url_prefix='/api/v1')
app.register_blueprint(marinas_api, url_prefix='/api/v1')


@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')




if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, host=HOST, port=PORT) #, port=8000, host=0.0.0.0)

#course=company
#reviews=marinas
