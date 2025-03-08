FROM python:3.11.0-slim-bullseye as build

RUN apt-get update && \
    apt-get install -y --no-install-recommends libsqlite3-mod-spatialite sqlite3 && \
    apt clean && \
    rm -rf /var/lib/apt && \
    rm -rf /var/lib/dpkg/info/*

RUN pip install https://github.com/simonw/datasette/archive/refs/tags/0.65.zip && \
    find /usr/local/lib -name '__pycache__' | xargs rm -r && \
    rm -rf /root/.cache/pip

RUN pip install requests dotenv sqlite_utils

RUN datasette install datasette-template-sql

COPY ./src /mnt

# if no data.db, create it from data.sql
RUN if [ ! -f /mnt/data.db ]; then sqlite3 /mnt/data.db < /mnt/data.sql; fi

EXPOSE 8001
CMD ["sh", "-c", "datasette --root -h 0.0.0.0 /mnt"]