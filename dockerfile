FROM python:3.6-alpine 

COPY . /admin
WORKDIR /admin

RUN apk --no-cache add build-base
RUN apk --no-cache add postgresql-dev
RUN python3 -m pip install psycopg2

RUN pip install -r requirements.txt

CMD [ "gunicorn", "-w", "4", "-b", "0.0.0.0:2000", "--access-logfile", "-", "app:app" ]