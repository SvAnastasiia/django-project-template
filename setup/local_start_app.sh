#!/bin/bash

PY="python3.13"

cleanup_and_exit() {
    echo "Exiting..."
    # Kill background processes
    kill $ID_dramatiq $ID_periodiq || true
    exit 1
}

# Set up trap to catch Ctrl+C
trap cleanup_and_exit SIGINT

set -e
source venv/bin/activate
source .env

# TODO: Uncomment in case the application uses postgres or remove if not needed
#check_db() {
#    pg_isready -d "$DB_NAME" -h "$DB_HOST" -p 5432 -U "$DB_USER"
#}

# TODO: Uncomment in case the application uses redis or remove if not needed
#check_redis() {
#    redis-cli ping > /dev/null 2>&1
#}

# TODO: Uncomment in case the application uses postgres or remove if not needed
#echo "Checking Postgres..."
#if check_db; then
#  echo "Postgres is up - continuing..."
#else
#  echo "Postgres is unavailable"
#  exit 1
#fi

# TODO: Uncomment in case the application uses redis or remove if not needed
#echo "Checking Redis..."
#if check_redis; then
#  echo "Redis is up - continuing..."
#else
#  echo "Redis is unavailable"
#  exit 1
#fi


$PY manage.py migrate || exit 1
$PY manage.py collectstatic --no-input || exit 1

# TODO: Uncomment in case the application has asynchronous tasks and uses Dramatiq and/or Periodiq to handle them  or remove if not needed
#$PY manage.py rundramatiq --processes=1 --threads=1 &
#ID_dramatiq=$!
#$PY manage.py runperiodiq &
#ID_periodiq=$!

$PY manage.py runserver || exit 1
