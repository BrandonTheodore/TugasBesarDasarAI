# Tugas Besar IF3070 - Dasar Artificial Intelligence

## Deskripsi

> Repository ini ditujukan untuk memenuhi Tugas Besar Dasar Artificial Intelligence IF3070 tahun ajaran 2025/2026

Repo ini berisi 3 algoritma local search dalam topik Searching pada Artificial Intelligence. Algoritma terdiri dari Steepest Hill Climbing, Simulated Annealing, dan Genetic Algorithm, algoritma yang dibuat akan digunakan untuk menyelesaikan permasalahan Knapsack.

## Anggota Kelompok

**Kelompok 42 :**

| NIM          | Nama                       |
| ---          | ---                        |
| 18223020     | Brandon Theodore F.        |
| 18223038     | Rafli Dwi Nugraha          |
| 18223041     | Luckman Fakhmanidris A.    |

## Setup dan Run Program
1. Buat Virtual Environment (Opsional)
```
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
```

2. Install Dependency
```
pip install -r requirements.txt
```

3. Pastikan file input berada di root directory

- Untuk Simulated Annealing
```
python -m src.algorithm.simulatedannealing <input>.json
```

- Untuk Hill Climbing
```
python -m src.algorithm.hillclimbsteepest <input>.json 
```

- Untuk Genetic Algorithm
```
python -m src.algorithm.genetic_algorithm <input>.json 
```
## Pembagian Tugas

| Nama                    | NIM          | Tugas                                            |
| ---                     | ---          | ---                                              |
| Brandon Theodore F.     | 18223020     | - Membuat algoritma simulated annealing          |
|                         |              | - Membuat repository github                      |
|                         |              | - Membuat template dokumen laporan               |
|                         |              | - Mengerjakan laporan bagian simulated annealing |
|                         |              | - Debugging Objective Function                   |
| Rafli Dwi Nugraha       | 18223038     | - Membuat algoritma hill climbing                |
|                         |              | - Membuat objective function                     |
|                         |              | - Membuat class State, Barang, dan Container     |
|                         |              | - Mengerjakan laporan bagian hill climbing       |
| Luckman Fakhmanidris A. | 18223041     | - Membuat algoritma genetic                      |
|                         |              | - Mengerjakan laporan bagian genetic algorithm   |


