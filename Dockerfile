FROM python:alpine3.11

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 5000

#ENV API_URL hotel_api:8000

CMD ["gunicorn", "server:app", "-b", "0.0.0.0:5000"]