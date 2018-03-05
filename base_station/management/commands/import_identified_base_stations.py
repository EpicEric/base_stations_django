import csv
import os
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand, CommandError

from base_station.models import IdentifiedBaseStation

BRASIL_MCC = '724'

class Command(BaseCommand):
    help = 'Imports identified base station data from a OpenCelliD CSV file'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file', help='Location of the OpenCelliD CSV file')

    def handle(self, *args, **options):
        csv_file = os.path.expanduser(options['csv_file'])
        try:
            station_list = []
            self.stdout.write('Reading data...')
            with open(csv_file, 'r') as f:
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
                            averageSignal=float(row[13]) or None)
                        station_list.append(station)
            self.stdout.write('Saving {} objects...'.format(len(station_list)))
            IdentifiedBaseStation.objects.bulk_create(station_list)
            self.stdout.write(self.style.SUCCESS(
                'Successfully imported base station data'))                        
        except FileNotFoundError:
            raise CommandError('File "{}" does not exist'.format(csv_file))
