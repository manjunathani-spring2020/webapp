#!/usr/bin/env bash
cd /home/ubuntu/myaccountapp/
source env/bin/activate
nohup python3 manage.py runserver 0.0.0.0:8000 &