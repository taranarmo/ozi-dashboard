# as-stats

1. Create Postgres instance on GCP, name it `asn_stats`
2. Use strong password for user `postgres` while creating DB, save it to the clipboard
3. Go to `asn-stats`'s console
4. Download code by cloning Git Repository
```
  git clone https://github.com/ilja-vladi/as-stats.git
```
5. Create database and user for asn_stats project
```
  cd as-stats/scripts
  # when asked for password use postgres password from step 2. 
  ./init_database.sh
  
```
6. Generate strong password for asn_stats user
```
  gcloud sql users set-password asn_stats --instance=asn_stats --password="put-your-password-here"
```
7. Create DB schema
```
  cat as-stats/create_database_schema.sql | gcloud sql connect asn-stats --user=asn_stats
```



## OLD - To Sort

- create compute engine at GCP (assure that cloud-sql api is enabled)
- ssh to this instance
- run following commands there:

  ```
  sudo apt-get update
  sudo apt-get install postgresql-client
  sudo apt-get install pip

  psql "host=127.0.0.1 port=5432 sslmode=disable dbname=as_stats user=as_stats"
  ```
  

## installing on gcp compute instance
ssh to the gcp compute engine instance
```
# ssh key
ssh-keygen -t ed25519 -C "your_email@example.com"
cat .ssh/id_ed25519.pub
```

copy output to github - add it as a new ssh-keys
```
git clone git@github.com:ilja-vladi/as-stats.git
cd as-stats
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