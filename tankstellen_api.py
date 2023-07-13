from enum import Enum
from geopy.geocoders import Nominatim
import requests
import pandas as pd

TANKERKOENIG_API_KEY = st.secrets["TANKERKOENIG_API_KEY"]
USER_AGENT = "studentproject_spritpreise"
ENABLED = True

sprittypes = {
    "Diesel" : "diesel",
    "Super E10" : "e10",
    "Super E5" : "e5"
}

def get_SpritType_From_SelectionText(selectionText):
    return sprittypes.get(selectionText)


def get_all_tankstellen_in_specific_radius_json(place_string, search_radius:int, sprit_type):
    if(ENABLED == False):
        return
    sort_type = "price"
    sprit_type = get_SpritType_From_SelectionText(sprit_type)
    geocode = place_to_geocode(place_string)
    if geocode is None:
        return None
    ## API Call
    station_radius_api_url = "https://creativecommons.tankerkoenig.de/json/list.php?lat={}&lng={}&rad={}&sort={}&type={}&apikey={}".format(geocode["latitude"], geocode["longitude"], search_radius, sort_type, sprit_type, TANKERKOENIG_API_KEY)
    print(station_radius_api_url)
    response = requests.get(station_radius_api_url)
    json_data = response.json()
    df = pd.json_normalize(json_data, 'stations')
    return df

def place_to_geocode(placestring):
    geolocator = Nominatim(user_agent=USER_AGENT)
    location = geolocator.geocode(placestring)
    if location is None:
        return None
    return {
        "latitude": str(location.latitude),
        "longitude": str(location.longitude)
    }

### Not used APIS

def get_prices_from_specific_tankstellen_json(tankstellen_id_list):
    tankstellen_ids_string = ""
    for id in tankstellen_id_list:
        tankstellen_ids_string += "{},".format(id)
    tankstellen_ids_string = tankstellen_ids_string[:-1]
    ## API Call
    prices_api_url = "https://creativecommons.tankerkoenig.de/json/prices.php?ids={}&apikey={}".format(tankstellen_ids_string, TANKERKOENIG_API_KEY)
    response = requests.get(prices_api_url)
    json_data = response.json
    return json_data

def get_details_to_a_specifix_tankstelle_json(id):
    details_url = "https://creativecommons.tankerkoenig.de/json/detail.php?id={}&apikey={}".format(id,TANKERKOENIG_API_KEY)
    response = requests.get(details_url)
    json_data = response.json()
    return json_data
