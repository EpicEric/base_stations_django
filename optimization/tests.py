import math
from django.contrib.gis.geos import Point
from unittest import TestCase, skip
from model_mommy import mommy
from scipy.optimize import minimize, basinhopping

from optimization.models import OptimizedBaseStation
from optimization.find_best_locations import OptimizeLocation
from optimization.taguchi import taguchi

from optimization.utils import timing

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
        solution = OptimizeLocation.slsqp(self.bs_inside, 2, self.bounds)
        self.assertEqual(len(solution), 2) # FIXME


class TaguchiTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        print(cls.__name__)

    @timing
    def test_himmelblaus(self):
        taguchi_result = taguchi([[-5,5],[-5,5]], 3, himmelblaus.symmetrical_function, 0.8)
        is_minimum_correct(taguchi_result['x'], himmelblaus.minimum)

    @timing
    def test_three_hump_camel(self):
        taguchi_result = taguchi([[-1.5,4],[-3,4]], 3, three_hump_camel.symmetrical_function, 0.8)
        is_minimum_correct(taguchi_result['x'], three_hump_camel.minimum)
    @timing
    def test_easom(self):
        taguchi_result = taguchi([[-1.5,4],[-3,4]], 3, easom.symmetrical_function, 0.8)
        is_minimum_correct(taguchi_result['x'], easom.minimum)
    @timing
    def test_mccormick(self):
        taguchi_result = taguchi([[-1.5,4],[-3,4]], 3, mccormick.symmetrical_function, 0.8)
        is_minimum_correct(taguchi_result['x'], mccormick.minimum)

class SlsqpTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        print(cls.__name__)

    @timing
    def test_himmelblaus(self):
        slsqp_result = minimize(fun = himmelblaus.function,
                                x0 = himmelblaus.initial_guess(),
                                method='SLSQP',
                                bounds=himmelblaus.domain,
                                options={'eps': 0.001})
        self.assertTrue(is_minimum_correct(slsqp_result.x, himmelblaus.minimum))

    @timing
    def test_three_hump_camel(self):
        slsqp_result = minimize(fun = three_hump_camel.function,
                                x0 = three_hump_camel.initial_guess(),
                                method='SLSQP',
                                bounds=three_hump_camel.domain,
                                options={'eps': 0.001})
        self.assertTrue(is_minimum_correct(slsqp_result.x, three_hump_camel.minimum))
    @skip("Do not work")
    @timing
    def test_easom(self):
        slsqp_result = minimize(fun = easom.function,
                                x0 = easom.initial_guess(),
                                method='SLSQP',
                                bounds=easom.domain,
                                options={'eps': 0.001})
        self.assertTrue(is_minimum_correct(slsqp_result.x, easom.minimum))
    @skip("Do not work")
    @timing
    def test_mccormick(self):
        slsqp_result = minimize(fun = mccormick.function,
                                x0 = [mccormick.initial_guess()],
                                method='SLSQP',
                                bounds=mccormick.domain,
                                options={'eps': 0.001})
        self.assertTrue(is_minimum_correct(slsqp_result.x, mccormick.minimum))


class OptimizationTestFunction():
    def __init__(self, function, domain, minimum):
        self.function = function
        self.domain = domain
        self.minimum = minimum

    def initial_guess(self):
        return [self.domain[0][0] + (self.domain[0][1] - self.domain[0][0]),
                self.domain[1][0] + (self.domain[1][1] - self.domain[1][0])]

    def symmetrical_function(self, x):
        return -(self.function(x))

himmelblaus = OptimizationTestFunction(
    function = lambda x: (x[0]**2 + x[1] - 11) ** 2 + (x[0] + x[1]**2 - 7) ** 2,
    domain = [[-5, 5], [-5, 5]],
    minimum = [[3,2], [-2.805118, 3.131312]])

three_hump_camel = OptimizationTestFunction(
    function = lambda x: 2 * x[0] * x[0] - 1.05*x[0]**4 + (x[0]**6)/6 + x[0]*x[1] + x[1]*x[1],
    domain = [[-5, 5], [-5, 5]],
    minimum = [[0,0]])

easom = OptimizationTestFunction(
    function = lambda x: -1 * math.cos(x[0])*math.cos(x[1])*math.e**(-((x[0] - math.pi)**2 + (x[1] - math.pi)**2)),
    domain = [[-100, 100], [-100, 100]],
    minimum = [[math.pi, math.pi]])

mccormick = OptimizationTestFunction(
    function = lambda x: math.sin(x[0] + x[1]) + (x[0]- x[1]) ** 2 - 1.5 * x[0] + 2.5 * x[1] + 1,
    domain = [[-1.5,4],[-3,4]],
    minimum = [[-0.54719, -1.54719]])

# eggholder = OptimizationTestFunction(
#     function = lambda x: -(x[1]+47)*math.sin(math.sqrt(abs(x[0]/2+x[1]+47)-x[0]*math.sin(math.sqrt(abs(x[0]-x[1]+47))))),
#     domain = [[-512, 512], [-512, 512]],
#     minimum = [[512, 404.2319]])

def is_close(x, y):
    epsilon = 1e-3
    return abs(x - y) < epsilon

def is_minimum_correct(calculated_minimum, minimum_set):
    is_minimum_x = False
    is_minimum_y = False
    for minimum in minimum_set:
        is_minimum_x = is_minimum_x or is_close(calculated_minimum[0], minimum[0])
        is_minimum_y = is_minimum_y or is_close(calculated_minimum[1], minimum[1])
    return is_minimum_x and is_minimum_y
