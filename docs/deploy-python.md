# Running in a development mode

Run the following commands in terminal to run Nextpie in development mode with debugging. If you want to run as a docker container with zero configuration please skip this and refer to docker execution section.

```bash
## Clone the repository
git clone https://version.helsinki.fi/fimm/nextpie.git
cd nextpie

## Create a virtual environment (Unix)
virtualenv -p python3.6 env
source env/bin/activate

## Install modules - SQLite Database
pip3 install -r requirements/requirements.txt
## OR with PostgreSQL
# pip install -r requirements/requirements-pgsql.txt

## Set the FLASK_APP environment variable (Unix/Mac)
export FLASK_APP=run.py

## Set up the DEBUG environment (Unix/Mac)
export FLASK_ENV=development

## Database setup and seeding if SQLite database file is not available
#flask db init
#flask db migrate -m "first"
#flask db upgrade
#flask seed

# Start the application (development mode)
# --host=0.0.0.0 - expose the app on all network interfaces (default 127.0.0.1)
# --port=5000    - specify the app port (default 5000)  
flask run --host=0.0.0.0 --port=5000
```

Access Nextpie via the link showed in the console. Use username `admin` and password `admin` to login. By default SQlite database is located at `$HOME/.Nextpie/nextpie-DB.sqlite3`. You can change the path by modifying the variable `SQLALCHEMY_DATABASE_URI ` in `config.py`.

