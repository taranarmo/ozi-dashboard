import argparse
from load_to_database import *
from country_lists import *
from etl_jobs import get_internet_quality_for_country

from etl_jobs import get_list_of_asns_for_country, get_stats_for_country, get_list_of_asn_neighbours_for_country, \
    get_traffic_for_country

CLOUDFLARE_API_TOKEN=os.getenv('OZI_CLOUDFLARE_API_TOKEN')
BAR_LENGTH = 50


def main():
    parser = argparse.ArgumentParser(description="ETL script for OZI Dashboard project.")
    parser.add_argument('-t', '--task', required=True, help="ETL task to perform (e.g., 'asns', 'stats_1d').")
    parser.add_argument('-c', '--countries', required=True, nargs='+', help="List of country ISO2 codes (e.g., 'US', 'DE').")
    parser.add_argument('-df', '--date-from', required=True, help="Start date in YYYY-MM-DD format.")
    parser.add_argument('-dt', '--date-to', required=True, help="End date in YYYY-MM-DD format.")

    args = parser.parse_args()
    task = args.task
    countries = args.countries
    try:
        date_from = datetime.strptime(args.date_from, "%Y-%m-%d")
        date_to = datetime.strptime(args.date_to, "%Y-%m-%d")
    except ValueError:
        print("Error: Dates must be in YYYY-MM-DD format.")
        return

    task_map = {
        "ASNS": etl_load_asns,
        "STATS_1D": etl_load_stats_1d,
        "STATS_5M": etl_load_stats_5m,
        "ASN_NEIGHBOURS": etl_load_asn_neighbours,
        "TRAFFIC": etl_load_traffic,
        "INTERNET_QUALITY": etl_load_internet_quality
    }

    if task not in task_map:
        print(f"Error: Unknown task '{task}'.")
        return

    for iso2 in countries:
        print(f"Started:    {task}")
        print(f"At:         {datetime.now()}")
        print(f"Country:    {iso2}")
        print(f"Date From:  {date_from.strftime("%Y-%m-%d")}")
        print(f"Date To:    {date_to.strftime("%Y-%m-%d")}\n")

        task_map[task](iso2, date_from, date_to)

        print(f"At:         {datetime.now()}")
        print(f"Finished:   {task}")


def etl_load_asns(iso2, date_from, date_to):
    print("Getting data from the API and storing to DB... ")
    for asns_batch, last_date in get_list_of_asns_for_country(iso2, date_from, date_to):
        progress = float((last_date - date_from).days + 1) / ((date_to - date_from).days + 1)
        filled_length = int(BAR_LENGTH * progress)
        bar = '█' * filled_length + '-' * (BAR_LENGTH - filled_length)
        print(f'\r{date_from.strftime("%Y-%m-%d")} |{bar}| {date_to.strftime("%Y-%m-%d")}', end=' ', flush=True)
        insert_country_asns_to_db(iso2, asns_batch, save_sql_to_file=False, load_to_database=True)


def etl_load_stats_1d(iso2, date_from, date_to):
    stats = get_stats_for_country(iso2, date_from, date_to, '1d')
    if stats:
        insert_country_stats_to_db(iso2, '1d', stats, True)

def etl_load_stats_5m(iso2, date_from, date_to):
    for year in range(2019, 2025):
        stats = get_stats_for_country(iso2, f"{year}-01-01", f'{year + 1}-01-01', '5m')
        if stats:
            insert_country_stats_to_db(iso2, '5m', stats, True)

def etl_load_asn_neighbours(iso2, date_from, date_to):
    asn_neighbours = get_list_of_asn_neighbours_for_country(iso2, date_from, date_to)
    if asn_neighbours:
        insert_country_asn_neighbours_to_db(iso2, asn_neighbours, True)


def etl_load_traffic(iso2, date_from, date_to):
    traffic=get_traffic_for_country(iso2, CLOUDFLARE_API_TOKEN)
    if traffic:
        insert_traffic_for_country_to_db(iso2, traffic, True)

def etl_load_internet_quality(iso2, date_from, date_to):
    internet_quality = get_internet_quality_for_country(iso2, CLOUDFLARE_API_TOKEN)
    if internet_quality:
         insert_internet_quality_for_country_to_db(iso2, internet_quality, True)

if __name__ == "__main__":
    main()
