source config.sh

cat *.sql | gcloud sql connect $DATABASE_INSTANCE --user=$DATABASE_USER