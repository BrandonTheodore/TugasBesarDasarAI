from entities import *
import random

class State:
    def __init__(self, list_barang: list[Barang]):
        self.list_barang = list_barang
        self.list_container: List[Container] = []
        self.objective_function = 0

    def __str__(self) -> str:
        if not self.list_container:
            return "State: No containers"
        
        result = []
        for i, container in enumerate(self.list_container, 1):
            container_str = f"Kontainer {i} (Total: {container.hitung_ukuran()}/{container.kapasitas}):"
            for barang in container.daftar_barang:
                container_str += f"\n{barang.ID} ({barang.ukuran})"
            result.append(container_str)
        
        return "\n\n".join(result)


    def initiate_random(self, kapasitas: int):
        self.list_container = []
        
        barang_packing = self.list_barang.copy()
        random.shuffle(barang_packing)
        
        kontainer = Container(kapasitas)

        for barang in barang_packing:
            if not kontainer.add_barang(barang):
                if kontainer.daftar_barang:
                    self.list_container.append(kontainer)
                kontainer = Container(kapasitas)
                kontainer.add_barang(barang)
        
        if kontainer.daftar_barang:
            self.list_container.append(kontainer)

    def move_exist(self, barang: Barang, kontainer1: Container, kontainer2: Container):
        if kontainer1.hitung_ukuran() + barang.ukuran > kontainer1.kapasitas:
            raise ValueError("Barang Melebihi Kapasitas")
        kontainer1.add_barang(barang)
        kontainer2.remove_barang(barang)

    def move_to_empty(self, barang:Barang, kapasitas:int):
        newcontainer = Container(kapasitas)
        newcontainer.add_barang(barang)
        for kontainer in self.list_container:
            kontainer.remove_barang(barang)
        self.list_container.append(newcontainer)
        


    def swap_barang(self, barang1: Barang, barang2: Barang):
        container1 = None
        container2 = None
        
        for container in self.list_container:
            if container.has_barang(barang1):
                container1 = container
            if container.has_barang(barang2):
                container2 = container

        if not container1 or not container2:
            raise ValueError("Barang tidak ditemukan")
            
        if container1 == container2:
            return
            
        new_size1 = container1.hitung_ukuran() - barang1.ukuran + barang2.ukuran
        new_size2 = container2.hitung_ukuran() - barang2.ukuran + barang1.ukuran
        
        if new_size1 > container1.kapasitas or new_size2 > container2.kapasitas:
            raise ValueError("Kapasitas tidak cukup")
        
        container1.remove_barang(barang1)
        container2.remove_barang(barang2)
        container1.add_barang(barang2)
        container2.add_barang(barang1)

    def generate_neighbour(self):
        daftar_kontainer = self.list_container
        for i in range(len(daftar_kontainer)):
            for j in range(i+1, len(daftar_kontainer)):
                neighbour = State(self.list_barang)
                try:
                    neighbour.swap_barang(neighbour.list_barang[i], neighbour.list_barang[j])
                except ValueError:
                    if neighbour.list_barang[i].ukuran > neighbour.list_barang[j]:
                        neighbour.move_to_empty(neighbour.list_barang[i], len(daftar_kontainer))
                    else:
                        neighbour.move_to_empty(neighbour.list_barang[j], len(daftar_kontainer))
                yield neighbour

