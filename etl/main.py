from database import insert_country_asns_to_db, insert_country_stats_to_db
from ripe_api import get_country_resource_list, get_country_resource_stats

EX_SOVIET_COUNTRIES = {
    "AM": "Armenia", "AZ": "Azerbaijan", "BY": "Belarus", "EE": "Estonia", "GE": "Georgia", "KZ": "Kazakhstan",
    "KG": "Kyrgyzstan", "LV": "Latvia", "LT": "Lithuania", "MD": "Moldova", "RU": "Russia", "TJ": "Tajikistan",
    "TM": "Turkmenistan", "UA": "Ukraine", "UZ": "Uzbekistan"
}


def get_list_of_asns_for_country(country_iso2):
    print(f"Getting ASNs for {EX_SOVIET_COUNTRIES[country_iso2]} ({country_iso2})", end=" ... ")
    d = get_country_resource_list(country_iso2, copy_to_file=True)
    asn_list = d['data']['resources']['asn']
    print("{} ASNs found".format(len(asn_list)))
    return asn_list

def get_stats_for_country(country_iso2):
    print(f"Getting historical stats for {EX_SOVIET_COUNTRIES[country_iso2]} ({country_iso2})", end=" ... ")
    d = get_country_resource_stats(country_iso2, '2014-01-01T12:00', copy_to_file=True)
    stats = d['data']['stats']
    print("Stats for {} days found".format(len(stats)))
    return stats


def main():
    for iso2 in EX_SOVIET_COUNTRIES:
        asns = get_list_of_asns_for_country(iso2)
        insert_country_asns_to_db(iso2, asns, True)

        stats = get_stats_for_country(iso2)
        insert_country_stats_to_db(iso2, stats, True)
    print("Done")

if __name__ == "__main__":
    main()
