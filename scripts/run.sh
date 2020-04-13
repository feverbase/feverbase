#!/bin/bash

cd /root/app
source venv/bin/activate

until python3 serve.py --prod --port 80; do
  EXIT=$?
  if [ $EXIT -eq 143 ]; then
    echo "Exiting gracefully..."
    break
  fi

  echo "Server crashed with exit code $EXIT, respawning..." >&2
  sleep 1
done
