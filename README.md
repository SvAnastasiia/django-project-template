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
