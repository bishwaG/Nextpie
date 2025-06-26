

## Waitress

[Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/) is a production-quality, pure-Python WSGI server designed for Windows, similar to Gunicorn on Unix systems. It offers good performance and has no dependencies beyond the standard Python library.

To install Waitress, run:
```bash
pip install waitress
```
Start the application with:
```bash
waitress-serve --port=5000 run:app
```
You should see: 
```
Serving on http://localhost:5000
```
Open your browser and navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000). Use the default credentials to log in:

**Username:** admin
**Password:** admin

> ⚠️ Note: Nextpie is primarily designed to run on Linux. While it may theoretically work on Windows using Waitress, this setup has not been tested.
