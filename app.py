import requests
from flask import jsonify, request, Flask
from flask_cors import CORS
from _utils import get_data_by_city, get_data_by_zipcode

app = Flask(__name__)
CORS(app)
@app.route('/city',methods=["POST"])
def get_city_data():
    num_bedrooms = request.json.get('bedrooms')
    city = request.json.get('city')
    return get_data_by_city(num_bedrooms=num_bedrooms, city_name= city)
@app.route('/zipcode', methods=["POST"])
def get_zipcode_data():
    num_bedrooms = request.json.get('bedrooms')
    zipcode = request.json.get('zipcode')
    return get_data_by_zipcode(num_bedrooms=num_bedrooms, zipcode=zipcode)
