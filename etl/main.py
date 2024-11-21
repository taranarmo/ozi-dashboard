import sys

from database import insert_country_asns_to_db, insert_country_stats_to_db
from country_lists import EX_SOVIET_COUNTRIES, REPORT_COUNTRIES
from ripe_api import get_country_resource_list, get_country_resource_stats

STATS_RESOLUTION = '1d'


def get_list_of_asns_for_country(country_iso2):
    print(f"Getting ASNs", end=" ... ")
    d = get_country_resource_list(country_iso2, copy_to_file=True)
    asn_list = d['data']['resources']['asn']
    print(f"{len(asn_list)} found")
    return asn_list


def get_stats_for_country(country_iso2, date_from, date_to, resolution):
    print(f"Getting historical stats {country_iso2}, {resolution}, {date_from}, {date_to}", end=' ... ')
    d = get_country_resource_stats(country_iso2, resolution, date_from, date_to, copy_to_file=True)
    stats = d['data']['stats']
    print(f"{len(stats)} records found")
    return stats


def main():
    task_map = {
            "task1": etl_task1_load_list_of_asns_for_country,
            "task2": etl_task2_load_1d_stats_for_country,
            "task3": etl_task3_load_5m_stats_for_country }

    if len(sys.argv) < 2:
        print("Error: No ETL task specified. Please provide 'task1', 'task2', or 'task3' as the first argument.")
        return

    task = sys.argv[1]
    if task not in task_map:
        print(f"Error: Unknown task '{task}'. Valid tasks are 'task1', 'task2', or 'task3'.")

    for iso2 in REPORT_COUNTRIES:
        print(f"\n{iso2} - {REPORT_COUNTRIES[iso2]}")
        task_map[task](iso2)
    print("Done")

def etl_task1_load_list_of_asns_for_country(iso2):
    asns = get_list_of_asns_for_country(iso2)
    insert_country_asns_to_db(iso2, asns, True)

def etl_task2_load_1d_stats_for_country(iso2):
    stats = get_stats_for_country(iso2, '2014-01-01', '2025-01-01', '1d')
    insert_country_stats_to_db(iso2, '1d', stats, True)

def etl_task3_load_5m_stats_for_country(iso2):
    for year in range(2019, 2025):
        stats = get_stats_for_country(iso2, f"{year}-01-01", f'{year + 1}-01-01', '5m')
        insert_country_stats_to_db(iso2, '5m', stats, True)


if __name__ == "__main__":
    main()
