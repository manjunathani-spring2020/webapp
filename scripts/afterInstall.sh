#!/usr/bin/env bash
source .bashrc
python3 manage.py makemigrations
python3 manage.py migrate