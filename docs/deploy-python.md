

## 🐍 Running in a development mode

Before deploying Nextpie using Python in development mode, ensure that your system has the following installed:

- Python 3.9
- setuptools
- python3-dev (or python3-devel)
- libsqlite3-dev
- libbz2-dev
- git

>⚠️ Important Note: To deploy Nextpie with Python version 3.12 or higher, you must manually install `distutils`. This is because starting with Python 3.10, the `distutils` module was deprecated and completely removed from the standard library in Python `3.12`. Since Nextpie has not yet been tested on Python versions `3.10` and above, we cannot guarantee it will function correctly. Support for Python `3.10+` will be added in a future release.

If your system does not have Python `3.9` installed, please refer to the [instructions](python-from-source.md) on how to build Python `3.9` from source.

Run the following commands in your terminal to launch Nextpie in development mode with debugging enabled. If you prefer to run Nextpie as a Docker container with zero configuration, please skip this section and refer to the Docker execution instructions.

```bash
## Clone the repository
git clone https://github.com/bishwaG/Nextpie.git  
cd Nextpie  
  
## Create a virtual environment (Unix)
## Change python version or user only 'python3'
python3.9  -m venv env  
source env/bin/activate  
  
## Install modules - SQLite Database
pip3 install -r requirements/requirements.txt  
## OR with PostgreSQL_  
# pip install -r requirements/requirements-pgsql.txt
  
## Set the FLASK_APP environment variable (Unix/Mac)
export  FLASK_APP=run.py  
  
## Set up the DEBUG environment (Unix/Mac)
export  FLASK_DEBUG=1  
  
## Database setup and seeding if SQLite database file is not available
#flask db init
#flask db migrate -m "first"
#flask db upgrade
#flask seed
  
# Start the application (development mode)
# --host=0.0.0.0 - expose the app on all network interfaces (default 127.0.0.1)
# --port=5000 - specify the app port (default 5000)
flask run --host=127.0.0.1 --port=5000
```
Open your browser and go to [http://127.0.0.1:5000](http://127.0.0.1:5000). 

Use the default login credentials:

**Username:** admin
**Password:** admin
