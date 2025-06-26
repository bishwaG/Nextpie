## Gunicorn

[Gunicorn](https://gunicorn.org/), also known as “Green Unicorn,” is a Python WSGI HTTP server designed for UNIX-based systems. If your software environment is properly configured, Gunicorn should already be installed, so no additional installation steps should be necessary.

To run Gunicorn, make sure your software environment is active. If you haven’t created a virtual environment yet, you can create one with Python 3.9 (Unix example):

### ✅ Step 1: Create a virtual environment (if not done already): 
```bash
virtualenv -p python3.9 env
```
### ✅ Step 2: Activate the virtual environment: 
```bash
source env/bin/activate
```
### ✅ Step 3: Start the Gunicorn server by running: 
```bash
gunicorn --bind 127.0.0.1:5000 run:app
```
Open your browser and navigate to http://127.0.0.1:5000. Use the default credentials to log in:

**Username:** admin
**Password:** admin
