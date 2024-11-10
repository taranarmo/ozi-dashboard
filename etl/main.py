from database import insert_country_asns_to_db, insert_country_stats_to_db
from ripe_api import get_country_resource_list, get_country_resource_stats

EX_SOVIET_COUNTRIES = {
    "AM": "Armenia", "AZ": "Azerbaijan", "BY": "Belarus", "EE": "Estonia", "GE": "Georgia", "KZ": "Kazakhstan",
    "KG": "Kyrgyzstan", "LV": "Latvia", "LT": "Lithuania", "MD": "Moldova", "RU": "Russia", "TJ": "Tajikistan",
    "TM": "Turkmenistan", "UA": "Ukraine", "UZ": "Uzbekistan"
}

STATS_RESOLUTION = '1d'

def get_list_of_asns_for_country(country_iso2):
    print(f"Getting ASNs", end=" ... ")
    d = get_country_resource_list(country_iso2, copy_to_file=True)
    asn_list = d['data']['resources']['asn']
    print("{} found".format(len(asn_list)))
    return asn_list

def get_stats_for_country(country_iso2):
    print("Getting historical stats", end=' ... ')
    d = get_country_resource_stats(country_iso2, STATS_RESOLUTION, '2014-01-01T12:00', copy_to_file=True)
    stats = d['data']['stats']
    print("stats for {} days found".format(len(stats)))
    return stats


def main():
    for iso2 in EX_SOVIET_COUNTRIES:
        print(f"\n{iso2} - {EX_SOVIET_COUNTRIES[iso2]}")
        asns = get_list_of_asns_for_country(iso2)
        insert_country_asns_to_db(iso2, asns, True)

        stats = get_stats_for_country(iso2)
        insert_country_stats_to_db(iso2, STATS_RESOLUTION, stats, True)
    print("Done")

if __name__ == "__main__":
    main()
