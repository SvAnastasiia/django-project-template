#!/bin/bash

sudo systemctl start postgresql
sudo systemctl enable postgresql

sudo -u postgres psql -c "CREATE ROLE <project-name> WITH LOGIN PASSWORD '<project-name>';"
sudo -u postgres psql -c "CREATE DATABASE <project-name> WITH OWNER <project-name>;"
