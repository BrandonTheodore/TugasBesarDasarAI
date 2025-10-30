import random
import csv
import time
import copy
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict
import sys
import os
from ..core.entities import *
from ..core.state import *
from ..core.objective_function import *
from ..utils.parser import *
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

    def create_initial_population(self):
        self.population = []
        for _ in range(self.pop_size):
            state = State(self.list_barang)
            state.initiate_random(self.kapasitas)
            objective_function(state, self.kapasitas)
            self.population.append(state)

    def select_parent(self) -> State:
        tournament = random.sample(self.population, self.tournament_size)
        winner = min(tournament, key=lambda s: s.objective_function)
        return winner

    def crossover(self, parent1: State, parent2: State) -> State:
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

    def mutate(self, state: State):
        if random.random() < self.mutation_prob:
            mutation_type = random.randint(1, 2)
            if mutation_type == 1 and len(self.list_barang) >= 2:
                try:
                    b1, b2 = random.sample(self.list_barang, 2)
                    state.swap_barang(b1, b2)
                except ValueError:
                    self.mutate_move_to_empty(state)
            elif mutation_type == 2:
                self.mutate_move_to_empty(state)
            else:
                self.mutate_move_to_empty(state)
            objective_function(state, self.kapasitas)

    def mutate_move_to_empty(self, state: State):
        try:
            barang_to_move = random.choice(self.list_barang)
            state.move_to_empty(barang_to_move, self.kapasitas)
        except Exception:
            pass

    def get_best_individuals(self, n: int) -> List[State]:
        sorted_pop = sorted(self.population, key=lambda s: s.objective_function)
        return sorted_pop[:n]

    def record_history(self):
        best_fitness = min(s.objective_function for s in self.population)
        avg_fitness = sum(s.objective_function for s in self.population) / self.pop_size
        self.history_best_fitness.append(best_fitness)
        self.history_avg_fitness.append(avg_fitness)

    def run(self) -> Tuple[State, State, float, List[float], List[float]]:
        start_time = time.time()
        self.create_initial_population()
        initial_best_state = copy.deepcopy(self.get_best_individuals(1)[0])
        self.record_history()
        for _ in range(self.iterations):
            new_population = []
            elites = self.get_best_individuals(self.elitism_count)
            new_population.extend(copy.deepcopy(elite) for elite in elites)
            while len(new_population) < self.pop_size:
                parent1 = self.select_parent()
                parent2 = self.select_parent()
                child = self.crossover(parent1, parent2)
                self.mutate(child)
                new_population.append(child)
            self.population = new_population
            self.record_history()
        end_time = time.time()
        duration = end_time - start_time
        final_best_state = self.get_best_individuals(1)[0]
        return initial_best_state, final_best_state, duration, self.history_best_fitness, self.history_avg_fitness
    

def create_color_map(list_barang: List[Barang]) -> dict:
    colors = plt.cm.get_cmap('tab20', len(list_barang))
    color_map = {barang.ID: colors(i) for i, barang in enumerate(list_barang)}
    return color_map

def plot_comparative_fitness(comparison_results: List[Dict], title: str, var_name: str):
    plt.figure(figsize=(12, 7))
    
    summary_text = "--- Ringkasan Hasil Terbaik ---\n"
    
    for result in comparison_results:
        variation_value = result['variation_value']
        best_run_data = result['best_run_data']
        history = best_run_data['history_best']
        plt.plot(history, label=f"{var_name} = {variation_value} (OF Akhir: {best_run_data['of_akhir']:.2f})")
        
        summary_text += (
            f"  {var_name} = {variation_value}:\n"
            f"    OF Akhir Terbaik: {best_run_data['of_akhir']:.2f}\n"
            f"    OF Awal: {best_run_data['initial_state'].objective_function:.2f}\n"
            f"    Durasi (s): {best_run_data['duration']:.4f}\n"
        )

    plt.title(f"Perbandingan Fitness Progress - {title}")
    plt.xlabel("Iterasi (Generasi)")
    plt.ylabel("Nilai Objective Function (Lower is better)")
    plt.legend(loc='upper right')
    plt.grid(True, linestyle=':', alpha=0.7)
    
    plt.figtext(0.01, 0.01, summary_text, ha="left", va="bottom", fontsize=8, 
                bbox={"boxstyle": "round,pad=0.5", "facecolor": "lightgray", "alpha": 0.5})

    plt.tight_layout(rect=[0, 0.15, 1, 1])
    
    safe_filename = f"{title}_COMP_FITNESS.png"
    plt.savefig(safe_filename) 
    print(f"  Plot Fitness Komparatif disimpan sebagai: {safe_filename}")
    plt.show(block=False)
    plt.close()

def plot_comparative_states(comparison_results: List[Dict], state_type: str, title: str, var_name: str, kapasitas: int, color_map: dict):
    num_variations = len(comparison_results)
    
    fig, axes = plt.subplots(num_variations, 1, 
                             figsize=(12, num_variations * 4 + 2), 
                             sharex=True)
    
    if num_variations == 1:
        axes = [axes]

    fig.suptitle(f"Perbandingan State {state_type.title()} - {title}", fontsize=16, y=1.02)

    for i, result in enumerate(comparison_results):
        ax = axes[i] 
        variation_value = result['variation_value']
        
        if state_type == 'awal':
            state = result['best_run_data']['initial_state']
            ax_title = f"{var_name} = {variation_value} (State Awal, OF: {state.objective_function})"
        else:
            state = result['best_run_data']['final_state']
            ax_title = f"{var_name} = {variation_value} (State Akhir, OF: {state.objective_function})"
        
        ax.set_title(ax_title)
        containers = state.list_container
        if not containers:
            ax.text(0.5, 0.5, 'Tidak ada kontainer', ha='center', va='center', transform=ax.transAxes)
            continue

        container_names = [f"Kontainer {j+1}" for j in range(len(containers))][::-1]
        subplot_labels = set()
        
        for j, container in enumerate(reversed(containers)):
            container_name = container_names[j]
            left_offset = 0
            barang_sorted = sorted(container.daftar_barang, key=lambda b: b.ID)
            
            for barang in barang_sorted:
                color = color_map.get(barang.ID, 'gray')
                label = barang.ID if barang.ID not in subplot_labels else None
                if label: subplot_labels.add(label)
                
                ax.barh(container_name, barang.ukuran, left=left_offset, color=color, label=label)
                
                if barang.ukuran > 3: 
                    ax.text(left_offset + barang.ukuran / 2, container_name, barang.ID, 
                             ha='center', va='center', color='white', fontsize=8, fontweight='bold')
                left_offset += barang.ukuran

        ax.axvline(x=kapasitas, color='red', linestyle='--', label=f'Kapasitas ({kapasitas})' if 'Kapasitas' not in subplot_labels else None)
        ax.set_xlabel('Ukuran Terisi')
        ax.grid(axis='x', linestyle=':', alpha=0.6)
        
        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys(), bbox_to_anchor=(1.02, 1), loc='upper left')

    plt.tight_layout(rect=[0, 0, 0.85, 1]) # Beri ruang untuk legenda
    
    safe_filename = f"{title}_COMP_{state_type.upper()}_STATE.png"
    plt.savefig(safe_filename)
    print(f"  Plot State {state_type.title()} Komparatif disimpan sebagai: {safe_filename}")
    plt.show(block=False)
    plt.close(fig)



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

try:
    with open(input_file, "r") as f:
        json_input = f.read()
except FileNotFoundError:
    print(f"Error: File '{input_file}' not found.")
    sys.exit(1)

KAPASITAS_KONTAINER, LIST_BARANG = parse_input(json_input)
random.seed(42) 

COLOR_MAP = create_color_map(LIST_BARANG) 

print("--- EKSPERIMEN ALGORITMA GENETIKA (Plot Komparatif) ---")
print(f"--- Daftar Barang (Total {len(LIST_BARANG)} item, Kapasitas: {KAPASITAS_KONTAINER}) ---")
for barang in LIST_BARANG:
    print(f"  {barang.ID} (Ukuran: {barang.ukuran})")
print("-" * 50)

JUMLAH_RUN = 3
PROB_MUTASI_VARS = [0.05, 0.2] 
print("\n=== EKSPERIMEN 1: Iterasi Bervariasi (Populasi Kontrol) ===")
POP_KONTROL = 50
ITERASI_VARS = [50, 100, 200] 

for mut_prob in PROB_MUTASI_VARS:
    comparison_results = []
    plot_title = f"E1_Pop{POP_KONTROL}_Mut{mut_prob}"
    
    for iterasi in ITERASI_VARS:
        print(f"\n--- Konfigurasi: Pop={POP_KONTROL}, Iter={iterasi}, MutProb={mut_prob} ---")
        
        run_results = []
        for run in range(1, JUMLAH_RUN + 1):
            print(f"  == Run {run}/{JUMLAH_RUN} ==")
            
            ga = GeneticAlgorithm(LIST_BARANG, KAPASITAS_KONTAINER,
                                    pop_size=POP_KONTROL,
                                    iterations=iterasi,
                                    mutation_prob=mut_prob)
            
            initial, final, duration, hist_best, hist_avg = ga.run()
            print(f"     OF Awal: {initial.objective_function:.2f}, OF Akhir: {final.objective_function:.2f}, Durasi: {duration:.4f}s")

            run_results.append({
                'initial_state': initial, 'final_state': final, 'duration': duration,
                'history_best': hist_best, 'of_akhir': final.objective_function
            })
        best_run_data = min(run_results, key=lambda x: x['of_akhir'])
        comparison_results.append({
            'variation_value': iterasi,
            'best_run_data': best_run_data
        })
        print(f"  -> Hasil terbaik dari 3 run: OF Akhir = {best_run_data['of_akhir']:.2f}")
    print(f"\nMembuat plot komparatif untuk {plot_title}...")
    plot_comparative_fitness(comparison_results, plot_title, "Iterasi")
    plot_comparative_states(comparison_results, "awal", plot_title, "Iterasi", KAPASITAS_KONTAINER, COLOR_MAP)
    plot_comparative_states(comparison_results, "akhir", plot_title, "Iterasi", KAPASITAS_KONTAINER, COLOR_MAP)
print("\n\n=== EKSPERIMEN 2: Populasi Bervariasi (Iterasi Kontrol) ===")
ITERASI_KONTROL = 100
POPULASI_VARS = [20, 50, 100] 

for mut_prob in PROB_MUTASI_VARS:

    comparison_results = []
    plot_title = f"E2_Iter{ITERASI_KONTROL}_Mut{mut_prob}"

    for populasi in POPULASI_VARS:
        print(f"\n--- Konfigurasi: Pop={populasi}, Iter={ITERASI_KONTROL}, MutProb={mut_prob} ---")
        
        run_results = []
        for run in range(1, JUMLAH_RUN + 1):
            print(f"  == Run {run}/{JUMLAH_RUN} ==")
            
            ga = GeneticAlgorithm(LIST_BARANG, KAPASITAS_KONTAINER,
                                    pop_size=populasi,
                                    iterations=ITERASI_KONTROL,
                                    mutation_prob=mut_prob)
            
            initial, final, duration, hist_best, hist_avg = ga.run()
            print(f"     OF Awal: {initial.objective_function:.2f}, OF Akhir: {final.objective_function:.2f}, Durasi: {duration:.4f}s")
            
            run_results.append({
                'initial_state': initial, 'final_state': final, 'duration': duration,
                'history_best': hist_best, 'of_akhir': final.objective_function
            })
            
        best_run_data = min(run_results, key=lambda x: x['of_akhir'])
        comparison_results.append({
            'variation_value': populasi,
            'best_run_data': best_run_data
        })
        print(f"  -> Hasil terbaik dari 3 run: OF Akhir = {best_run_data['of_akhir']:.2f}")
        
    print(f"\nMembuat plot komparatif untuk {plot_title}...")
    plot_comparative_fitness(comparison_results, plot_title, "Populasi")
    plot_comparative_states(comparison_results, "awal", plot_title, "Populasi", KAPASITAS_KONTAINER, COLOR_MAP)
    plot_comparative_states(comparison_results, "akhir", plot_title, "Populasi", KAPASITAS_KONTAINER, COLOR_MAP)

print(f"\n\n--- Semua Eksperimen Selesai ---")
print(f"Semua plot komparatif telah disimpan sebagai file .png di folder 'src/'.")
print("Menampilkan semua plot...")
plt.show()