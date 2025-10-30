from core.entities import *
from core.objective_function import *
from core.state import *
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

    def run(self, kapasitas):
        start = time.time

        self.initial_state.initiate_random(kapasitas)
        self.initial_state_value = objective_function(self.initial_state, kapasitas)
        self.neighbour_value = 0

        while True:

            neighbours: List[State] = self.initial_state.generate_neighbour()
            hitung_of(neighbours, kapasitas)
            neighbour: State = neighbours[0]
            for successor in neighbours:
                if neighbour.objective_function > successor.objective_function:
                    neighbour = successor
                    self.iteration += 1
            self.neighbour_value = neighbour.objective_function
            
            if self.neighbour_value >= self.initial_state_value:
                self.final_state = self.initial_state
                self.final_state_value = self.initial_state_value

                end = time.time()

                self.time_execution = (end - start) * 1000
                return self.initial_state
            
            self.initial_state = neighbour
            self.initial_state_value = neighbour.objective_function
            

        