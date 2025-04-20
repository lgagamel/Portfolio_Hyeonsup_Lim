# https://pypi.org/project/python-tsp/

import numpy as np
from python_tsp.exact import solve_tsp_dynamic_programming
from python_tsp.heuristics import solve_tsp_simulated_annealing
import itertools




def calculate_distance(p,dm):
    dist = 0
    for i in range(len(p)-1):
        dist = dist + dm[p[i],p[i+1]]
    return dist 
        
def exact_solution_keep_od(sub_distance_matrix):
    input_list = list(range(len(sub_distance_matrix)))
    input_list = input_list[1:-1]
    perm_list = list(itertools.permutations(input_list))
    perm_list = [[0]+list(x)+[len(sub_distance_matrix)-1] for x in perm_list]
    
    min_dist = np.inf
    best_perm = perm_list[0].copy()
    for perm in perm_list:        
        dist = 0
        for i in range(len(perm)-1):
            dist = dist + sub_distance_matrix[perm[i],perm[i+1]]
        if dist<min_dist:
            min_dist = dist
            best_perm = perm.copy() 
    return best_perm


# =============================================================================
# re-arrange output
# =============================================================================
def rearrange_solution(solution):
    solution = list(solution)
    ind = solution.index(0)
    solution = solution[ind:] + solution[:ind]    
    return solution

# =============================================================================
# update solution
# =============================================================================
def update_solution(i,prev_solution,distance_matrix,sub_solution_n):
    curr_solution = prev_solution[:i].copy()
    while len(curr_solution)<len(prev_solution):
        subset = prev_solution[i:i+sub_solution_n]
        sub_distance_matrix = distance_matrix[subset][:,subset].copy()
        sub_permutation = exact_solution_keep_od(sub_distance_matrix)
        sub_permutation = rearrange_solution(sub_permutation)
        subset = np.array(subset)
        tmp_solution = list(subset[sub_permutation])
        curr_solution = curr_solution + tmp_solution
        i = i + sub_solution_n
    curr_solution = curr_solution[:len(prev_solution)]
    return curr_solution



# =============================================================================
# final main
# =============================================================================
def tsp_main(distance_matrix,sub_solution_n=8):
    if len(distance_matrix)>10:
        # heuristic solution
        permutation, distance = solve_tsp_simulated_annealing(distance_matrix)
        
        # final update
        curr_solution = update_solution(0,permutation,distance_matrix,sub_solution_n)
        curr_solution = update_solution(int(sub_solution_n/2),curr_solution,distance_matrix,sub_solution_n)
        curr_solution = update_solution(0,curr_solution,distance_matrix,sub_solution_n)
        curr_solution = update_solution(int(sub_solution_n/2),curr_solution,distance_matrix,sub_solution_n)
        curr_solution = update_solution(0,curr_solution,distance_matrix,sub_solution_n)
    else:        
        curr_solution, distance = solve_tsp_dynamic_programming(distance_matrix)
    return curr_solution
