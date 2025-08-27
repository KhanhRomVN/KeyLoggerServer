FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN mkdir -p data/logs data/database

EXPOSE 5000
EXPOSE 443

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--certfile", "config/ssl/server.crt", "--keyfile", "config/ssl/server.key", "src.main:app"]