echo "WARNING: this script will drop asn-stats database and re-create it."
echo "Type 'confirm' to proceed..."

read user_input
if [ "$user_input" == "confirm" ]; then
    echo "\nLet's rock!"
else
    echo "\nNot today... buy!"
    exit
fi

source config.sh
