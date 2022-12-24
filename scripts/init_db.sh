set -e

mongod --fork --logpath /var/log/mongod.log
poetry run dvc pull
# poetry run python3 ./scripts/init_db/load_anime_csv_mongo.py
poetry run dvc repro
