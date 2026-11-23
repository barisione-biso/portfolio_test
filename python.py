#TIPOS CONCRETOS DE PYTHON: List , Dict, Dequeue y estructuras conceptuales (pila, cola, arbol, grafo) que puedes implementar utilizando esos tipos
print ("Lists : Mutable")
#3 lists
list_a = [1, 5, 9]
list_b = [8, 7, 6, 4]
list_c = [10, 2]
# Appending single item, extending and appending another list
list_a.append(4)
list_a.extend(list_b)
list_a.append(list_c)

print(list_a)
# Insert a number in a specific index
list_a.insert(11, 3)
list_a.insert(0, 0)
print(list_a)

# Remove a specific item on a parameter
list_a.pop(9)
print(list_a)

# Sorting the list
list_a.sort()
print(list_a)

print ("String Lists")
list_a = ["pineapple", "apple", "banana", "cherry"]

list_a.sort()
print(list_a)

list_a.remove("cherry")
print(list_a)

print ("Restricted-types lists (IDE aid only)")
list_1: list[int] = [25, 30, 40]
list_1.append("a string")
print(list_1)

print("=================")
print("tuples :inmutable")
tuple = (1,2,3, "pineapple")
print(tuple[0])
print(tuple[-1])#backwards
print(tuple[:2]) # que es esto?
print(len(tuple))
print(tuple.count("pineapple"))
print(tuple.index("pineapple"))

print("=================")
print("Set")
set_1 = {1,2,3}
set_1.add(4)
set_1.discard(99)
set_1.remove(2)
try:
    set_1.remove(-1)
except KeyError as error:
        print(f"except catch while removing number : {error} which is not in the Set")
print(set_1)
print(3 in set_1)# cuesta O(1) en promedio y O(n) en el peor caso
set_2 = {1, 5, 5, 6}
set_3 = set_1 | set_2
set_3.add(99) # No garantiza inserción ordenada ni mantiene los valores de la estructura ordenados
print(f"union: {set_3}")    
set_3 = set_1 & set_2
print(f"intersection: {set_3}")
try:
    set_2[0]
except TypeError as error:
    print(f"Set is not allowed to query an element by index: {error}")
print("=================")
print("tuples :inmutable")
tuple = (1,2,3)
tuple_2 = ("mango", )
for element in tuple:
    print(element)
e_1, e_2, e_3 = tuple
print(f"tuple: {e_1},{e_2},{e_3}")

print("=================")
print("dict: Keys must be UNIQUE and hashables")
user = {
    "name": "John",
    "age": 30,
}
print(user["name"])
print(user.get("nationality", "N/D"))
user["nationality"] = "Italian"

for key, value in user.items():
    print(f"key: {key}, value: {value}")

del user
print("=================")
print("range: Secuencia inmutable de enteros con un paso constante")
print(list(range(5)))
start = 0
stop = 10
step = 2
evens = range(start, stop, step)
print(6 in evens)
for even_num in evens:
    print(even_num)
print("=================")
print("collections: frozenset, Counter, defaultdict, deque (colas y ventanas deslizantes), heapq (heap)")
from collections import Counter

c = Counter(["python","c++","javascript", "c++", "python", "lisp", "prolog", "prolog", "c++"])
print(c["c++"])
print(c.most_common(1))
print(c.most_common(3))

from collections import defaultdict
#No necesitas crear manualmente la lista antes del primer append.
team = defaultdict(list)
team["backend"] = "Josh"
team["backend"] = "Peter"

print(team["backend"])

from collections import deque #supports queue :) 
print("=================")
print("Stack")
stack = []
stack.append("first")
stack.append("second")
stack.append("third")
print(f"stack : {len(stack)}, last element: {stack[-1]}")
while stack:
    e = stack.pop()
    print(e)

print("=================")
print("Queue")

from collections import deque

queue = deque()
queue.append("A")
queue.append("B")

print(queue.popleft()) #O(1)
print(queue.popleft())
#queue.pop(0) #Avoid it, is a O(n) operation, it has to shift all remaining elements to the left


print("=================")
print("DQueue : double-ended queue")

dqueue = deque(["A","B"])
dqueue.appendleft("C") # C A B
dqueue.append("D") # C A B D

print(dqueue.popleft())
print(dqueue.pop())

# Ojo un DEQUE permite responder a la pregunta, cuales son los ultimos N elementos ?


print("=================")
print("Heap: priority queue")
#En Python, una cola de prioridad se puede implementar con una lista y las funciones de heapq. La lista almacena los elementos; heapq mantiene la propiedad del heap.
# Por esto no es necesario importar Collections pero si funciones adicionales que operan sobre una lista
import heapq
tasks = []

heapq.heappush(tasks, (3, "send report"))	#O(log n)
heapq.heappush(tasks, (1, "resolve incident"))#O(log n)
heapq.heappush(tasks, (2, "review code"))#O(log n)

print(f"min value: {tasks[0]}")	# O(1)
print(heapq.heappop(tasks))#Extact the minimum : O(log n)
cola = [30, 10, 50, 20]
heapq.heapify(cola)  # O(n), modifica la lista
#Porque construye el heap desde abajo. La mayoría de los nodos están cerca de las hojas y requieren poco o ningún desplazamiento. La suma del trabajo es O(n).
#es más eficiente asintóticamente que insertar los n elementos uno por uno, que cuesta O(n log n) en el peor caso.
print(cola)

#¿Por qué heapq no está en collections?

#La biblioteca estándar organiza funcionalidades en módulos distintos:
#|Módulo     |	Qué proporciona                                                         |
#|collections|	Contenedores especializados: deque, Counter, defaultdict.               |
#|heapq	    |Funciones que mantienen un heap sobre una lista.                           |
#|queue	    |Colas sincronizadas para comunicación entre hilos, incluida PriorityQueue. |

#heapq proporciona principalmente algoritmos sobre una lista existente, mientras que collections proporciona tipos de contenedores. Es una decisión de organización de la biblioteca, no una limitación técnica.
