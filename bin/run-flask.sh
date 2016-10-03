#!/usr/bin/env bash

export FLASK_APP=bin/uwsgi.py
python -m flask run # --host=0.0.0.0

