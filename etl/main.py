import sys
from load_to_database import *
from country_lists import *
from etl_jobs import get_internet_quality_for_country

from etl_jobs import get_list_of_asns_for_country, get_stats_for_country, get_list_of_asn_neighbours_for_country, \
    get_traffic_for_country

CLOUDFLARE_API_TOKEN=os.getenv('OZI_CLOUDFLARE_API_TOKEN')

ETL_COUNTRIES = {  "RU": None }
# ETL_COUNTRIES = SPLITERCON
# _TALK

DATE_FROM='2023-07-01'
DATE_TO='2023-12-31'

def main():
    task_map = {
            "asns": etl_load_asns,
            "stats_1d": etl_load_stats_1d,
            "stats_5m": etl_load_stats_5m,
            "asn_neighbours": etl_load_asn_neighbours,
            "traffic": etl_load_traffic,
            "internet_quality": etl_load_internet_quality
    }

    if len(sys.argv) < 2:
        print("Error: No ETL task specified. Please provide 'task1', 'task2', or 'task3' as the first argument.")
        return

    task = sys.argv[1]
    if task not in task_map:
        print(f"Error: Unknown task '{task}'.")
        return

    for iso2 in ETL_COUNTRIES:
        print(f'ETL_TASK: {task}\nPARAMS: country {iso2} - {ETL_COUNTRIES[iso2]} for period {DATE_FROM} -- {DATE_TO}')
        task_map[task](iso2)
    print("Done")

def etl_load_asns(iso2, date_from=DATE_FROM, date_to=DATE_TO):
    asns = get_list_of_asns_for_country(iso2, date_from, date_to)
    if asns:
        insert_country_asns_to_db(iso2, date_from, date_to, asns, False, load_to_database=True)

def etl_load_stats_1d(iso2, date_from=DATE_FROM, date_to=DATE_TO):
    stats = get_stats_for_country(iso2, date_from, date_to, '1d')
    if stats:
        insert_country_stats_to_db(iso2, '1d', stats, True)

def etl_load_stats_5m(iso2, date_from=DATE_FROM, date_to=DATE_TO):
    for year in range(2019, 2025):
        stats = get_stats_for_country(iso2, f"{year}-01-01", f'{year + 1}-01-01', '5m')
        if stats:
            insert_country_stats_to_db(iso2, '5m', stats, True)

def etl_load_asn_neighbours(iso2, date_from=DATE_FROM, date_to=DATE_TO):
    asn_neighbours = get_list_of_asn_neighbours_for_country(iso2)
    if asn_neighbours:
        insert_country_asn_neighbours_to_db(iso2, datetime.now().strftime('%Y%m%d'), asn_neighbours, True)


def etl_load_traffic(iso2, date_from=DATE_FROM, date_to=DATE_TO):
    traffic=get_traffic_for_country(iso2, CLOUDFLARE_API_TOKEN)
    if traffic:
        insert_traffic_for_country_to_db(iso2, traffic, True)

def etl_load_internet_quality(iso2, date_from=DATE_FROM, date_to=DATE_TO):
    internet_quality = get_internet_quality_for_country(iso2, CLOUDFLARE_API_TOKEN)
    if internet_quality:
         insert_internet_quality_for_country_to_db(iso2, internet_quality, True)

if __name__ == "__main__":
    main()
