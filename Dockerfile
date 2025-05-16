
FROM python:3.10-slim

COPY ./requirements.txt /tmp

RUN pip install --no-cache-dir -r /tmp/requirements.txt
WORKDIR /app/bin/
RUN mkdir -p /app/config/
RUN mkdir -p /app/data/
COPY ./src/ .


CMD ["python", "./", "/app/config/config.json", "/app/data/persons.json"]
