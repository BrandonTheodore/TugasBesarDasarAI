from ..core.entities import *
from ..core.objective_function import *
from ..core.state import *
from ..utils.parser import *
import time
import matplotlib.pyplot as plt
import numpy as np
import sys

class HCsteepest():
    def __init__(self, state: State):
        self.initial_state = state
        self.initial_state_value = 0
        self.final_state = None
        self.final_state_value = 0
        self.neighbours = None
        self.iteration = 0
        self.time_execution = 0
        self.objective_history = []

    def run(self, kapasitas, list_barang: List[Barang]):
        start = time.time()

        self.initial_state.initiate_random(kapasitas)
        objective_function(self.initial_state, kapasitas)
        self.initial_state_value = self.initial_state.objective_function
        print(f"Initial Value: {self.initial_state_value}")
        self.neighbour_value = 0

        while True:
            neighbours = self.initial_state.generate_neighbour(kapasitas)
            hitung_of(neighbours, kapasitas)
            neighbour = neighbours[0]

            best_neighbour = min(neighbours, key=lambda n: n.objective_function)
            best_value = best_neighbour.objective_function
            self.objective_history.append(best_value)
            self.iteration += 1
            for successor in neighbours[1:]:
                if neighbour.objective_function > successor.objective_function:
                    neighbour = successor

            objective_function(neighbour, kapasitas)
            self.neighbour_value = neighbour.objective_function
            
            if self.neighbour_value >= self.initial_state_value:
                self.final_state = self.initial_state
                self.final_state_value = self.initial_state_value

                end = time.time()

                self.time_execution = (end - start) * 1000
                plt.figure(figsize=(7, 4))
                plt.plot(range(len(self.objective_history)), self.objective_history, marker='o')
                plt.title("Objective Function vs Iteration")
                plt.xlabel("Iteration")
                plt.ylabel("Objective Function Value")
                plt.grid(True, linestyle="--", alpha=0.6)
                plt.tight_layout()
                plt.show()
                return self.initial_state
            
            self.initial_state = neighbour
            self.initial_state_value = neighbour.objective_function

    def visualize_state(self, state):
    
        container_sizes = [c.hitung_ukuran() for c in state.list_container]
        capacities = [c.kapasitas for c in state.list_container]

        n = len(container_sizes)
        container_labels = [f'C{i+1}' for i in range(n)]

        plt.figure(figsize=(8, 5))
        
        bars = plt.bar(container_labels, container_sizes, color='skyblue', label='Used Capacity')
        plt.hlines(capacities[0], -0.5, n - 0.5, colors='r', linestyles='dashed', label='Capacity')
        for bar, used, cap in zip(bars, container_sizes, capacities):
            if used > cap:
                bar.set_color('salmon')
        for i, (used, cap) in enumerate(zip(container_sizes, capacities)):
            plt.text(i, used + 2, f"{used}/{cap}", ha='center', fontsize=9)

        plt.title("Container Fill Level Visualization")
        plt.ylabel("Used Capacity")
        plt.xlabel("Container")
        plt.ylim(0, max(max(container_sizes), capacities[0]) * 1.2)
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.show()



if len(sys.argv) < 2:
    print("Usage: python main.py <input_file.json>")
    sys.exit(1)

input_file = sys.argv[1]

try:
    with open(input_file, "r") as f:
        json_input = f.read()
except FileNotFoundError:
    print(f"Error: File '{input_file}' not found.")
    sys.exit(1)

kapasitas, list_barang = parse_input(json_input)

state = State(list_barang)
state.initiate_random(kapasitas)
for barang in state.list_barang:
    print(barang)

hcsteep = HCsteepest(state)
hcsteep.run(kapasitas, list_barang)
print(f"time: {hcsteep.time_execution} ms\n")
print(f"iterasi: {hcsteep.iteration}\n")
print(f"final value: {hcsteep.final_state_value}")
hcsteep.visualize_state(hcsteep.initial_state)
hcsteep.visualize_state(hcsteep.final_state)






            

        