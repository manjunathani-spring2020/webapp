#!/usr/bin/env bash
cd /home/ubuntu/myaccountapp/
sudo python3 manage.py makemigrations
sudo python3 manage.py migrate
sudo cp -rf cloudwatch-config.json /opt/aws/amazon-cloudwatch-agent/etc/cloudwatch-config.json
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -c file:/opt/aws/amazon-cloudwatch-agent/etc/cloudwatch-config.json -s