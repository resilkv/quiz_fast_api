
FROM python:3.11-slim-bullseye


WORKDIR /code


RUN apt-get update && \
    apt-get install -y gcc libpq-dev libffi-dev build-essential postgresql-client && \
    rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /code/requirements.txt

# Install all Python packages
RUN pip install --progress-bar=on --verbose --upgrade -r /code/requirements.txt


COPY ./app /code/app

COPY ./start.sh /code/start.sh
RUN chmod +x /code/start.sh

# Run the start script
CMD ["/code/start.sh"]
