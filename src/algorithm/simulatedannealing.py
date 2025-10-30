import math
import time
import random
import copy
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, "../core")
from entities import Barang, Container
from state import State
from objective_function import objective_function

def generate_neighbour(list_of_barang, kapasitas):
    list_of_states = []
    for i in range ((len(list_of_barang) ** 2) - 1):
        state = State(list_of_barang)
        state.initiate_random(kapasitas)
        list_of_states.append(state)
    
    return list_of_states

def generate_barang():
    list_of_barang = []
    for i in range(10):
        barang = Barang(ID=f"BRG{i+1}", ukuran=random.randint(5, 50))
        list_of_barang.append(barang)
    
    return list_of_barang

def fitness_over_iteration(fitness_history):
    plt.figure(figsize=(8, 4))
    plt.plot(fitness_history, color='blue', linewidth=2)
    plt.title("Fitness Progress Over Iterations")
    plt.xlabel("Iteration")
    plt.ylabel("Fitness Value (Objective Function)")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

def delta_e_over_iteration(x):
    plt.figure(figsize=(8, 4))
    plt.plot(x, color='blue', linewidth=2)
    plt.title("Delta E / T Over Iterations")
    plt.xlabel("Iteration")
    plt.ylabel("e ^(-ΔE / T)")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

def local_optima(best_fitness, last_best_fitness, no_improve_steps, stuck_counter, stuck_threshold):
    if best_fitness < last_best_fitness:
        no_improve_steps = 0
        last_best_fitness = best_fitness
    else:
        no_improve_steps += 1
        if no_improve_steps >= stuck_threshold:
            stuck_counter += 1
            no_improve_steps = 0 

    return no_improve_steps, stuck_counter, last_best_fitness


def simulated_annealing(start_temp, end_temp, prob, iteration, list_of_barang):
    start = time.time()
    state = State(list_of_barang)
    state.initiate_random(kapasitas=100)
    objective_function(state, kapasitas=100)
    print(f"\nInitial Fitness: {state.objective_function}")
    print("Initial State:")
    for container in state.list_container:
        print(container)

    current = state
    current_fitness = state.objective_function

    best = copy.deepcopy(state)
    best_fitness = current_fitness

    list_of_states = generate_neighbour(list_of_barang, kapasitas=100)
    rand_state = random.choice(list_of_states)
    objective_function(rand_state, 100)

    fitness_history = [current_fitness]
    delta_e_history = []

    stuck_counter = 0
    no_improve_steps = 0
    stuck_threshold = 100
    last_best_fitness = best_fitness

    T = start_temp

    while T > end_temp:
        for i in range(iteration):
            new_state = random.choice(list_of_states)
            objective_function(new_state, 100)
            new_fitness = new_state.objective_function

            delta_e = new_fitness - current_fitness

            if delta_e < 0 or math.exp(-delta_e / T) > random.random():
                current = new_state
                current_fitness = new_fitness

                fitness_history.append(current_fitness)
                delta_e_history.append(math.exp(-delta_e / T))
                if current_fitness < best_fitness:
                    best = copy.deepcopy(current)
                    best_fitness = current_fitness

            no_improve_steps, stuck_counter, last_best_fitness = local_optima(best_fitness, last_best_fitness, no_improve_steps, stuck_counter, stuck_threshold)
        T *= prob
    end_time = time.time()
    execution_time = (end_time - start)
    fitness_over_iteration(fitness_history)
    delta_e_over_iteration(delta_e_history)
    print(f"\nTotal Stuck in Local Optima: {stuck_counter}")
    print(f"\nExecution Time: {execution_time:.4f} s")
    print(f"\nBest Fitness: {best_fitness}")
    return best.list_container

    
list_barang = generate_barang()
print("Daftar Barang:")
for barang in list_barang:
    print(barang)

best = simulated_annealing(start_temp=1000, end_temp=1, prob=0.995, iteration=100, list_of_barang=list_barang)

print("Best State Found:")
for container in best:
    print(container)