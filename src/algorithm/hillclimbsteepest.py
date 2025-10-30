from ..core.entities import *
from ..core.objective_function import *
from ..core.state import *
import time

class HCsteepest():
    def __init__(self, state: State):
        self.initial_state = state
        self.initial_state_value = 0
        self.final_state = None
        self.final_state_value = 0
        self.neighbours = None
        self.iteration = 0
        self.time_execution = 0

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
                return self.initial_state
            
            self.initial_state = neighbour
            self.initial_state_value = neighbour.objective_function


list_barang = []
for i in range(100):
    barang = Barang(f"XX{i}", random.randint(1,100))
    list_barang.append(barang)

state = State(list_barang)
state.initiate_random(100)
for barang in state.list_barang:
    print(barang)

hcsteep = HCsteepest(state)
hcsteep.run(100, list_barang)
print(f"time: {hcsteep.time_execution}\n")
print(f"{hcsteep.final_state}\n")
print(f"iterasi: {hcsteep.iteration}\n")
print(f"final value: {hcsteep.final_state_value}")






            

        