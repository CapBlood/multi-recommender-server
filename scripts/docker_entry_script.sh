set -e

mongod --fork --logpath /var/log/mongod.log

exec "$@"