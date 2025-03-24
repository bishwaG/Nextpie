# Running in a development mode

## Prerequisite
Before deploying nextpie using Python in development make sure that you have the following in your system.
- python3.9
- setuptools
- python3-dev/python3-devel
- libsqlite3-dev
- libbz2-dev
- git

> NOTE: To deploy Nextpie using Python >=3.12, you have to install `distutils` manually. Starting from Python 3.10, the distutils module was deprecated and removed from the standard library in Python 3.12. Since Nextpie is not tested in >=3.10, we do not guaranteed that things will not break. Python >=3.10 support will be added in Nextpie in the future.

If your system does not have `Python3.9`, please check the [instructions](python-from-source.md) how to build `Python3.9` from source.

Run the following commands in terminal to run Nextpie in development mode with debugging. If you want to run as a docker container with zero configuration please skip this and refer to docker execution section.

```bash
## Clone the repository
git clone https://github.com/bishwaG/Nextpie.git
cd Nextpie

## Create a virtual environment (Unix)
## Change python version or user only 'python3'
virtualenv -p python3.9 env
source env/bin/activate

## Install modules - SQLite Database
pip3 install -r requirements/requirements.txt
## OR with PostgreSQL
# pip install -r requirements/requirements-pgsql.txt

## Set the FLASK_APP environment variable (Unix/Mac)
export FLASK_APP=run.py

## Set up the DEBUG environment (Unix/Mac)
export FLASK_DEBUG=1

## Database setup and seeding if SQLite database file is not available
#flask db init
#flask db migrate -m "first"
#flask db upgrade
#flask seed

# Start the application (development mode)
# --host=0.0.0.0 - expose the app on all network interfaces (default 127.0.0.1)
# --port=5000    - specify the app port (default 5000)  
flask run --host=127.0.0.1 --port=5000
```


Open your browser and go to [http://localhost:5000](http://localhost:5000). Use username `admin` and password `admin` to login. By default SQlite database is located at `$HOME/.Nextpie/nextpie-DB.sqlite3`. You can change the path by modifying the variable `SQLALCHEMY_DATABASE_URI ` in `config.py`.

