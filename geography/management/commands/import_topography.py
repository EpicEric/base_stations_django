import csv
import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point
from django.db import transaction

from geography.models import Topography


class Command(BaseCommand):
    help = 'Imports topographic data from directory'

    def add_arguments(self, parser):
        parser.add_argument(
            'topography_directory',
            help='Location of directory of topographic files')

    def handle(self, *args, **options):
        topography_directory = os.path.expanduser(options['topography_directory'])
        try:
            topography_list = []
            topography_files = filter(lambda x: x[-4:] == '.txt',
                                  map(lambda x: topography_directory + '/' + x,
                                      os.listdir(topography_directory)))
            self.stdout.write('Reading data...')
            for topography_file in topography_files:
                with open(topography_file, 'r') as f:
                    content = f.readlines()
                    for line in content:
                        c = line.split()
                        if len(c) == 3:
                            point = Point(float(c[0]), float(c[1]))
                            t = Topography(point=point, altitude=int(float(c[2])))
                            topography_list.append(t)
            self.stdout.write('Saving {} objects...'.format(len(topography_list)))
            Topography.objects.bulk_create(topography_list)
            self.stdout.write(self.style.SUCCESS(
                'Successfully imported topographic data'))
        except FileNotFoundError:
            raise CommandError('Could not import topographic data')
