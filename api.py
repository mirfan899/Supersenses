from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_restful import reqparse
from helpers import *

app = Flask(__name__)
api = Api(app, prefix="/api/v1")

parser = reqparse.RequestParser()
parser.add_argument("sentence", type=str, help="sentence or words should be unicode text", location='form')


class Supersenses(Resource):
    def get(self):
        return {"message": "Welcome to SupersensesAPI.", "status": 200}

    def post(self):
        args = parser.parse_args()

        text = args["sentence"]
        if text:
            return jsonify(get_supersenses(text))
        else:
            return {"sentence parameter is missing": 404}


api.add_resource(Supersenses, "/supersenses")

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')
