from etl.database import insert_all_asns_for_country
from etl.ripe_api import get_country_resource_list, get_country_resource_stats

ex_soviet_countries = {
    "AM": "Armenia", "AZ": "Azerbaijan", "BY": "Belarus", "EE": "Estonia", "GE": "Georgia", "KZ": "Kazakhstan",
    "KG": "Kyrgyzstan", "LV": "Latvia", "LT": "Lithuania", "MD": "Moldova", "RU": "Russia", "TJ": "Tajikistan",
    "TM": "Turkmenistan", "UA": "Ukraine", "UZ": "Uzbekistan"
}


def process_asns_of_ex_soviet_countries():
    for country_iso2 in ex_soviet_countries:
        print("Getting ASNs for {} ({})".format(ex_soviet_countries[country_iso2], country_iso2), end=" ... ")
        d = get_country_resource_list(country_iso2, copy_to_file=True)
        asn_list = d['data']['resources']['asn']
        print("{} ASNs found".format(len(asn_list)))

def process_stats_of_ex_soviet_countries():
    for country_iso2 in ex_soviet_countries:
        print("Getting historical stats for {} ({})".format(ex_soviet_countries[country_iso2], country_iso2), end=" ... ")
        d = get_country_resource_stats(country_iso2, '2014-01-01T12:00', copy_to_file=True)
        stats = d['data']['stats']
        print("Stats for {} days found".format(len(stats)))

    insert_all_asns_for_country(None, None)

def main():
    # process_asns_of_ex_soviet_countries()
    # process_stats_of_ex_soviet_countries()
    insert_all_asns_for_country(None, None)

if __name__ == "__main__":
    main()
