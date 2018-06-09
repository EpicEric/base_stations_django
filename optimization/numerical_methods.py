import math
from scipy.optimize import basinhopping
from scipy.optimize import minimize
import numpy as np


class Basinhopping():

    def minimize(self, objective, bounds, x0):
        minimizer_kwargs = {"method":"L-BFGS-B", "bounds": bounds}
        solution = basinhopping(objective,
                                x0,
                                minimizer_kwargs=minimizer_kwargs,
                                niter=10)
        return solution


class SLSQP():

    def minimize(self, objective,  bounds, x0):
        solution = minimize(objective,
                            x0,
                            method='SLSQP',
                            bounds=bounds,
                            options={'eps': 0.1})
        return solution


class Taguchi():

    def minimize(self, objective, bounds, x0=None):
        solution = self.taguchi(bounds, 3, objective, 0.9)
        return solution

    @staticmethod
    def orthogonal_array(params_qty):
        if params_qty == 2:
            return np.array([[1,1,1,2,2,2,3,3,3], [1,2,3,1,2,3,1,2,3]])
        elif params_qty == 4:
            return np.array([[1,1,1,2,2,2,3,3,3],[1,2,3,1,2,3,1,2,3],[1,2,3,2,3,1,3,1,2],[1,3,2,2,1,3,3,2,1]])

    @staticmethod
    def mapping_function(level, s, v, beta, min_value, max_value):
        if 1 <= level and level <= math.ceil(s/2) -1:       
            mapped_value = v - (math.ceil(s/2) - level) * beta
            if mapped_value < min_value:
                mapped_value = min_value + (level - 1) * ((v - min_value) /  (math.ceil(s/2) - 1))
        elif level == math.ceil(s/2):
            mapped_value = v
        else:
            mapped_value = v + (level - math.ceil(s/2)) * beta
            if mapped_value > max_value:
                mapped_value = v + (level - math.ceil(s/2)) * ((max_value - v) / (math.ceil(s/2) - 1))
        return mapped_value

    def taguchi(self, limits, s, objective, epsilon):
        params_qty = len(limits)        
        v = np.zeros(params_qty)
        beta = np.zeros(params_qty)

        for i in range(len(limits)):
            v[i] = (limits[i][0] + limits[i][1])/2
            beta[i] = (limits[i][1] - limits[i][0])/(s + 1)
        
        oa = Taguchi.orthogonal_array(params_qty)
        experiments_qty = len(oa[0])
        iterations = 0
        while any(b > 0.001 for b in beta):
            iterations += 1
            parameter_array = np.zeros((params_qty, experiments_qty))
            level_to_parameter = np.zeros((params_qty, s))
            for i in range(params_qty):
                for x in set(oa[i]):
                    level_to_parameter[i][x-1] = Taguchi.mapping_function(x, s, v[i], beta[i], limits[i][0], limits[i][1])
                parameter_array[i] = list(map(lambda x: level_to_parameter[i][x-1], oa[i]))

            y = [objective(list(i)) for i in zip(*parameter_array)]
            #sn = [10 * math.log10(i*i) for i in y]
            sn = y
            sn_mean = np.zeros((len(oa), s))

            for i in range(params_qty):
                for j in range(experiments_qty):
                    sn_mean[i][oa[i][j]-1] += s/len(sn) * sn[j]
            min_values_indexes = [0] * params_qty
            for i in range(params_qty):
                min_value = sn_mean[i][0]
                for j in range(1, s):
                    if sn_mean[i][j] < min_value:
                        min_value = sn_mean[i][j]
                        min_values_indexes[i] = j
            v = [level_to_parameter[param_index][i] for param_index, i in enumerate(min_values_indexes)]
            beta = beta * epsilon
        return TaguchiResult(fun = objective(v), nit = iterations, x = v)

class TaguchiResult():
    def __init__(self, fun, nit, x):
        self.fun = fun
        self.nit = nit
        self.x = x
