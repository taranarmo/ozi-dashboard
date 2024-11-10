# as-stats

1. Create Postgres instance on GCP, name it `asn-stats`
2. Use strong password for user `postgres` while creating DB
3. Go to `asn-stats`'s console
4. Download code by cloning Git Repository
```
  git clone https://github.com/ilja-vladi/as-stats.git
```
5. Create database, user and tables for asn_stats project
  - when asked for password use postgres password from step 2 first
  - and asn_data password for the second sql script

```
  cd as-stats
  ./init_database.sh
  
```
## TMP
```
cat sql/*.sql | gcloud sql connect asn-stats2 --user=asn_stats
```

## TODO
- 5min stats instead of daily
- index connectivity - load neighbours
- 

## Conference
data insights for countries with 'risky internet', comparition
connectivity index, reliability(?) index - how many asns guaranty connections to the outside
proposal for presentation
show riskis of "чебурнотизация" for different countries