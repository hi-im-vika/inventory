#!/bin/sh
export FLASK_APP=./app.py
uv run flask --debug run -p 8080