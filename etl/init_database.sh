echo "WARNING: this script will drop asn_stats database and re-create it."
echo "Type 'confirm' to proceed..."

read user_input
if [ "$user_input" == "confirm" ]; then
    echo "\nLet's rock!"
else
    echo "\nNot today... buy!"
    exit
fi

source config.sh
cat init_database.sql | gcloud sql connect $DATABASE_INSTANCE --user=postgres