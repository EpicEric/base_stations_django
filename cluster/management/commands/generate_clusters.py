from django.core.management import BaseCommand, CommandError

from cluster.models import MAX_CLUSTER_PRECISION_SIZE, BaseStationCluster


class Command(BaseCommand):
    help = 'Clears and re-generates all base station clusters'

    def add_arguments(self, parser):
        parser.add_argument('--yes', '-y', action='store_true', help='Automatic yes to cluster deletion prompts')
        pass

    def handle(self, *args, **options):
        assume_yes = options['yes']
        if BaseStationCluster.objects.all().exists() and not assume_yes:
            self.stdout.write('There are clusters currently in the database. '
                              'This command will delete all previous clusters.')
            result = input('Proceed? [y|n] ')
            while not result or result[0].lower() not in 'yn':
                result = input('Please answer [y]es or [n]o: ')
            if result[0].lower() != 'y':
                raise CommandError('Operation cancelled.')
        for precision in range(MAX_CLUSTER_PRECISION_SIZE, 0, -1):
            self.stdout.write(self.style.NOTICE('=== PRECISION {} ==='.format(precision)))
            previous = BaseStationCluster.objects.filter(precision=precision).delete()[0]
            if previous > 0:
                self.stdout.write(self.style.WARNING(
                    'Deleted {} previous clusters for precision {}'.format(previous, precision)))
            BaseStationCluster.generate_clusters(precision)
            self.stdout.write(self.style.NOTICE('==================='.format(precision)))
        self.stdout.write(self.style.SUCCESS('Done.'))
