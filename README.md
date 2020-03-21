# TLDRSS - API

Back-end Django REST API for TL;DRss client app.

## Running the app

Once completting all installation steps below, simply run 

### `python manage.py runserver` 


# Installation

First, make sure you have the development client-side React app running: [https://github.com/rdbishop19/TLDRss](Installation) 

Clone this repository. `cd` into the project directory and run:

### `python manage.py migrate`

## Load example data

### `python manage.py loaddata`

## Setup local env

### `python -m venv env`
### `source env/bin/activate` (MAC)
### `source env/Scripts/activate` (PC)

## Dependencies

### `pip install -r requirements.txt`

# Browseable API (optional) 

Visit [http://localhost:8000](http://localhost:8000) to view the browseable API.