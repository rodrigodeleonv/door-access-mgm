#!/bin/sh

PG_HOST="$POSTGRES_HOST"
PG_PORT=${PG_PORT:-5432}
ENTRY_SKIP=${ENTRY_SKIP:-0}

# ENTRY_SKIP allows to bypass the Docker entrypoint script
# Use for debug purposes

if [ "$ENTRY_SKIP" = "1" ]; then
    echo "DEBUG mode enabled. Skipping all"
    exec "$@"
    exit 0
fi

echo "Trying to connect to Database $PG_HOST:$PG_PORT"
while ! nc -z $PG_HOST $PG_PORT
do
    echo "Waiting connection..."
    sleep 1
done

echo "Migrate"
python proj/manage.py migrate --noinput

echo "Collect statics"
python proj/manage.py collectstatic --noinput --clear > /dev/null

echo "Provisioning"
python proj/manage.py runscript provision

exec "$@"