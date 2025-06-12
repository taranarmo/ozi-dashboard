#!/bin/bash

# DB connection
HOST="localhost"
USER="ozi"
DB="ozi_db"

# Output directory (optional)
OUTDIR="./exports"
mkdir -p "$OUTDIR"

# List of countries
declare -A COUNTRIES=(
    ["AM"]="Armenia"
    ["AZ"]="Azerbaijan"
    ["BY"]="Belarus"
    ["EE"]="Estonia"
    ["GE"]="Georgia"
    ["KZ"]="Kazakhstan"
    ["KG"]="Kyrgyzstan"
    ["LV"]="Latvia"
    ["LT"]="Lithuania"
    ["MD"]="Moldova"
    ["RU"]="Russia"
    ["TJ"]="Tajikistan"
    ["TM"]="Turkmenistan"
    ["UA"]="Ukraine"
    ["UZ"]="Uzbekistan"
    ["PL"]="Poland"
    ["MN"]="Mongolia"
    ["CZ"]="Czechia"
)

for ISO2 in "${!COUNTRIES[@]}"; do
    OUTFILE="${OUTDIR}/${ISO2,,}_stats_weekly.csv"

    echo "Exporting data for ${COUNTRIES[$ISO2]} ($ISO2)..."

    psql -h "$HOST" -U "$USER" "$DB" --csv -o "$OUTFILE" <<EOF
select date_trunc('week', cs_stats_timestamp)::date,
       round(avg(cs_v4_prefixes_ris)) as avg_cs_v4_prefixes_ris,
       round(avg(cs_v6_prefixes_ris)) as avg_cs_v6_prefixes_ris,
       round(avg(cs_asns_ris)) as avg_cs_asns_ris,
       round(avg(cs_asns_stats)) as avg_cs_asns_stats
from data.country_stat
where cs_country_iso2 = '$ISO2' and cs_stats_resolution = '1d'
group by date_trunc('week', cs_stats_timestamp)::date
order by date_trunc('week', cs_stats_timestamp)::date;
EOF

done