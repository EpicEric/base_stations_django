# Production

http://159.89.46.207 or http://2604:a880:800:a1::9d4:8001

# Development

* Create and activate a Python 3 virtualenv `venv` in this directory.
* Run `pip install -r requirements.txt`.
* [Install PostGIS](https://postgis.net/install/) (+ GEOS, PROJ.4, GDAL; optional GeoIP).
* Create a file `django_project/config_settings.py` and set the following options:
```python
DEBUG = True

SECRET_KEY = 'some-secure-random-secret-key'

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'your-postgres-database',
        'USER': 'your-username',
        'PASSWORD': 'your-password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
* Set up the Postgres database to use the PostGIS extension:
```sql
CREATE EXTENSION postgis;
```
* Run `python manage.py makemigrations && python manage.py migrate`.
* (optional) Import base station data with `python manage.py import_base_stations file.csv`.
* Run `python manage.py runserver`.

