import itertools
from datetime import datetime, timedelta

from extract_from_cloudflare_api import get_cloudflare_traffic_for_country, get_cloudflare_internet_quality_for_country
from extract_from_ripe_api import get_country_asns, get_country_resource_stats, get_asn_neighbours


def get_list_of_asns_for_country(country_iso2, date_from, date_to, batch_size=25000, verbose=True):
    date = date_from
    asns_batch = []
    # rolling_line = itertools.cycle(['o', 'O'])

    while date <= date_to:
        d = get_country_asns(country_iso2, date, save_mode='file')
        # if verbose:
        #     print('\b' + next(rolling_line), end='')

        routed_asns = d['data']['countries'][0]['routed']
        non_routed_asns = d['data']['countries'][0]['non_routed']
        routed_list = [ item.split('(')[1].split(')')[0] for item in routed_asns.strip('{}').split(', ') if item.startswith("AsnSingle")]
        non_routed_list = [ item.split('(')[1].split(')')[0] for item in non_routed_asns.strip('{}').split(', ') if item.startswith("AsnSingle")]

        for asn in routed_list:
            asns_batch.append({'asn':asn, 'date':date.strftime("%Y-%m-%d"), 'is_routed' : True})
        for asn in non_routed_list:
            asns_batch.append({'asn':asn, 'date':date.strftime("%Y-%m-%d"), 'is_routed' : False})

        if len(asns_batch) >= batch_size:
            yield asns_batch, date
            asns_batch = []

        date += timedelta(days=1)


def get_stats_for_country(country_iso2, date_from, date_to, resolution):
    print(f"    Getting historical stats {country_iso2}, {resolution}, {date_from}, {date_to}", end=' ... ')
    d = get_country_resource_stats(country_iso2, resolution, date_from, date_to, save_mode='file')
    if d:
        stats = d['data']['stats']
        print(f"    {len(stats)} records found")
        return stats


def get_list_of_asn_neighbours_for_country(country_iso2, date_from, date_to, verbose=True):
    total_days = (date_to - date_from).days
    length = 50
    date = date_from

    while date <= date_to:
        if verbose:
            filled_length = int(length * (date - date_from).days // total_days)
            bar = '█' * filled_length + '-' * (length - filled_length)

        result = {}
        asn_list = get_list_of_asns_for_country(country_iso2, date, date, verbose=False) #save_mode
        if asn_list:
            counter=0
            for item in asn_list:
                asn=item['asn']
                counter+=1
                if verbose:
                    print(f'\r    Getting data from the API ... |{bar}| {date.strftime("%Y-%m-%d")}, asn {counter}/{len(asn_list)}', end='', flush=True)
                d = get_asn_neighbours(asn, date)
                result[(asn,date)] = d['data']['neighbours']

        date += timedelta(days=1)

    if verbose:
        print(f'\r    Getting data from the API ... |{bar}|  SUCCESS', end=' - ', flush=True)
        print(f"    Total records collected: {len(result)}")
    return result


def get_traffic_for_country(country_iso2, token):
    print(f"Getting traffic for {country_iso2}", end=" ... ")
    d = get_cloudflare_traffic_for_country(country_iso2, token, copy_to_file=True)
    if d:
        traffic = d['result']['main']
        print(f"{len(traffic['timestamps'])} records found")
        return traffic

def get_internet_quality_for_country(country_iso2, token):
    print(f"    Getting internet quality for {country_iso2}", end=" ... ")
    d = get_cloudflare_internet_quality_for_country(country_iso2, token, copy_to_file=True)
    if d:
        internet_quality = d['result']['main']
        print(f"{len(internet_quality['timestamps'])} records found")
        return internet_quality

