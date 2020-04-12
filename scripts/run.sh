#!/bin/bash

cd /root/app
source venv/bin/activate
python3 serve.py --prod --port 80
