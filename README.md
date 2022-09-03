# My Media List

## Requirements
* Originally developed on Python 3.10, may work with other versions of Python 3
* Developed with Node v14.20.0, but should work with any version that supports dependencies in package.json

## Development Setup

* Run `docker-compose.yml` to set up a local postgres container
* Run `npm install` to install Node dependencies
* Install Python packages from `requirements.txt`

## Django Setup

1. Run `python manage.py migrate` to apply SQL migrations
2. Run `python manage.py runserver` to start the Django development server
