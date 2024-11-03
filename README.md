# as-stats

- create compute engine at GCP (assure that cloud-sql api is enabled)
- ssh to this instance
- run following commands there:

  ```
  sudo apt-get update
  sudo apt-get install postgresql-client

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