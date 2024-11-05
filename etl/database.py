from sqlalchemy import create_engine

HOST="34.32.52.216"
PORT="5432"
DBNAME="as_stats"
USER="as_stats"
PASSWORD='abc123'

def get_db_connection(password):
    connection_string = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"
    engine = create_engine(connection_string)
    return engine.connect()

def insert_country_asns_to_db(country_iso2, list_of_asns):
    connection = get_db_connection(PASSWORD)
    sql= "INSERT INTO dwh.asn(a_country_iso2, a_ripe_id)\nVALUES"
    for asn in list_of_asns:
        sql += f"\n('{country_iso2}', {asn}),"
    sql = sql[:-1] + ";"
    print(sql)
    connection.execute(sql)

def insert_country_stats_to_db(country_iso2, stats):
    connection = get_db_connection(PASSWORD)
    sql= ("INSERT INTO dwh.country_stat(cs_country_iso2, cs_stats_date, cs_v4_prefixes_ris, cs_v6_prefixes_ris,"
          " cs_asns_ris, cs_v4_prefixes_stats, cs_v6_prefixes_stats, cs_asns_stats )\nVALUES ")
    for item in stats:
        sql += (f"\n('{country_iso2}', '{item['stats_date'][:10]}', {item['v4_prefixes_ris']}"
                f"{item['v6_prefixes_ris']}, {item['asns_ris']}, {item['v4_prefixes_stats']}, "
                f"{item['v6_prefixes_stats']}, {item['asns_stats']}),")
    sql = sql[:-1] + ";"
    print(sql)
    connection.execute(sql)
