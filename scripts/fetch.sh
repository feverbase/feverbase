#!/bin/bash

cd /root/app
source venv/bin/activate
python3 fetch.py
./scripts/restart.sh
