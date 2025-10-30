import random
import time
import matplotlib.pyplot as plt
from typing import List
import sys
import os
import csv
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from core.entities import Barang
from algorithm.genetic_algorithm import GeneticAlgorithm

def generate_barang() -> List[Barang]:
    list_of_barang = []
    for i in range(10): 
        barang = Barang(ID=f"BRG{i+1}", ukuran=random.randint(5, 50))
        list_of_barang.append(barang)
    return list_of_barang

def plot_fitness(history_best: List[float], history_avg: List[float], title: str):
    plt.figure(figsize=(10, 5))
    plt.plot(history_best, label='Nilai OF Terbaik (Terendah)', color='blue', linewidth=2)
    plt.plot(history_avg, label='Nilai OF Rata-rata Populasi', color='orange', linestyle='--')
    
    plt.title(f"Perkembangan Objective Function - {title}")
    plt.xlabel("Iterasi (Generasi)")
    plt.ylabel("Nilai Objective Function (Lower is better)")
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.tight_layout()
    
    safe_filename = title.replace(":", "").replace("=", "").replace(",", "_").replace(" ", "_") + ".png"
    plt.savefig(safe_filename) 
    print(f"  Plot disimpan sebagai: {safe_filename}")
    plt.close() 

if __name__ == "__main__":
    KAPASITAS_KONTAINER = 100
    random.seed(42) 
    LIST_BARANG = generate_barang() 

    print("--- EKSPERIMEN ALGORITMA GENETIKA ---")
    print(f"--- Daftar Barang (Total {len(LIST_BARANG)} item, Kapasitas: {KAPASITAS_KONTAINER}) ---")
    for barang in LIST_BARANG:
        print(f"  {barang.ID} (Ukuran: {barang.ukuran})")
    print("-" * 50)
    JUMLAH_RUN = 3
    PROB_MUTASI_VARS = [0.05, 0.2] 

    csv_filename = "hasil_eksperimen_ga.csv"
    csv_headers = [
        "Eksperimen", "Prob_Mutasi", "Populasi", "Iterasi", "Run", 
        "OF_Akhir", "Durasi_Detik", "OF_Awal", 
        "Nama_File_Plot", "State_Awal_Detail", "State_Akhir_Detail"
    ]

    with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers) 
        print("\n=== EKSPERIMEN 1: Iterasi Bervariasi (Populasi Kontrol) ===")
        POP_KONTROL = 50
        ITERASI_VARS = [50, 100, 200] 
        for mut_prob in PROB_MUTASI_VARS:
            for iterasi in ITERASI_VARS:
                print(f"\n--- Konfigurasi: Pop={POP_KONTROL}, Iter={iterasi}, MutProb={mut_prob} ---")
                for run in range(1, JUMLAH_RUN + 1):
                    print(f"\n== Run {run}/{JUMLAH_RUN} ==")
                    
                    ga = GeneticAlgorithm(LIST_BARANG, KAPASITAS_KONTAINER,
                                          pop_size=POP_KONTROL,
                                          iterations=iterasi,
                                          mutation_prob=mut_prob)
                    
                    initial, final, duration, hist_best, hist_avg = ga.run()
                    
                    print(f"  Durasi Proses: {duration:.4f} detik")
                    print(f"  State Awal (Best OF): {initial.objective_function}")
                    print(f"  State Akhir (Best OF): {final.objective_function}")

                    plot_title = f"E1_Run{run}_Pop{POP_KONTROL}_Iter{iterasi}_Mut{mut_prob}"
                    plot_fitness(hist_best, hist_avg, plot_title)
                    
                    data_row = [
                        1, mut_prob, POP_KONTROL, iterasi, run,
                        final.objective_function, round(duration, 4), initial.objective_function,
                        f"{plot_title}.png",
                        str(initial).replace("\n", " | "), 
                        str(final).replace("\n", " | ")
                    ]
                    writer.writerow(data_row)
        print("\n\n=== EKSPERIMEN 2: Populasi Bervariasi (Iterasi Kontrol) ===")
        ITERASI_KONTROL = 100
        POPULASI_VARS = [20, 50, 100] 
        
        for mut_prob in PROB_MUTASI_VARS:
            for populasi in POPULASI_VARS:
                print(f"\n--- Konfigurasi: Pop={populasi}, Iter={ITERASI_KONTROL}, MutProb={mut_prob} ---")
                for run in range(1, JUMLAH_RUN + 1):
                    print(f"\n== Run {run}/{JUMLAH_RUN} ==")
                    
                    ga = GeneticAlgorithm(LIST_BARANG, KAPASITAS_KONTAINER,
                                          pop_size=populasi,
                                          iterations=ITERASI_KONTROL,
                                          mutation_prob=mut_prob)
                    
                    initial, final, duration, hist_best, hist_avg = ga.run()

                    print(f"  Durasi Proses: {duration:.4f} detik")
                    print(f"  State Awal (Best OF): {initial.objective_function}")
                    print(f"  State Akhir (Best OF): {final.objective_function}")
                    
                    plot_title = f"E2_Run{run}_Pop{populasi}_Iter{ITERASI_KONTROL}_Mut{mut_prob}"
                    plot_fitness(hist_best, hist_avg, plot_title)
                    
                    data_row = [
                        2, mut_prob, populasi, ITERASI_KONTROL, run,
                        final.objective_function, round(duration, 4), initial.objective_function,
                        f"{plot_title}.png",
                        str(initial).replace("\n", " | "),
                        str(final).replace("\n", " | ")
                    ]
                    writer.writerow(data_row)