import csv
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from base_station.models import IdentifiedBaseStation

BRASIL_MCC = '724'

class Command(BaseCommand):
    help = 'Imports base station data from a OpenCelliD CSV file'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file', help='Location of the OpenCelliD CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        try:
            station_list = []
            with open(csv_file, 'r', encoding='iso-8859-1') as f:
                reader = csv.reader(f, delimiter=',')
                for row in reader:
                    if row[1] == BRASIL_MCC:
                        point = Point(float(row[6]), float(row[7]))
                        station = IdentifiedBaseStation(
                            radio=row[0],
                            mcc=row[1],
                            mnc=row[2],
                            lac=row[3],
                            cid=row[4],
                            point=point,
                            averageSignal = row[13])
                        station_list.append(station)
            with transaction.atomic():
                for s in station_list:
                    s.save()
            self.stdout.write(self.style.SUCCESS(
                'Successfully imported base station data'))                        
        except FileNotFoundError:
            raise CommandError('File "{}" does not exist'.format(csv_file))
