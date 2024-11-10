echo "WARNING: this script will drop all tables in asn_stats database and re-create them."
echo "Type 'confirm' to proceed..."

read user_input
if [ "$user_input" == "confirm" ]; then
    echo "\nLet's rock!"
else
    echo "\nNot today... buy!"
    exit
fi

source config.sh
cat create_database_schema.sql | gcloud sql connect $DATABASE_INSTANCE --user=$DATABASE_USER