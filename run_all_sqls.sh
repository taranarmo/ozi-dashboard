source config.sh

cat sql/*.sql | gcloud sql connect $DATABASE_INSTANCE --user=$DATABASE_USER