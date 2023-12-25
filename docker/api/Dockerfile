FROM python:3.8

WORKDIR /pyapp/

COPY requirements.txt .

COPY .env .

COPY src ./src

RUN pip install --no-cache-dir --upgrade -r requirements.txt
