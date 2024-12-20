FROM python:3.11

WORKDIR /app

COPY requirements.txt .

ENV PYTHONUNBUFFERED=1

RUN pip install gunicorn

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
