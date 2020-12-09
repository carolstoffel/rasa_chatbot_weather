#!/bin/sh

if [ -z "$PORT"]
then
  PORT=5056
fi
rasa run -m models --endpoints --enable-api --cors "*" --debug --port $PORT
