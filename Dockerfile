FROM python:3.9

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP run.py
ENV DEBUG True

RUN mkdir -p /root/nextpie

COPY requirements/requirements.txt /root/nextpie/requirements.txt

# install python dependencies


RUN ls -lah
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /root/nextpie/requirements.txt


COPY .env /root/nextpie/.env

COPY . /root/nextpie/

#RUN flask db init
#RUN flask db migrate
#RUN flask db upgrade
#RUN flask seed

WORKDIR "/root/nextpie/"
# gunicorn
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "run:app"]
