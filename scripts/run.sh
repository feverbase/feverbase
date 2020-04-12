#!/bin/bash

cd /root/app
source venv/bin/activate
until python3 serve.py --prod --port 80; do
  echo "Server crashed with exit code $?, respawning..." >&2
  sleep 1
done
