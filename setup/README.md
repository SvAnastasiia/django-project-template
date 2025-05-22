# Setup the project locally #

## Ubuntu 22.04 ##

*Scripts for Ubuntu setup are in `ubuntu_setup` folder:*
- install_components.sh
- setup_db.sh
- start_redis.sh

*To run the setup use the following command:*

`make ubuntu_setup`

## MacOS ##

*Scripts for MacOS setup are in `macos_setup` folder:*
- install_components.sh
- start_services.sh

*To run the setup use the following command:*

`make macos_setup`

## For development ##
*Perform the following actions:*
- Run `pre-commit install`
- Run `cp .env.example .env` and populate it with required data

## Start app ##

*To start the app run the following command:*

`make start_app`

- Checks db availability
- Pings redis (used for worker)
- Runs migrations, collects static files
- Runs the server


# Server setup #
## Setup the project using supervisor as daemon and gunicorn worker ##

1) Run the `install_components.sh` script
2) In the project root directory (location on manage.py) create logs directory
```
mkdir -p logs/gunicorn
touch logs/gunicorn/info.log
touch logs/gunicorn/error.log
```
2) Execute `sudo nano /etc/supervisor/conf.d/gunicorn.conf` (instead of `gunicorn.conf` anything can be choosen as filename)
3) Copy the content below
```
; ================================
;  gunicorn supervisor
; ================================

[program:<APPLICATION_NAME>]
directory = <APPLICATION_ROOT_DIR>/setup
command = <APPLICATION_ROOT_DIR>/setup/gunicorn_start.sh
user = <SYSTEM_USER>
stdout_logfile = <APPLICATION_ROOT_DIR>/logs/gunicorn/info.log
stderr_logfile = <APPLICATION_ROOT_DIR>/logs/gunicorn/error.log
autostart=true
autorestart=true
numprocs=1
environment=HOME="<APPLICATION_ROOT_DIR>",LANG=en_US.UTF-8,LC_ALL=en_US.UTF-8
```
### Names meaning ###

- APPLICATION_NAME - can be any and will be used to control application with supervisor
- APPLICATION_ROOT_DIR - location of manage.py file
- SYSTEM_USER - can be checked using `whoami` command

### Supervisor conf (important) ###
- directory - location of the launch script, otherwise commands in launch script that dynamically 
set location will return wrong path, by default `pwd` will return `/` and script will not work as 
it should see the script location path, not root path.
- command - start script full path
- stdout_logfile - info logs file
- stderr_logfile - error logs file
- numprocs - number of launched processes

## Usage ##

#### To update supervisor process when conf file is changed via CLI (gunicorn.conf) ####

`sudo supervisorctl reread` - rereads configuration update, if syntax is wrong, outputs the message

`sudo supervisorctl update <APPLICATION_NAME>` - stops the process if running and takes changes 

#### To restart supervisor process ####

`sudo supervisorctl restart <APPLICATION_NAME>` - stops the process if running and relaunches it

#### To start/stop supervisor process ####

`sudo supervisorctl start <APPLICATION_NAME>`

`sudo supervisorctl stop <APPLICATION_NAME>`

#### To check status of supervisor process ####

`sudo supervisorctl status <APPLICATION_NAME>`

`sudo supervisorctl status all` - if multiple apps are running (ex. app and worker)

# SSH server access #
To access the server via SSH, the following steps should be performed:
- Generate SSH key pair if not already generated.
- Go to https://forge.laravel.com/servers and select the server. Navigate to the SSH Keys tab.
- Copy your public key and paste it. Save changes.
- Now you can access the server using the following command:
`ssh -i </path/to/private-key> forge@<server-public-ip>`

# Deployment #
Deployment is handled automatically on push to the dev/staging/main branch.

# Git branching strategy #
- `main` - production branch
- `staging` - staging branch
- `dev` - development branch

### We try to use Gitflow branching strategy. Some of the rules are: ###
- `feature` branches are created from `dev` branch and merged back into `dev` branch.
- Once `feature` branch is complete and tested locally, it's merged into `staging`.
- `staging` branch is used for testing in similar to production environment.
- Once `staging` branch is tested and ready for production, it's merged into `main`.
- When a bug is found in production, a `bugfix` branch is created directly from `main`.
- `bugfix` branch is merged into `staging` and tested. Then merged into both `dev` and `main` branches.

Note: When you create new migrations be aware of migration conflicts between multiple features.
