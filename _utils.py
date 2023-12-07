import csv
import os
from os import listdir
from os.path import isfile, join
import json

city_files = [join('_city', f) for f in sorted(listdir('_city')) if isfile(join('_city', f))]
zipcode_files= [join('_zipcode', f) for f in sorted(listdir('_zipcode')) if isfile(join('_zipcode', f))]
def get_data_by_city(num_bedrooms: str, city_name: str):
    """Finds the CSV file matching the number of bedrooms in '_city' folder and returns a JSON object: 
     
       with average home price in that city"""
    for fileName in city_files:
        if fileName == f'_city/City_zhvi_bdrmcnt_{num_bedrooms}_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv':
            valueFound = False
          
            with open(fileName, mode='r') as csvfile:
                for lines in csv.DictReader(csvfile):
                    if lines.get('RegionName') == city_name.title():
                        valueFound = True
                        try:
                            res = float(lines.get('2023-10-31'))
                            city = lines.get('RegionName')
                            state = lines.get('State')
                            metro: lines.get('Metro')
                            county_name:  lines.get('CountyName')
                            return json.dumps({"price": (round(res, 2)), "city":city, "state": state, "metro": metro, "countyName": county_name})
                        except ValueError as e:
                            print(f"Error converting value to float: {e}")
                if not valueFound:
                 
                    return f"Error: City Not Found"
                    # else:
                    #     # You may not need this else block, depending on your requirements
                    #     print(lines.get('RegionName'))


def get_data_by_zipcode(num_bedrooms:str,zipcode: str):
    for fileName in zipcode_files:
        if fileName == f'_zipcode/Zip_zhvi_bdrmcnt_{num_bedrooms}_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv':
            valueFound = False
          
            with open(fileName, mode='r') as csvfile:
         
                for lines in csv.DictReader(csvfile):
                    
                    if lines.get('RegionName') == zipcode.title():
                        valueFound = True
                        try:
                            res = float(lines.get('2023-10-31'))
                            city = lines.get('City')
                            state = lines.get('State')
                            metro = lines.get('Metro')
                            county_name= lines.get('CountyName')
                            return json.dumps({'price': (round(res, 2)), 'city': city, 'state': state, 'metro': metro, 'countyName': county_name})
                        except ValueError as e:
                            print(json.dumps({"Error": f"Error converting value to float: {e}"}))
                if not valueFound:
                 
                    return f"Error: City Not Found"
                    # else:
                    #     # You may not need this else block, depending on your requirements
                    #     print(lines.get('RegionName'))
