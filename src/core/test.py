from entities import *
from state import *
from objective_function import *

barang1 = Barang("XX11", 80)
barang2 = Barang("XX21", 20)
barang3 = Barang("xx31", 50)

list_barang :  List[Barang] = []
list_barang.append(barang1)
list_barang.append(barang2)
list_barang.append(barang3)


state = State(list_barang)
state.initiate_random(100)
for barang in state.list_barang:
    print(barang)

for container in state.list_container:
    print(container)

state.swap_barang(barang1, barang3)
for container in state.list_container:
    print(container)

objective_function(state, 100)
print(state.objective_function)
