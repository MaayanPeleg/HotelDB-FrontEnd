# HotelDB-FrontEnd
Here i make calls to the API and generate web pages
Run in DEV with:
```
flask --app serverapi run --debug
```
Run in PROD with:
```
gunicorn server:app -b 0.0.0.0:5000
```
