#!/usr/bin/bash
cd myaccountapp/
nohup python -u manage.py runserver 0.0.0.0:8000 </dev/null >/dev/null 2>&1 &