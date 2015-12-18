###author: Spurthi Amba Hombaiah
###Web application for language identifier. Making HTTP POST requests to the appliction.

from flask import Flask
from flask_restful import reqparse, Api, Resource
from flask.views import MethodView
from language_identifier import Language_identifier
import json

app = Flask(__name__)
lang_id_api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('text')

class LangDetector(MethodView):
	def get(self):
		return self

	def post(self):
		args = parser.parse_args()
		li = Language_identifier()
		language, distance = li.driver(args['text'])
		l_dict = dict()
		l_dict[language] = distance
		return l_dict
        
lang_id_api.add_resource(LangDetector, '/lang_id')

if __name__ == '__main__':
    app.run(debug=True)

