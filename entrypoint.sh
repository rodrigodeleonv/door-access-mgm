#!/bin/sh

PG_HOST=$POSTGRES_HOST
PG_PORT=5432

echo "Trying to connecto to Database: $PG_HOST:$PG_PORT"
while ! nc -z $PG_HOST $PG_PORT
do
echo "Waiting connection..."
sleep 1
done

echo "Migrate"
python proj/manage.py migrate --no-input
# For initial provisioning only!
# echo "Provisioning Database. Loading data and Config CiberC."
# python manage.py runscript scripts.initial.data_load
# echo "Collecting statics..."
# python manage.py collectstatic --no-input --clear > /dev/null

exec "$@"