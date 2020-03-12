#!/usr/bin/env bash
cd /home/ubuntu/myaccountapp/
python3 -m venv env
source env/bin/activate
nohup python3 manage.py runserver 0.0.0.0:8000 &