import requests
from flask import jsonify, request, Flask
from flask_cors import CORS

from data_class import Data_Storage

app = Flask(__name__)
CORS(app)
Model = Data_Storage()
@app.route('/')
def index():
    return jsonify({"hello": 'world'})
@app.route('/city',methods=["POST"])
def get_city_data():
    num_bedrooms = request.json.get('bedrooms')
    city = request.json.get('city')
    city_data =Model.fetch_city_data(num_bedrooms=num_bedrooms, city_name= city)
    filtered_city_data = Model.filter_one_date_per_year(city_data)
    return filtered_city_data
@app.route('/zipcode', methods=["POST"])
def get_zipcode_data():
    num_bedrooms = request.json.get('bedrooms')
    zipcode = request.json.get('zipcode')
    zipcode_data = Model.fetch_zipcode_data(num_bedrooms=num_bedrooms, zipcode=zipcode)
    filtered_zipcode_data = Model.filter_one_date_per_year(zipcode_data)
    return filtered_zipcode_data
if __name__ == '__main__':
    app.run(debug=True)