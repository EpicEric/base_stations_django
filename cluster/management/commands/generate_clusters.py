from django.core.management import BaseCommand

from cluster.models import MAX_CLUSTER_PRECISION_SIZE, BaseStationCluster


class Command(BaseCommand):
    help = 'Clears and re-generates all base station clusters'

    def add_arguments(self, parser):
        # parser.add_argument('csv_file', help='Location of the Telebrasil CSV file')
        pass

    def handle(self, *args, **options):
        # csv_file = os.path.expanduser(options['csv_file'])
        for precision in reversed(range(1, MAX_CLUSTER_PRECISION_SIZE + 1)):
            self.stdout.write(self.style.NOTICE('=== PRECISION {} ==='.format(precision)))
            previous = BaseStationCluster.objects.filter(precision=precision).delete()[0]
            if previous > 0:
                self.stdout.write(self.style.WARNING(
                    'Deleted {} previous clusters for precision {}'.format(previous, precision)))
            BaseStationCluster.generate_clusters(precision)
            self.stdout.write(self.style.NOTICE('==================='.format(precision)))
        self.stdout.write(self.style.SUCCESS('Done.'))
