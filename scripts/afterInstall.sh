#!/usr/bin/bash
#cd myaccountapp/
#python -m venv env
#source env/bin/activate
#cd ..
#pip install -r requirements.txt
cd myaccountapp/
python manage.py makemigrations
python manage.py migrate