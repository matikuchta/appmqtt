
FROM python:3.10-slim
WORKDIR /app/bin/
RUN mkdir -p /app/config/
RUN mkdir -p /app/data/
COPY ./src/ .
COPY ./requirements.txt /tmp

RUN pip install --no-cache-dir -r /tmp/requirements.txt

CMD ["python", "./", "/app/config/config.json"]
