import math
import numpy as np

def orthogonal_array():
    return np.array([[1,1,1,2,2,2,3,3,3],[1,2,3,1,2,3,1,2,3],[1,2,3,2,3,1,3,1,2],[1,3,2,2,1,3,3,2,1]])

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

def taguchi(limits, s, objective, epsilon):
    params_qty = len(limits)        
    v = np.zeros(params_qty)
    beta = np.zeros(params_qty)
    #print("LIMITS:", limits)
    for i in range(len(limits)):
        v[i] = (limits[i][0] + limits[i][1])/2
        #print("v[i]", v[i])
        beta[i] = (limits[i][1] - limits[i][0])/(s + 1)
    
    oa = orthogonal_array()
    experiments_qty = len(oa[0])
    iterations = 0
    while any(abs(b) > 0.0001 for b in beta):
        iterations += 1
        parameter_array = np.zeros((params_qty, experiments_qty))
        level_to_parameter = np.zeros((params_qty, s))
        for i in range(params_qty):
            for x in set(oa[i]):
                level_to_parameter[i][x-1] = mapping_function(x, s, v[i], beta[i], limits[i][0], limits[i][1])
            parameter_array[i] = list(map(lambda x: level_to_parameter[i][x-1], oa[i]))
        #print("parameter_array", parameter_array)
        y = [objective(list(i)) for i in zip(*parameter_array)]
        #print("y", y)
        sn = [10 * math.log10(i*i) for i in y]
        sn_mean = np.zeros((len(oa), s))

        for i in range(params_qty):
            for j in range(experiments_qty):
                sn_mean[i][oa[i][j]-1] += s/len(sn) * sn[j]
        max_values_indexes = [0] * params_qty
        for i in range(params_qty):
            max_value = sn_mean[i][0]
            for j in range(1, s):
                if sn_mean[i][j] > max_value:
                    max_value = sn_mean[i][j]
                    max_values_indexes[i] = j
        v = [level_to_parameter[param_index][i] for param_index, i in enumerate(max_values_indexes)]
        beta = beta * epsilon
        #print("beta", beta)
    return {"iterations": iterations, "x": v}
