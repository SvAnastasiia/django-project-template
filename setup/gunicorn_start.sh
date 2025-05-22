#!/bin/bash

cd setup || exit

# Get the project directory
NAME="example-app-name"                                  				# Name of the application # TODO: replace with your app name
DJANGODIR="$(dirname $(pwd))"       		                        # Django project directory
USER="$(whoami)"                                     				    # the user to run as
GROUP="$(id -g -n)"                              				        # the group to run as
NUM_WORKERS=2                                    				        # TODO: adjust for your server (2 * cores + 1)
DJANGO_SETTINGS_HOME=config.settings             				        # Base settings dir of the app
DJANGO_WSGI_MODULE=config.wsgi

# Load environment variables from .env file in parent directory
if [ -f "$DJANGODIR/.env" ]; then
    source "$DJANGODIR/.env"
fi

# Read the ENVIRONMENT variable or set default value
ENVIRONMENT="${ENVIRONMENT:-development}"

# Append the environment name to the base settings module
DJANGO_SETTINGS_MODULE="$DJANGO_SETTINGS_HOME.$ENVIRONMENT"

echo "Starting $NAME in $ENVIRONMENT environment as $(whoami)"

# Detect virtual environment
if [[ -n "$VIRTUAL_ENV" ]]; then
    DJANGOENVDIR="$VIRTUAL_ENV"
elif command -v poetry &>/dev/null && poetry env info -p &>/dev/null; then
    DJANGOENVDIR="$(poetry env info -p)"
elif [ -d "$DJANGODIR/venv" ]; then
    DJANGOENVDIR="$DJANGODIR/venv"
else
    exit 1
fi

echo "Using virtual environment at: $DJANGOENVDIR"

# Activate the virtual environment
cd "$DJANGODIR" || exit
source "$DJANGOENVDIR/bin/activate"

# Export environment variables for Django and Python
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH
export DJANGO_ENVIRONMENT=$ENVIRONMENT

# Start Gunicorn
exec "$DJANGOENVDIR/bin/gunicorn" ${DJANGO_WSGI_MODULE}:application \
  --chdir "$DJANGODIR" \
  --name "$NAME" \
  --workers $NUM_WORKERS \
  --worker-class gevent \
  --user="$USER" --group="$GROUP" \
  --bind=0.0.0.0:8000 \
  --log-level info \
  --capture-output \
  --timeout 120
