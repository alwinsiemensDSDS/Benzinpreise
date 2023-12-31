from geopy.geocoders import Nominatim
import requests
import pandas as pd
import streamlit as st

TANKERKOENIG_API_KEY = st.secrets["TANKERKOENIG_API_KEY"]
USER_AGENT = st.secrets["GEOPY_USERAGENT"]
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
