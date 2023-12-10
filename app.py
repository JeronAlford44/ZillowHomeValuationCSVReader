import requests
from flask import jsonify, request, Flask
from flask_cors import CORS



import firebase_admin
from firebase_admin import credentials, storage
from datetime import datetime
import json


cred = credentials.Certificate("capstoneadmin-ae398-firebase-adminsdk-3ns45-cddae79f61.json")
firebase_admin.initialize_app(cred, {'storageBucket': 'capstoneadmin-ae398.appspot.com'})

class Data_Storage():
    def __init__(self) -> None:
        self.bucket = storage.bucket()

    def fetch_city_data(self, num_bedrooms: str, city_name: str):
        if not num_bedrooms or not city_name:
            return LookupError

        city_file_folder = f'data_by_city/cities{num_bedrooms}.json'
        request = self.bucket.blob(city_file_folder).download_as_text()
        json_data = json.loads(request)
        for city_dict in json_data:
            if city_dict.get('RegionName') == city_name:
                return city_dict
        

        return

    def fetch_zipcode_data(self, num_bedrooms: str, zipcode: str):
        if not num_bedrooms or not zipcode:
            return LookupError

        zipcode_file_folder = f'data_by_zipcode/zipcodes{num_bedrooms}.json'
        request = self.bucket.blob(zipcode_file_folder).download_as_text()
        json_data = json.loads(request)
        for zipcode_dict in json_data:
            if zipcode_dict.get('RegionName') == zipcode:
                return zipcode_dict
        

        return

    def filter_one_date_per_year(self, data: dict):
        try:
            # Assuming data is a JSON object with date-value pairs
           

            # Extract the year from each date and keep track of seen years
            seen_years = set()
            filtered_data = {}

            for date_str, value in data.items():
                try:
                    date_object = datetime.strptime(date_str, '%Y-%m-%d')
                    year = date_object.year

                    if year not in seen_years:
                        seen_years.add(year)
                        filtered_data[date_str] = value
                except ValueError:
                    # Ignore keys that are not valid dates
                    pass

            return json.dumps(filtered_data)

        except json.JSONDecodeError:
            # Handle JSON decoding error
            return None


# Example usage


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