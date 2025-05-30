# Django project template #

Includes initial setup for a Django project.

### What is included? ###

* Poetry package manager
* Django, Django Rest Framework and simplejwt for authentication installed and configured
* Logging
* Postgres connection instructions
* Drf-spectacular for Swagger documentation generating
* Pre-commit hooks for black, isort and flake8
* Environment variables validation and reading from .env file using pydantic
* AWS S3 storage connection configured

### How do I get set up? ###

#### No Docker ####
* Install python 3.13
* Install poetry
* Clone the repository
* Install dependencies using `poetry install`
* Identify the virtual environment using `poetry env info --path` and activate it using `poetry shell` or `source <path_to_venv>/bin/activate`
* Create .env file in the root directory (same level as .env.example) and add the variables that are contained in .env.example file
* Ensure database is connected and check credentials (you can use default sqlite3 for local, but it is recommended to use Postgres as it is used in production)
* Run the migrations using `python manage.py migrate`
* Create superuser using `python manage.py createsuperuser` and follow the instructions to create a superuser
* Collect static files using `python manage.py collectstatic`
* Run the server using `python manage.py runserver`
* If you need to add a new application to the project, use `python manage.py startapp <app_name>`, register it in the settings.py file in the INSTALLED_APPS list

#### Docker-compose ####
* Install docker and docker-compose
* Clone the repository
* Create .env file in the root directory (same level as .env.example) and add the variables that are contained in .env.example file. Pay attention to service names in compose file while creating the .env file, for example database is named 'db', so you should use this value as host instead of localhost.
* Run the docker-compose using `docker-compose up --build`
* There might be some issues with the entrypoint file, if you see the error `./entrypoint-local.sh: no such file or directory`, it means that the entrypoint file is not executable. This can happen if you are using Windows and the file was created with Windows line endings / they were applied in Git. To fix this, run `dos2unix ./entrypoint-local.sh` to convert the file to Unix line endings.
* If the permission issues with executable file occur, run `chmod +x ./entrypoint-local.sh` to make the file executable and rebuild the docker image using `docker-compose up --build`

### Best practices regarding code organisation ###

* Do not put any logic in the views.py file, create a `services` directory inside your app, create a file with meaningful service name and separate your logic there, if some functions have similar purposes, organize it into service class.
* If service is used in multiple apps, create a `services` directory in the root of the project, move your logic there and import it in the apps where it is needed.
* Add typing to your functions and classes, use type hints and type checking.

### What a developer should know? ###

* Use pre-commit hooks to ensure code quality: `pre-commit install`, in case change needed in the hooks, modify `.pre-commit-config.yaml` file, more details here: https://pre-commit.com/
* Working with poetry for dependency management: `poetry add <package_name>`, `poetry remove <package_name>`, `poetry update`, `poetry install`..., more here: https://python-poetry.org/docs/managing-dependencies/. Poetry groups are used to separate the dependencies into groups, for example, `dev` group is used for code enhancement libraries, `setup` group is used for deployment-needed libraries, `test` group can be used for testing dependencies etc.