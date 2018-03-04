import csv
import os
import re
from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point
from django.db import transaction

from base_station.models import OwnedBaseStation, Operator
from geography.models import FederativeUnit


class Command(BaseCommand):
    help = 'Imports owned base station data from a Telebrasil CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', help='Location of the Telebrasil CSV file')

    def handle(self, *args, **options):
        csv_file = os.path.expanduser(options['csv_file'])
        try:
            station_list = []
            self.stdout.write('Reading data...')
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
                    operator, created = Operator.objects.get_or_create(
                        name=row[0],
                        defaults={'number': '', 'cnpj': '', 'fistel': ''}
                    )
                    if created:
                        self.stdout.write(self.style.WARNING(
                            'Automatically created operator: {}'.format(operator)))
                    state, created = FederativeUnit.objects.get_or_create(
                        short=row[1],
                        defaults={'name': ''}
                    )
                    if created:
                        self.stdout.write(self.style.WARNING(
                            'Automatically created FU: {}'.format(state)))
                    station = OwnedBaseStation(operator=operator, state=state, municipality=row[2], address=row[4], point=pnt)
                    station_list.append(station)
            self.stdout.write('Saving {} objects...'.format(len(station_list)))
            OwnedBaseStation.objects.bulk_create(station_list)
            self.stdout.write(self.style.SUCCESS('Successfully imported base station data'))
        except FileNotFoundError:
            raise CommandError('File "{}" does not exist'.format(csv_file))
