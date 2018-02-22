import csv
import re

from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point
from django.db import transaction

from base_station.models import BaseStation


class Command(BaseCommand):
    help = 'Imports base station data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', help='Location of the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        try:
            station_list = []
            with open(csv_file, 'r', encoding='iso-8859-1') as f:
                reader = csv.reader(f, delimiter=';')
                for row in reader:
                    if row[0] == 'Operadora':
                        continue
                    lat = re.match('(\d\d)([NS])[NS]?(\d\d)(\d\d)(\d*)', ''.join(row[5].split(',')))
                    lon = re.match('(\d\d)([EW])[EW]?(\d\d)(\d\d)(\d*)', ''.join(row[6].split(',')))
                    if not lat or not lon:
                        raise CommandError('Error on data: "{}"'.format(', '.join(row)))
                    lat_deg = int(lat.group(1)) +\
                              int(lat.group(3)) / 60 +\
                              float(lat.group(4) + "." + lat.group(5)) / 3600
                    if lat.group(2) == "S":
                        lat_deg = -lat_deg
                    lon_deg = int(lon.group(1)) +\
                              int(lon.group(3)) / 60 +\
                              float(lon.group(4) + "." + lon.group(5)) / 3600
                    if lon.group(2) == "W":
                        lon_deg = -lon_deg
                    pnt = Point(lon_deg, lat_deg)
                    station = BaseStation(operator=row[0], state=row[1], municipality=row[2], address=row[4], point=pnt)
                    station_list.append(station)
            with transaction.atomic():
                for s in station_list:
                    s.save()
            self.stdout.write(self.style.SUCCESS('Successfully imported base station data'))
        except FileNotFoundError:
            raise CommandError('File "{}" does not exist'.format(csv_file))

