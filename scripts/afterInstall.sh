#!/usr/bin/env bash
cd /home/ubuntu/myaccountapp/
python3 -m venv env
source env/bin/activate
cd /home/ubuntu/
pip3 install -r requirements.txt
cd /home/ubuntu/myaccountapp/
python3 manage.py makemigrations
python3 manage.py migrate