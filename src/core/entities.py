from typing import List

class Barang:
    def __init__(self, ID: str, ukuran: int):
        self.ID = ID
        self.ukuran = ukuran

    def __str__(self) -> str:
        return f"ID: {self.ID}n\Ukuran: {self.ukuran}"
    
class Container:
    def __init__(self, kapasitas: int):
        self.kapasitas = kapasitas
        self.daftar: List[Barang] = []

    def add_barang(self, barang: Barang) -> bool:
        total_ukuran = self.hitung_ukuran() + barang.ukuran
        if total_ukuran <= self.kapasitas:
            self.daftar.append(barang)
            return True
        return False

    def hitung_ukuran(self) -> int:
        return sum(barang.ukuran for barang in self.daftar)

    def __str__(self) -> str:
        return f"Container (Kapasitas: {self.kapasitas}, Terisi: {self.hitung_ukuran()})\nBarang: {[barang.ID for barang in self.daftar]}"
