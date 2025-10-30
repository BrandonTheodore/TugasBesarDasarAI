from entities import *
from state import *

def hitung_value_kapasitas(state: State, kapasitas: int) -> int:
    result = 0
    
    for container in state.list_container:
        if container.hitung_ukuran() > kapasitas:
            result += container.hitung_ukuran() - kapasitas

    return result

def hitung_value_kepadatan(state: State) -> int:
    result = 0
    total_sisa = 0

    for container in state.list_container:
        if container.hitung_ukuran() <= container.kapasitas:
            total_sisa += container.kapasitas - container.hitung_ukuran()
    
    result = total_sisa

    return result

def objective_function(state: State, kapasitas: int):
    state.objective_function = hitung_value_kapasitas(state, kapasitas) + hitung_value_kepadatan(state)

def hitung_of(daftar: List[State], kapasitas: int):
    for state in daftar:
        objective_function(state, kapasitas)    