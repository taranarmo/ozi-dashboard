echo "WARNING: this script will drop asn_stats database and re-create it. Type 'confirm' to proceed..."
read user_input

if [ "$user_input" == "confirm" ]; then
    echo "Let's rock!"
else
    echo "Not today..."
    exit
fi

source config.sh
echo 'Initializing the database...'
cat create_database_and_user.sql | gcloud sql connect $DATABASE_INSTANCE --user=postgres
echo 'Creating the database schema...'
cat create_database_schema.sql | gcloud sql connect $DATABASE_INSTANCE --user=$DATABASE_USER