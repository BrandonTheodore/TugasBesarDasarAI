import random
import time
import copy
import matplotlib.pyplot as plt
from typing import List, Tuple
import sys
import os
from core.entities import *
from core.state import *
from core.objective_function import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class GeneticAlgorithm:
    def __init__(self, list_barang: List[Barang], kapasitas: int,
                 pop_size: int, iterations: int,
                 mutation_prob: float, 
                 tournament_size: int = 3, elitism_count: int = 1):
        
        self.list_barang = list_barang
        self.kapasitas = kapasitas
        self.pop_size = pop_size
        self.iterations = iterations
        self.mutation_prob = mutation_prob
        self.tournament_size = tournament_size
        self.elitism_count = elitism_count
        
        self.population: List[State] = []
        self.history_best_fitness: List[float] = []
        self.history_avg_fitness: List[float] = []

    def _create_initial_population(self):
        self.population = []
        for _ in range(self.pop_size):
            state = State(self.list_barang)
            state.initiate_random(self.kapasitas)
            objective_function(state, self.kapasitas)
            self.population.append(state)

    def _select_parent(self) -> State:
        tournament = random.sample(self.population, self.tournament_size)
        winner = min(tournament, key=lambda s: s.objective_function)
        return winner

    def _crossover(self, parent1: State, parent2: State) -> State:
        child = copy.deepcopy(parent2)
        if not parent1.list_container:
            return child
        
        container_to_inject = random.choice(parent1.list_container)
        items_in_container = {b.ID for b in container_to_inject.daftar_barang}

        new_child_containers: List[Container] = []
        for container in child.list_container:
            items_to_keep = [b for b in container.daftar_barang if b.ID not in items_in_container]
            if items_to_keep:
                new_container = Container(self.kapasitas)
                for item in items_to_keep:
                    new_container.add_barang(item)
                new_child_containers.append(new_container)
        
        new_child_containers.append(copy.deepcopy(container_to_inject))
        child.list_container = new_child_containers
        objective_function(child, self.kapasitas)
        return child

    def _mutate(self, state: State):
        if random.random() < self.mutation_prob:
            mutation_type = random.randint(1, 2)
            if mutation_type == 1 and len(self.list_barang) >= 2:
                try:
                    b1, b2 = random.sample(self.list_barang, 2)
                    state.swap_barang(b1, b2)
                except ValueError:
                    self._mutate_move_to_empty(state)
            elif mutation_type == 2:
                self._mutate_move_to_empty(state)
            else:
                self._mutate_move_to_empty(state)
            objective_function(state, self.kapasitas)

    def _mutate_move_to_empty(self, state: State):
        try:
            barang_to_move = random.choice(self.list_barang)
            state.move_to_empty(barang_to_move, self.kapasitas)
        except Exception:
            pass

    def _get_best_individuals(self, n: int) -> List[State]:
        """Mendapatkan n individu terbaik (OF terendah) dari populasi."""
        sorted_pop = sorted(self.population, key=lambda s: s.objective_function)
        return sorted_pop[:n]

    def _record_history(self):
        best_fitness = min(s.objective_function for s in self.population)
        avg_fitness = sum(s.objective_function for s in self.population) / self.pop_size
        self.history_best_fitness.append(best_fitness)
        self.history_avg_fitness.append(avg_fitness)

    def run(self) -> Tuple[State, State, float, List[float], List[float]]:
        start_time = time.time()
        self._create_initial_population()
        initial_best_state = copy.deepcopy(self._get_best_individuals(1)[0])
        self._record_history()
        
        for _ in range(self.iterations):
            new_population = []
            elites = self._get_best_individuals(self.elitism_count)
            new_population.extend(copy.deepcopy(elite) for elite in elites)
            while len(new_population) < self.pop_size:
                parent1 = self._select_parent()
                parent2 = self._select_parent()
                child = self._crossover(parent1, parent2)
                self._mutate(child)
                new_population.append(child)
            self.population = new_population
            self._record_history()
        
        end_time = time.time()
        duration = end_time - start_time
        final_best_state = self._get_best_individuals(1)[0]
        
        return initial_best_state, final_best_state, duration, self.history_best_fitness, self.history_avg_fitness