#!/bin/bash

cd /root/app
git pull
source venv/bin/activate
pip3 install -r requirements.txt
./scripts/restart.sh
