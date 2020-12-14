echo "Starting"
mongoimport --db vault --collection icons --type json --file /docker-entrypoint-initdb.d/icons.json --jsonArray
echo "Done"