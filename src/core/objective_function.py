from src.core.entities import *
from src.core.state import *

def hitung_value_kapasitas(state: State) -> int:
    result = 0
    
    for container in state.list_container:
        result += container.hitung_ukuran

    return result

def hitung_value_kepadatan(state: State) -> int:
    result = 0
    total_sisa = 0

    for container in state.list_container:
        if container.hitung_ukuran <= container.kapasitas:
            total_sisa += container.kapasitas - container.hitung_ukuran
    
    result = total_sisa/len(state.list_container)

    return result

def objective_function(state: State) -> int:
    return hitung_value_kapasitas(state) + hitung_value_kepadatan(state)