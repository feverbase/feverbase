#!/bin/bash

# Ctrl+C a few times for good measure
screen -S flask -X stuff $'\003'
screen -S flask -X stuff $'\003'
screen -S flask -X stuff $'\003'

kill $(lsof -ti :80)

# kills all screen sessions with same name
#SESSION_NAME='flask'
#screen -ls "$SESSION_NAME" | (
#  IFS=$(printf '\t');
#  sed "s/^$IFS//" |
#  while read -r name stuff; do
#      screen -S "$name" -X stuff $'\003'
#  done
#)
