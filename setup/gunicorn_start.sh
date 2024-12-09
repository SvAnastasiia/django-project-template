#!/bin/bash

cd setup || exit

# Get the project directory
NAME="example-app-name"                                  				# Name of the application # TODO: replace with your app name
DJANGODIR="$(dirname $(pwd))"       		                        # Django project directory
DJANGOENVDIR="$DJANGODIR/venv"            			                # Django project env
USER="$(whoami)"                                     				    # the user to run as, recommended: do NOT use superuser (ex. ubuntu, root etc.)
GROUP="$(id -g -n)"                              				        # the group to run as
NUM_WORKERS=4                                    				        # TODO: change how many worker processes should Gunicorn spawn; recommended: 2 * number of CPU cores + 1
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

echo "Starting $NAME in $ENVIRONMENT environment as `whoami`"

# Activate the virtual environment
cd $DJANGODIR || exit

source "$DJANGOENVDIR/bin/activate"
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH
export DJANGO_ENVIRONMENT=$ENVIRONMENT  # Export the environment variable

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec "$DJANGOENVDIR/bin/gunicorn" ${DJANGO_WSGI_MODULE}:application \
  --chdir $DJANGODIR \
  --name $NAME \
  --workers $NUM_WORKERS \
  --worker-class gevent \
  --user=$USER --group=$GROUP \
  --bind=0.0.0.0:8000 \
  --log-level info \
  --capture-output \
  --timeout 120
