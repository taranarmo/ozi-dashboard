from database import insert_country_asns_to_db, insert_country_stats_to_db
from country_lists import EX_SOVIET_COUNTRIES, REPORT_COUNTRIES
from ripe_api import get_country_resource_list, get_country_resource_stats

STATS_RESOLUTION = '1d'

def get_list_of_asns_for_country(country_iso2):
    print(f"Getting ASNs", end=" ... ")
    d = get_country_resource_list(country_iso2, copy_to_file=True)
    asn_list = d['data']['resources']['asn']
    print("{} found".format(len(asn_list)))
    return asn_list


def get_stats_for_country(country_iso2, date_from, date_to, resolution):
    print("Getting historical stats", end=' ... ')
    d = get_country_resource_stats(country_iso2, resolution, '2014-01-01T12:00', copy_to_file=True)
    stats = d['data']['stats']
    print("stats for {} days found".format(len(stats)))
    return stats


def main():
    for iso2 in REPORT_COUNTRIES:
        print(f"\n{iso2} - {REPORT_COUNTRIES[iso2]}")
        asns = get_list_of_asns_for_country(iso2)
        insert_country_asns_to_db(iso2, asns, True)

        print(f"getting 1d stats for {iso2}".format(iso2=iso2))
        stats = get_stats_for_country(iso2, '2014-01-01', '2025-01-01', '1d')
        insert_country_stats_to_db(iso2, '1d', stats, True)

        for year in range(2019, 2025):
            print("getting stats for year {}".format(year))
            date_from = f"{year}-01-01".format(year=year)
            date_to = f'{year + 1}-01-01'.format(year=year)

            stats = get_stats_for_country(iso2, date_from, date_to, '5m')
            insert_country_stats_to_db(iso2, '5m', stats, True)
    print("Done")

if __name__ == "__main__":
    main()
