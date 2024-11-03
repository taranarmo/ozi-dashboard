from sqlalchemy import create_engine

HOST="34.32.52.216"
PORT="5432"
DBNAME="as_stats"
USER="as_stats"
PASSWORD='...'

def get_db_connection(password):
    connection_string = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"
    engine = create_engine(connection_string)
    return engine.connect()

def insert_all_asns_for_country(country_iso2, list_of_asns):
    connection = get_db_connection(PASSWORD)
    sql= "insert into asn_country (a_country_iso2, a_ripe_id) values ('aa', 100)"
    connection.execute(sql)
