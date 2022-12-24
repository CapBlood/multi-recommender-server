set -e

mongod --fork --logpath /var/log/mongod.log

poetry run python3 ./scripts/init_db/load_anime_csv_mongo.py
