import csv
import re
import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point
from django.db import transaction

from base_station.models import Topography


class Command(BaseCommand):
    help = 'Imports topographic data from directory'

    def add_arguments(self, parser):
        parser.add_argument(
            'topography_directory',
            help='Location of directory of topographic files')

    def handle(self, *args, **options):
        topography_directory = options['topography_directory']
        topography_list = list()
        try:
            topography_files = map(lambda x: topography_directory + x,
                                   os.listdir(topography_directory))
            for topography_file in topography_files:
                with open(topography_file, 'r') as f:
                    content = f.readlines()
                    for line in content:
                        c = line.split()
                        if len(c) == 3:
                            point = Point(float(c[0]), float(c[1]), float(c[2]))
                            t = Topography(point=point)
                            topography_list.append(t)
            with transaction.atomic():
                for t in topography_list:
                    t.save()
            self.stdout.write(self.style.SUCCESS(
                'Successfully imported topographic data'))
        except FileNotFoundError:
            raise CommandError('Could not import topographic data')
