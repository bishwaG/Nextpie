## Gunicorn
---

[Gunicorn](https://gunicorn.org/) 'Green Unicorn' is a Python WSGI HTTP Server for UNIX based systems. If you have configured a software environment properly, it is already installed. Thus, there is no additional installation steps.

Run the following line in the terminal. Make sure that your software environment is active.

```bash
gunicorn --bind 0.0.0.0:8001 run:app
```

Open your browser and go to `http://localhost:5005`. Use username `admin` and password `admin` to login.
