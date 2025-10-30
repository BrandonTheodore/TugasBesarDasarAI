import json
from ..core.entities import *
from typing import List, Tuple

def parse_input(json_input: str) -> Tuple[int, List[Barang]]:
    data = json.loads(json_input)

    kapasitas = data.get("kapasitas_kontaine") or data.get("kapasitas_kontainer")

    list_barang = []
    for item in data["barang"]:
        barang = Barang(item["id"], item["ukuran"])
        list_barang.append(barang)

    return kapasitas, list_barang
