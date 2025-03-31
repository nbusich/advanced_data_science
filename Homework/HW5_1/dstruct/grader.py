import time

import numpy as np
import pandas as pd
import numpy.ma as ma
from sklearn import preprocessing as pre
import random as rnd
from evo import Evo
pd.set_option('future.no_silent_downcasting', True)

t_array = np.array(
        [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
         False]).reshape(1, 17)
f_array = np.array(
    [True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
     False]).reshape(1, 17)

def load_data():
    sec = pd.read_csv('sections.csv')
    ta = pd.read_csv('tas.csv')

    willing = ta[
        ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']].to_numpy()
    willing = np.where(willing == 'U', 0, np.where(willing == 'W', 1, 2)).astype(np.uint8)

    required = sec[['min_ta']].T.to_numpy(dtype = 'uint8')

    avail = ta['max_assigned'].to_numpy(dtype = 'uint8')

    unique_times = set(sec['daytime'])
    time_codes = list(range(1, len(unique_times)+1))
    sec.replace(to_replace= unique_times, value = time_codes, inplace=True)
    timeslots = sec['daytime'].to_numpy(dtype = 'uint8')
    timeslots = np.expand_dims(timeslots, axis = 1)
    timeslots = pre.OneHotEncoder(sparse_output=False, dtype = 'uint8').fit_transform(timeslots)
    return willing, required, avail, timeslots

def overallocation(solution):
    oa = avail - solution.sum(axis=1)
    oa[oa > 0] = 0
    return abs(oa.sum())

def conflicts(solution):
    # Schedule must be [Sections, Positional section code]
    ss = solution @ timeslots
    mask = np.where(ss>1, 1, 0)
    return mask.sum()

def under_support(solution):
    us = solution.sum(axis=0) - required
    us[us > 0] = 0
    return abs(us.sum())

def unwilling(solution):
    mask = np.where(willing == 0, False, True) # 0=U
    uw = ma.masked_array(solution, mask)
    return uw.sum()

def un_preferred(solution):
    mask = np.where(willing == 1, False, True) # 1=W
    up = ma.masked_array(solution, mask)
    return up.sum()

def total_grade(solution):
    return un_preferred(solution)+unwilling(solution)+under_support(solution)+conflicts(solution)+overallocation(solution)

def start_array():
    starting_array = np.zeros(shape=[43,17], dtype = 'float64')
    for i in range(len(avail)):
        if avail[i] > 0:
            indices = rnd.sample(range(starting_array.shape[1]), avail[i])
            starting_array[i, indices] = 1
    return starting_array

def agent1(solutions):
    """ Swap two random values in the ONE solution provided """
    L = solutions[rnd.randrange(0, len(solutions))]
    i = rnd.randrange(0, len(L))
    j = rnd.randrange(0, len(L))
    L[i], L[j] = L[j], L[i]
    return L

def agent2(solutions):
    """"""
    solution = solutions[0]
    mask = np.where(willing == 0, False, True)  # 0=U
    z = ma.masked_array(solution, mask)
    indices = np.argwhere(z == 1)
    mod_indices = (indices + [[0,1]]) % [[43,17]]
    solution[tuple(indices.T)] = 0
    solution[tuple(mod_indices.T)] = 1
    return solution

def agent3(solutions):
    solution = solutions[0]
    mask = np.where(willing == 1, False, True)  # 0=U
    z = ma.masked_array(solution, mask)
    indices = np.argwhere(z == 1)
    mod_indices = (indices + [[0, 1]]) % [[43, 17]]
    solution[tuple(indices.T)] = 0
    solution[tuple(mod_indices.T)] = 1
    return solution

def agent4(solution):
    """Set value to one randomly to rows with a sum that is less than the corresponding avail value"""
    solutions = solution[0]
    # Mask rows that have a sum that equals available
    np.random.shuffle(f_array)
    condition = (avail - solutions.sum(axis=1)) > 0
    condition = np.expand_dims(condition, axis = 1)
    b_condition = np.broadcast_to(condition, (43,17))
    mask = np.where(b_condition, f_array, t_array)
    result = ma.masked_array(solutions, mask).filled(1)
    return result

willing, required, avail, timeslots = load_data()


def main():
    init_time = time.time()
    a = start_array()
    print("Initial total grade:", total_grade(a))

    E = Evo()
    E.add_fitness_criteria("TotalGrade", total_grade)
    E.add_fitness_criteria("Overallocation", overallocation)
    E.add_fitness_criteria("Undersupport", under_support)
    E.add_fitness_criteria("Conflicts", conflicts)
    E.add_fitness_criteria("Unwilling", unwilling)
    E.add_fitness_criteria("Unpreferred", un_preferred)

    E.add_agent("agent1", agent1, k=1)
    E.add_agent("un_pref_reducer0", agent2, k=1)
    E.add_agent("un_will_reducer0", agent3, k=1)
    E.add_agent("adder1", agent4, k=1)


    E.add_solution(a)
    best_solution = E.evolve(n=500000, dom=100, status=100000)
    np.savetxt("best_array_3.csv", best_solution, delimiter=",", fmt="%d")
    end_time = time.time()
    print("Time taken:", end_time - init_time)
    print("Final overallocation score:", overallocation(best_solution))
    print("Final conflicts score:", conflicts(best_solution))
    print("Final under support score:", under_support(best_solution))
    print("Final unwilling score:", unwilling(best_solution))
    print("Final un_preferred score:", un_preferred(best_solution))
    print("Final Overall Grade:", total_grade(best_solution))
if __name__ == '__main__':
    main()