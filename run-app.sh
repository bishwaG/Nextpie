#!/bin/bash

source env/bin/activate
#export FLASK_APP=run.py
#export FLASK_ENV=development
export FLASK_DEBUG=1
export FLASK_APP=run.py 


flask run --debugger
