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

* Install python 3.13
* Install poetry
* Clone the repository
* Create virtual environment using `python -m venv venv`
* Activate virtual environment using `source venv/bin/activate`
* Install dependencies using `poetry install`
* Create .env file in the root directory (same level as .env.example) and add the variables that are contained in .env.example file
* Ensure database is connected and check credentials (you can use default sqlite3 for local, but it is recommended to use Postgres as it is used in production)
* Run the migrations using `python manage.py migrate`
* Create superuser using `python manage.py createsuperuser`
* Collect static files using `python manage.py collectstatic`
* Run the server using `python manage.py runserver`
* Add application to the project using `python manage.py startapp <app_name>`, register it in the settings.py file in the INSTALLED_APPS list

### Best practices regarding code organisation ###

* Do not put any logic in the views.py file, create a `services` directory inside your app, create a file with meaningful service name and separate your logic there, if some functions have similar purposes, organize it into service class.
* If service is used in multiple apps, create a `services` directory in the root of the project, move your logic there and import it in the apps where it is needed.
* Add typing to your functions and classes, use type hints and type checking.

### What a developer should know? ###

* Use pre-commit hooks to ensure code quality: `pre-commit install`, in case change needed in the hooks, modify `.pre-commit-config.yaml` file, more details here: https://pre-commit.com/
* Working with poetry for dependency management: `poetry add <package_name>`, `poetry remove <package_name>`, `poetry update`, `poetry install`..., more here: https://python-poetry.org/docs/managing-dependencies/