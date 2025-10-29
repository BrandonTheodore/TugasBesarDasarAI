from typing import List

class Barang:
    def __init__(self, ID: str, ukuran: int):
        self.ID = ID
        self.ukuran = ukuran

    def __eq__(self, other):
        if not isinstance(other, Barang):
            return NotImplemented
        return self.value == other.value

    def __str__(self) -> str:
        return f"ID: {self.ID}n\Ukuran: {self.ukuran}"
    
class Container:
    def __init__(self, kapasitas: int):
        self.kapasitas = kapasitas
        self.daftar_barang: List[Barang] = []

    def add_barang(self, barang: Barang) -> bool:
        total_ukuran = self.hitung_ukuran() + barang.ukuran
        if total_ukuran <= self.kapasitas:
            self.daftar_barang.append(barang)
            return True
        return False
    
    def remove_barang(self, barang_keluar: Barang):
        for barang in self.daftar_barang:
            if barang.ID == barang_keluar:
                self.daftar_barang.remove(barang_keluar)

    def hitung_ukuran(self) -> int:
        return sum(barang.ukuran for barang in self.daftar_barang)
    
    def reset_container(self):
        self.daftar_barang: List[Barang] = []

    def has_barang(self, barang1: Barang) -> bool:
        for barang in self.daftar_barang:
            if barang.ID == barang1.ID:
                return True
        return False

    def __str__(self) -> str:
        return f"Container (Kapasitas: {self.kapasitas}, Terisi: {self.hitung_ukuran()})\nBarang: {[barang.ID for barang in self.daftar_barang]}"
