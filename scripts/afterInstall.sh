#!/usr/bin/env bash
cd ..
python3 manage.py makemigrations
python3 manage.py migrate