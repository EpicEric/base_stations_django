import csv
import os
import re
from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point

from base_station.models import OwnedBaseStation, Operator
from geography.models import FederativeUnit


class Command(BaseCommand):
    help = 'Imports owned base station data from a Telebrasil CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', help='Location of the Telebrasil CSV file')

    def handle(self, *args, **options):
        csv_file = os.path.expanduser(options['csv_file'])
        try:
            new = 0
            unmodified = 0
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
                    station, created = OwnedBaseStation.objects.get_or_create(
                        operator=operator,
                        state=state,
                        municipality=row[2],
                        address=row[4],
                        defaults={
                            'point': pnt
                        })
                    if created:
                        new += 1
                    else:
                        unmodified += 1
            self.stdout.write(self.style.SUCCESS(
                'Successfully imported base station data ({} new, {} unmodified)'.format(
                    new, unmodified
                )))
        except FileNotFoundError:
            raise CommandError('File "{}" does not exist'.format(csv_file))
