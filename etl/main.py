import sys
from database import insert_country_asns_to_db, insert_country_stats_to_db, insert_traffic_for_country_to_db, \
    insert_internet_quality_for_country_to_db
from etl.country_lists import REPORT_COUNTRIES
from etl.etl_jobs import get_internet_quality_for_country

from etl_jobs import get_list_of_asns_for_country, get_stats_for_country, get_list_of_asn_neighbours_for_country, \
    get_traffic_for_country

CLOUDFLARE_API_TOKEN=None

def main():
    task_map = {
            "task1": etl_task1_load_list_of_asns_for_country,
            "task2": etl_task2_load_1d_stats_for_country,
            "task3": etl_task3_load_5m_stats_for_country,
            "task4": etl_task4_load_asn_neighbours_for_country,
            "task5": etl_task5_load_traffic_for_country,
            "task6": etl_task6_load_internet_quality_for_country
    }

    if len(sys.argv) < 2:
        print("Error: No ETL task specified. Please provide 'task1', 'task2', or 'task3' as the first argument.")
        return

    api_token=None
    task = sys.argv[1]
    if task not in task_map:
        print(f"Error: Unknown task '{task}'. Valid tasks are 'task1', 'task2', or 'task3'.")
        return
    if task in ("task5", "task6"):
        if len(sys.argv) < 3:
            print("Error: No Cloudflare API token specified. Please provide the token as a second argument.")
            return
        api_token=sys.argv[2]

    for iso2 in REPORT_COUNTRIES:
        print(f"\n{iso2} - {REPORT_COUNTRIES[iso2]}")
        task_map[task](iso2, api_token)
    print("Done")

def etl_task1_load_list_of_asns_for_country(iso2, api_token=None):
    asns = get_list_of_asns_for_country(iso2)
    if asns:
        insert_country_asns_to_db(iso2, asns, True)

def etl_task2_load_1d_stats_for_country(iso2, api_token=None):
    stats = get_stats_for_country(iso2, '2014-01-01', '2025-01-01', '1d')
    if stats:
        insert_country_stats_to_db(iso2, '1d', stats, True)

def etl_task3_load_5m_stats_for_country(iso2, api_token=None):
    for year in range(2019, 2025):
        stats = get_stats_for_country(iso2, f"{year}-01-01", f'{year + 1}-01-01', '5m')
        if stats:
            insert_country_stats_to_db(iso2, '5m', stats, True)

def etl_task4_load_asn_neighbours_for_country(iso2, api_token=None):
    asn_neighbours = get_list_of_asn_neighbours_for_country(iso2)
    if asn_neighbours:
        # insert_country_asn_neighbours_to_db(iso2, asn_neighbours, True)
        print('not implemented')

def etl_task5_load_traffic_for_country(iso2, api_token=None):
    traffic=get_traffic_for_country(iso2, api_token)
    if traffic:
        insert_traffic_for_country_to_db(iso2, traffic, True)

def etl_task6_load_internet_quality_for_country(iso2, api_token=None):
    internet_quality = get_internet_quality_for_country(iso2, api_token)
    if internet_quality:
         insert_internet_quality_for_country_to_db(iso2, internet_quality, True)

if __name__ == "__main__":
    main()
