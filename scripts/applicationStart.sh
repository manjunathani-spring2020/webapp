#!/usr/bin/env bash
cd /home/ubuntu/myaccountapp/
nohup python3 -u manage.py runserver 0.0.0.0:8000 </dev/null >/dev/null 2>&1 &