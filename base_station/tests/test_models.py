from collections import Counter
from django.test import TestCase
from django.contrib.gis.geos import Point
from model_mommy import mommy

from base_station.models import IdentifiedBaseStation


class IdentifiedBaseStationTestCase(TestCase):

    def test_one_bs_inside_bounds(self):
        bs = mommy.make(IdentifiedBaseStation, point=Point(-46.5, -23.5))
        bs_within_box = IdentifiedBaseStation.get_base_stations_inside_bounds(
            -46, -23, -47, -24)

        self.assertEqual(bs_within_box.first(), bs)

    def test_some_bs_inside_and_some_outside_bounds(self):
        bs_inside = [
            mommy.make(IdentifiedBaseStation, point=Point(-46.5, -23.5)),
            mommy.make(IdentifiedBaseStation, point=Point(-46.2, -24.0)),
            mommy.make(IdentifiedBaseStation, point=Point(-46.0, -23.9))]
        bs_outside = [
            mommy.make(IdentifiedBaseStation, point=Point(-47.5, -23.5)),
            mommy.make(IdentifiedBaseStation, point=Point(46.2, -24.0)),
            mommy.make(IdentifiedBaseStation, point=Point(-46.3, -24.1))]
        bs_within_box = IdentifiedBaseStation.get_base_stations_inside_bounds(
            -46, -23, -47, -24)

        self.assertEqual(Counter(bs_within_box), Counter(bs_inside))

    def test_get_covered_area(self):
        #TODO
        pass
