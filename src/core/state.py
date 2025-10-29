from src.core.entities import *
import random

class State:
    def __init__(self, list_barang: list[Barang], list_container: list[Container], objective_function, kapasitas: int):
        self.list_barang = list_barang
        self.list_container = list_container
        self.objective_function = objective_function


    def initiate_random(self, kapasitas: int):
        random.shuffle(self.list_barang)

        kontainer = kontainer(kapasitas)
        total_ukuran = 0
        for barang in self.list_barang:
            if total_ukuran + self.list_barang.ukuran > self.kapasitas:
                self.list_container.append(kontainer)
                kontainer.reset_container()
                total_ukuran = 0
            
            kontainer.add_barang(barang)
            total_ukuran += barang.ukuran

        self.list_container.append(kontainer)

    def move_exist(self, barang: Barang, kontainer1: Container, kontainer2: Container):
        if kontainer1.hitung_ukuran() + barang.ukuran > kontainer1.kapasitas:
            raise ValueError("Barang Melebihi Kapasitas")
        kontainer1.add_barang(barang)
        kontainer2.remove_barang(barang)

    def move_to_empty(self, barang:Barang, kapasitas:int):
        newcontainer = Container(kapasitas)
        newcontainer.add_barang(barang)
        self.list_container.append(newcontainer)
        for kontainer in self.list_container:
            kontainer.remove_barang(barang)


    def swap_barang(self, barang1: Barang, barang2: Barang):
        cukup1 = False
        cukup2 = False
        for container in self.list_container:
            if container.has_barang(barang1):
                if container.hitung_ukurang() - barang1.ukuran + barang2.ukuran > container.kapasitas:
                    raise ValueError("Kontainer melebihi kapasitas")
                cukup1 = True
            if container.has_barang(barang2):
                if container.hitung_barang() - barang2.ukuran + barang1.ukuran > container.kapasitas:
                    raise ValueError("Kontainer melebihi kapasitas")
                cukup2 = True

        if cukup1 and cukup2:
            for container in self.list_container:
                if container.has_barang(barang1):
                    container.remove_barang(barang1)
                    container.add_barang(barang2)
                if container.has_barang(barang2):
                    container.remove_barang(barang2)
                    container.add_barang(barang1)
