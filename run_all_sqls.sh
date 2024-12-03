source config.sh

cat etl/sql/*.sql | gcloud sql connect $DATABASE_INSTANCE --user=$DATABASE_USER