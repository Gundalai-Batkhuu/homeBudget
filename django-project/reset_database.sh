#!/bin/bash

rm db.sqlite3

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --username=admin --email=admin@example.com

echo "Seeding the database"
python data_seed.py