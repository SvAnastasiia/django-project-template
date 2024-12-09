#!/bin/bash

PY="python3.13"

# Get the project directory
PROJECT_DIR="$(pwd)"

# Check if Homebrew is installed
if test ! $(which brew); then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Undo all changes you have made to any of Homebrew's repositories
brew update-reset
# Update Homebrew
brew update

# Install necessary packages
brew install python@3.13 postgresql@13 redis

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