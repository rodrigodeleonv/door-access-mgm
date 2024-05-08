#!/bin/sh

PG_HOST=$POSTGRES_HOST
PG_PORT=5432

echo "Trying to connecto to Database $PG_HOST:$PG_PORT"
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