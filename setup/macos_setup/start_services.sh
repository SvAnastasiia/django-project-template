#!/bin/bash

# Start Redis
brew services start redis

# Start PostgreSQL
brew services start postgresql@13

# Create PostgreSQL database
createuser <project-name> --createdb
createdb <project-name> -U <project-name>-user