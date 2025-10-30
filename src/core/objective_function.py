from .entities import *
from .state import *

def hitung_value_kapasitas(state: State, kapasitas: int) -> int:
    result = 0
    
    for container in state.list_container:
        if container.hitung_ukuran() > kapasitas:
            result += (container.hitung_ukuran() - kapasitas)*2

    return result

def hitung_value_kepadatan(state: State) -> int:
    result = 0
    total_sisa = 0

    for container in state.list_container:
        if container.hitung_ukuran() <= container.kapasitas:
            kepadatan = container.hitung_ukuran() / container.kapasitas

    kepadatan = kepadatan / len(state.list_container)
    
    result = (1 - kepadatan) * len(state.list_container)

    return result

def objective_function(current_state: State, kapasitas: int):
    current_state.objective_function = hitung_value_kapasitas(current_state, kapasitas) + hitung_value_kepadatan(current_state)

def hitung_of(daftar: List[State], kapasitas: int):
    for state in daftar:
        objective_function(state, kapasitas)    