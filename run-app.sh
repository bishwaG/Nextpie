#!/bin/bash

source env/bin/activate
export FLASK_APP=run.py
export FLASK_ENV=development

flask run --debugger
