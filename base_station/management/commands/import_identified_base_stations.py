import csv
import os
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand, CommandError

from base_station.models import IdentifiedBaseStation


BRAZIL_MCC = '724'

class Command(BaseCommand):
    help = 'Imports identified base station data from a OpenCelliD CSV file'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file', help='Location of the OpenCelliD CSV file')

    def handle(self, *args, **options):
        csv_file = os.path.expanduser(options['csv_file'])
        try:
            new = 0
            unmodified = 0
            self.stdout.write('Reading data...')
            with open(csv_file, 'r') as f:
                reader = csv.reader(f, delimiter=',')
                for row in reader:
                    if row[1] != BRAZIL_MCC:
                        continue
                    point = Point(float(row[6]), float(row[7]))
                    station, created = IdentifiedBaseStation.objects.get_or_create(
                        mcc=row[1],
                        mnc=row[2],
                        lac=row[3],
                        cid=row[4],
                        defaults={
                            'radio': row[0],
                            'point': point,
                            'average_signal': float(row[13]) or None
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
