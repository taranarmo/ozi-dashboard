from datetime import datetime
from json import loads
import requests

api_url = 'https://stat.ripe.net/data/{}/data.json'

def save_data_to_file(data, name=None):
    filename = 'data/ripe_data_{}_{}.json'.format(name, datetime.now().strftime('%Y%m%d_%H%M%S'))
    with open(filename, 'w') as f:
        print(data, file=f)

def get_country_resource_list(country_iso2, copy_to_file=False):
    response = requests.get(api_url.format("country-resource-list"), {"resource": country_iso2})
    try:
        data = loads(response.text)
    except Exception as e:
        print("Exception during API request")
        return None
    if copy_to_file:
        save_data_to_file(data, "country_resource_list_{}".format(country_iso2))
    return data

def get_country_resource_stats(country_iso2, start_time, copy_to_file=False):
    response = requests.get(api_url.format("country-resource-stats"),
                            {"resource": country_iso2, "starttime": start_time, "resolution": "5m"})
    try:
        data = loads(response.text)
    except Exception as e:
        print("Exception during API request")
        return None
    if copy_to_file:
        save_data_to_file(data, "country_resource_list_{}".format(country_iso2))
    return data