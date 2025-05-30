import os
import json
import re

import requests


def get_address_pincode_from_lat_long(lat, lng):
    lat = str(lat)
    lng = str(lng)
    KEY = os.getenv("GMAPS_KEY")
    try:
        resp = requests.get(
            f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={KEY}"
        ).text
        print(
            f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={KEY}"
        )
        resp = json.loads(resp)
        if "results" in resp:
            result = resp["results"][0]
            message = result["formatted_address"]
            pincode = int(re.findall("[0-9]{6}", message)[0])
            return pincode, message
    except Exception as ignored:
        return None, None


if __name__ == "__main__":
    print(get_address_pincode_from_lat_long("17.4477236", "78.3656206"))
