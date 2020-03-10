#!/usr/bin/env bash
cd /home/ubuntu/myaccountapp/
python3 manage.py makemigrations
python3 manage.py migrate