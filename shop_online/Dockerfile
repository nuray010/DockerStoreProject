FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /store_app

COPY requirements.txt /store_app/
RUN pip install --upgrade pip && \
    pip install -r req.txt

COPY nginx/nginx.conf /etc/nginx/conf.d/

COPY . /store_app/
