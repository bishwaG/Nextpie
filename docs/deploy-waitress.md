## Waitress
---

[Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/) (Gunicorn equivalent for Windows) is meant to be a production-quality pure-Python WSGI server with very acceptable performance. It has no dependencies except ones that live in the Python standard library.

> Install using pip

```bash
$ pip install waitress
```
> Start the app using [waitress-serve](https://docs.pylonsproject.org/projects/waitress/en/stable/runner.html)

```bash
$ waitress-serve --port=5000 run:app
Serving on http://localhost:5000
```

Open your browser and go to `http://localhost:5000`. Use username `admin` and password `admin` to login.

> NOTE: Nextipe is built to run under Linux. Theoritically it is possible to run under Windows, but it has not been tested. 
