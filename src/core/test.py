from src.core.entities import *
from src.core.state import *
from src.core.objective_function import *

barang1 = Barang("XX11", 80)
barang2 = Barang("XX21", 20)
barang3 = Barang("xx31", 20)
barang4 = Barang("XX41", 50)

list_barang :  List[Barang] = []
list_barang.append(barang1)
list_barang.append(barang2)
list_barang.append(barang3)
list_barang.append(barang4)


state = State(list_barang)
state.initiate_random(100)
for barang in state.list_barang:
    print(barang)

for container in state.list_container:
    print(container)

print(state.objective_function)
