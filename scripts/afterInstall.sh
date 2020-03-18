#!/usr/bin/env bash
cd /home/ubuntu/myaccountapp/
sudo python3 manage.py makemigrations
sudo python3 manage.py migrate

cd /home/ubuntu/myaccountapp/
sudo cp -rf scripts/amazon-cloudwatch-agent.json /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -c file:/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json -s