from django.test import TestCase
from django.contrib.gis.geos import Point
from model_mommy import mommy

from base_station.models import IdentifiedBaseStation
from base_station.use_cases.find_best_locations import find_best_locations

class FindBestLocationsTestCase(TestCase):

    def setUp(self):
        self.bounds = ((-50, -40),(-25, -20))
        self.bs_inside = [
            mommy.make(IdentifiedBaseStation, point=Point(-46.5, -23.5)),
            mommy.make(IdentifiedBaseStation, point=Point(-44.22, -21.90)),
            mommy.make(IdentifiedBaseStation, point=Point(-40.0, -20.0))]

    def test_find_best_locations(self):
        # FIXME
        solution = find_best_locations(self.bs_inside, self.bounds)

        self.assertEqual(
            solution.message, 'Optimization terminated successfully.')
