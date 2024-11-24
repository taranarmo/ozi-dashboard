from datetime import datetime
from json import loads
import requests

API_URL = 'https://stat.ripe.net/data/{}/data.json'
RETRIES = 5

def save_data_to_file(data, name=None):
    filename = 'data/ripe_data_{}_{}.json'.format(name, datetime.now().strftime('%Y%m%d_%H%M%S'))
    with open(filename, 'w') as f:
        print(data, file=f)


def get_country_resource_list(country_iso2, copy_to_file=False):
    url = API_URL.format("country-resource-list")
    params = {"resource": country_iso2}
    data = ripe_api_call(url, params)

    if copy_to_file:
        save_data_to_file(data, f"country_resource_list_{country_iso2}")
    return data


def get_country_resource_stats(country_iso2, resolution, start_time, end_time, copy_to_file=False):
    url = API_URL.format("country-resource-stats")
    params = {"resource": country_iso2, "starttime": start_time, "endtime": end_time, "resolution": resolution}
    data = ripe_api_call(url, params)

    if copy_to_file:
        save_data_to_file(data, f"country_resource_stats_{country_iso2}_{resolution}_{start_time}_{end_time}")
    return data

def get_asn_neighbours(asn, copy_to_file=False):
    url = API_URL.format("asn-neighbours")
    params = {"resource": asn}
    data = ripe_api_call(url, params)

    if copy_to_file:
        save_data_to_file(data, f"asn-neighbours_{asn}")
    return data


def ripe_api_call(url, params):
    attempts_left = RETRIES
    while attempts_left > 0:
        response = requests.get(url, params)
        try:
            data = loads(response.text)
            if data:
                return data
        except Exception as e:
            print("Exception during API request" + "... retrying" if attempts_left else "... STOP")
    return None
