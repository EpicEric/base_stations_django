from django.test import TestCase
from django.contrib.gis.geos import Point
from model_mommy import mommy

from optimization.models import OptimizedBaseStation
from optimization.find_best_locations import find_best_locations


class FindBestLocationsTestCase(TestCase):
    def setUp(self):
        self.bounds = ((-50, -20), (-60, -30))
        self.bs_inside = [
            mommy.make(OptimizedBaseStation, point=Point(-46.5, -23.5)),
            mommy.make(OptimizedBaseStation, point=Point(-50.22, -45.90)),
            mommy.make(OptimizedBaseStation, point=Point(-50.0, -60.0)),
            mommy.make(OptimizedBaseStation, point=Point(-20.0, -44.5)),
            mommy.make(OptimizedBaseStation, point=Point(-20.0, -43.8))]

    def test_find_best_locations(self):
        solution = find_best_locations(self.bs_inside, 2, self.bounds)
        self.assertEqual(
            solution.message, 'Optimization terminated successfully.')
