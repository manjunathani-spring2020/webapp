#!/usr/bin/env bash
cd /srv/app/myaccountapp/
python3 manage.py makemigrations
python3 manage.py migrate