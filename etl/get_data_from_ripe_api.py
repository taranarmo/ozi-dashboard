from datetime import datetime
from json import loads

import requests


def get_data(*argl, **argd):
    try:
        req = requests.get(*argl, **argd)
    except Exception as e:
        print("Error")
        return False
    if req.status_code != 200:
        print("Error")
        return False
    return req

def country_resource_stats(resource=None, starttime=None, endtime=None, resolution=None):
    url = 'https://stat.ripe.net/data/country-resource-stats/data.json'
    params = {"resource": resource}
    if starttime is not None:
        params['starttime'] = starttime
    if endtime is not None:
        params['endtime'] = endtime
    if resolution is not None:
        params['resolution'] = resolution
    req = get_data(url, params)
    if req:
        try:
            list_ = loads(req.text)['data']['stats']
        except Exception as e:
            print("Error")
            return False
    else:
        return False
    return list_


country_code = 'RU'
resolution = '1d'
starttime = '2020-02-01'
endtime = '2024-02-01'
print_response = False

resource_stats = country_resource_stats(resource=country_code, starttime=starttime, endtime=endtime, resolution=resolution)

def save_data_to_csv(data=None, filename= ''):
    if not data:
        return False
    if not filename:
        filename = 'ripe_data_{}.csv'.format(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))

      
# print(resource_stats)
print("done")