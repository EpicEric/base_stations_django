# Production

* **HTTPS** - https://tcc.ericpires.com.br/
* **SSH** - `ssh root@159.89.46.207` or `ssh -6 root@2604:a880:800:a1::9d4:8001`

## Deploying to production

* Adding remote:
```sh
git remote add production root@159.89.46.207:deploy
```

* Deploying to remote:
```sh
git push production master
```

# Development

* Create and activate a Python 3 virtualenv `venv` in this directory.
* Run `pip install -r requirements.txt`.
* [Install PostGIS](https://postgis.net/install/) (+ GEOS, PROJ.4, GDAL, GeoIP2).
* Create a file `django_project/config_settings.py` and set the following options:
```python
DEBUG = True

SECRET_KEY = 'some-secure-random-secret-key'
# You can generate a new key as follows:
# >>> import random
# >>> ''.join(random.SystemRandom() \
#       .choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') \
#       for i in range(50))

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
* (optional) Import all pertinent data:
```sh
python manage.py import_owned_base_stations file.csv
python manage.py import_identified_base_stations file.csv
python manage.py import_topography directory
```
* (optional) Create an admin user with `python manage.py createsuperuser`.
* Collect static files with `python manage.py collectstatic --noinput`.
* (optional) Download and extract the `.mmdb` Country and City files from [MaxMind](https://dev.maxmind.com/geoip/geoip2/geolite2/) into `static/geoip2`.
* Run `python manage.py runserver`.
