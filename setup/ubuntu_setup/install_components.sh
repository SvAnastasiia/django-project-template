#!/bin/bash

PY="python3.13"

# Get the current working directory
CURRENT_DIR="$(pwd)"

# Get the project directory
PROJECT_DIR="$(dirname "$(dirname "$CURRENT_DIR")")"

# Ubuntu 22.04
sudo apt -y update
sudo apt -y upgrade

sudo apt -y install ${PY}-dev ${PY} ${PY}-venv \
     postgresql-client postgresql-contrib-13 redis-tools redis-server \
     supervisor

# Create venv if no venv is present in project dir
venv_dir="$PROJECT_DIR/venv"
if [ -d "$venv_dir" ]; then
    echo "Virtual environment already exists in $venv_dir. Skipping creation."
else
    $PY -m venv $venv_dir
    echo "Virtual environment created in $venv_dir."
fi

# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -
sudo apt-get install python3-poetry
pip install poetry

# Install dependencies
source $PROJECT_DIR/venv/bin/activate
poetry install
