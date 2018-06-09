import math
from django.contrib.gis.geos import Point
from unittest import TestCase, skip
from model_mommy import mommy

from optimization.models import OptimizedBaseStation
from optimization.find_best_locations import OptimizeLocation
from optimization.numerical_methods import Basinhopping, SLSQP, Taguchi
from optimization.propagation_models import AreaOptimization

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
        optimizer = OptimizeLocation(
            self.bs_inside, self.bounds, SLSQP(), AreaOptimization().objective)
        solution = optimizer.find_best_locations()
        self.assertEqual(len(solution), 1) # FIXME


class TaguchiTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        print(cls.__name__)

    @timing
    def test_himmelblaus(self):
        taguchi_result = Taguchi().minimize(himmelblaus.symmetrical_function, himmelblaus.domain)
        self.assertTrue(is_minimum_correct(taguchi_result.x, himmelblaus.minimum))

    @timing
    def test_three_hump_camel(self):
        taguchi_result = Taguchi().minimize(three_hump_camel.symmetrical_function, three_hump_camel.domain)
        self.assertTrue(is_minimum_correct(taguchi_result.x, three_hump_camel.minimum))

    @timing
    def test_easom(self):
        taguchi_result = Taguchi().minimize(easom.symmetrical_function, easom.domain)
        self.assertTrue(is_minimum_correct(taguchi_result.x, easom.minimum))

    @timing
    def test_mccormick(self):
        taguchi_result = Taguchi().minimize(mccormick.symmetrical_function, mccormick.domain)
        self.assertTrue(is_minimum_correct(taguchi_result.x, mccormick.minimum))

    @skip("Do not work")
    @timing
    def test_schaffer4(self):
        taguchi_result = Taguchi().minimize(schaffer4.symmetrical_function, schaffer4.domain)
        self.assertTrue(is_minimum_correct(taguchi_result.x, schaffer4.minimum))

    @timing
    def test_matyas(self):
        taguchi_result = Taguchi().minimize(matyas.symmetrical_function, matyas.domain)
        self.assertTrue(is_minimum_correct(taguchi_result.x, matyas.minimum))


class BasinhoppingTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        print(cls.__name__)

    @timing
    def test_himmelblaus(self):
        basinhopping_result = Basinhopping().minimize(
            objective = himmelblaus.function,
            bounds = himmelblaus.domain,
            x0 = himmelblaus.initial_guess)

        self.assertTrue(is_minimum_correct(basinhopping_result.x, himmelblaus.minimum))

    @timing
    def test_three_hump_camel(self):
        basinhopping_result = Basinhopping().minimize(
            objective = three_hump_camel.function,
            bounds = three_hump_camel.domain,
            x0 = three_hump_camel.initial_guess)

        self.assertTrue(is_minimum_correct(basinhopping_result.x, three_hump_camel.minimum))

    @skip("Do not work")
    @timing
    def test_easom(self):
        basinhopping_result = Basinhopping().minimize(
            objective = easom.function,
            bounds = easom.domain,
            x0 = easom.initial_guess)
        self.assertTrue(is_minimum_correct(basinhopping_result.x, easom.minimum))

    @skip("Do not work")
    @timing
    def test_mccormick(self):
        basinhopping_result = Basinhopping().minimize(
            objective = mccormick.function,
            bounds = mccormick.domain,
            x0 = mccormick.initial_guess)
        self.assertTrue(is_minimum_correct(basinhopping_result.x, mccormick.minimum))

    @skip("Do not work")
    @timing
    def test_schaffer4(self):
        basinhopping_result = Basinhopping().minimize(
            objective = schaffer4.function,
            bounds = schaffer4.domain,
            x0 = schaffer4.initial_guess)
        self.assertTrue(is_minimum_correct(basinhopping_result.x, schaffer4.minimum))

    @timing
    def test_matyas(self):
        basinhopping_result = Basinhopping().minimize(
            objective = matyas.function,
            bounds = matyas.domain,
            x0 = matyas.initial_guess)
        self.assertTrue(is_minimum_correct(basinhopping_result.x, matyas.minimum))


class SlsqpTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        print(cls.__name__)

    @skip("Do not work")
    @timing
    def test_himmelblaus(self):
        slsqp_result = SLSQP().minimize(
            objective = himmelblaus.function,
            bounds = himmelblaus.domain,
            x0 = himmelblaus.initial_guess)

        self.assertTrue(is_minimum_correct(slsqp_result.x, himmelblaus.minimum))

    @timing
    def test_three_hump_camel(self):
        slsqp_result = SLSQP().minimize(
            objective = three_hump_camel.function,
            bounds = three_hump_camel.domain,
            x0 = three_hump_camel.initial_guess)
        self.assertTrue(is_minimum_correct(slsqp_result.x, three_hump_camel.minimum))

    @skip("Do not work")
    @timing
    def test_easom(self):
        slsqp_result = SLSQP().minimize(
            objective = easom.function,
            bounds = easom.domain,
            x0 = easom.initial_guess)
        self.assertTrue(is_minimum_correct(slsqp_result.x, easom.minimum))

    @skip("Do not work")
    @timing
    def test_mccormick(self):
        slsqp_result = SLSQP().minimize(
            objective = mccormick.function,
            bounds = mccormick.domain,
            x0 = mccormick.initial_guess)
        self.assertTrue(is_minimum_correct(slsqp_result.x, mccormick.minimum))

    @skip("Do not work")
    @timing
    def test_schaffer4(self):
        slsqp_result = SLSQP().minimize(
            objective = schaffer4.function,
            bounds = schaffer4.domain,
            x0 = schaffer4.initial_guess)
        self.assertTrue(is_minimum_correct(slsqp_result.x, schaffer4.minimum))

    @skip("Do not work")
    @timing
    def test_matyas(self):
        slsqp_result = SLSQP().minimize(
            objective = matyas.function,
            bounds = matyas.domain,
            x0 = matyas.initial_guess)
        self.assertTrue(is_minimum_correct(slsqp_result.x, matyas.minimum))


class OptimizationTestFunction():
    def __init__(self, function, domain, minimum):
        self.function = function
        self.domain = domain
        self.minimum = minimum

    @property
    def initial_guess(self):
        return [self.domain[0][0] + (self.domain[0][1] - self.domain[0][0]),
                self.domain[1][0] + (self.domain[1][1] - self.domain[1][0])]

    def symmetrical_function(self, x):
        return -(self.function(x))

himmelblaus = OptimizationTestFunction(
    function = lambda x: (x[0]**2 + x[1] - 11) ** 2 + (x[0] + x[1]**2 - 7) ** 2,
    domain = [[-5, 5], [-5, 5]],
    minimum = [[3,2], [-2.805118, 3.131312], [-3.779310, -3.283186]])

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

schaffer4 = OptimizationTestFunction(
    function = lambda x: 0.5 + ((math.cos(math.sin(abs(x[0]**2-x[1]**2))))**2-0.5)/((1+0.001*(x[0]**2+x[1]**2))**2),
    domain = [[-100, 100], [-100, 100]],
    minimum = [[0, 1.25313]])

matyas = OptimizationTestFunction(
    function = lambda x: 0.26*(x[0]**2+x[1]**2)-0.48*x[0]*x[1],
    domain = [[-10, 10], [-10, 10]],
    minimum = [[0,0]])

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
