#!/usr/bin/env bash
#cd myaccountapp/
#python -m venv env
#source env/bin/activate
#cd ..
#pip install -r requirements.txt
cd /home/ubuntu/myaccountapp/
python3 manage.py makemigrations
python3 manage.py migrate