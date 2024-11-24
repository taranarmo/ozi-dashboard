from cloudflare_api import get_cloudflare_traffic_for_country
from ripe_api import get_country_resource_list, get_country_resource_stats

def get_list_of_asns_for_country(country_iso2):
    print(f"Getting ASNs", end=" ... ")
    d = get_country_resource_list(country_iso2, copy_to_file=True)
    asn_list = d['data']['resources']['asn']
    print(f"{len(asn_list)} found")
    return asn_list


def get_stats_for_country(country_iso2, date_from, date_to, resolution):
    print(f"Getting historical stats {country_iso2}, {resolution}, {date_from}, {date_to}", end=' ... ')
    d = get_country_resource_stats(country_iso2, resolution, date_from, date_to, copy_to_file=True)
    if d:
        stats = d['data']['stats']
        print(f"{len(stats)} records found")
        return stats


def get_list_of_asn_neighbours_for_country(country_iso2):
    print(f"Getting ASN neighbours", end=" ... ")
    print("not implemented")

def get_traffic_for_country(country_iso2, token):
    print(f"Getting traffic for {country_iso2}", end=" ... ")
    d = get_cloudflare_traffic_for_country(country_iso2, token, copy_to_file=True)
    if d:
        traffic = d['result']['main']
        print(f"{len(traffic['timestamps'])} records found")
        return traffic
