from __future__ import annotations #Permite escribir anotaciones que mencionan clases que todavía no han terminado de definirse
from dataclasses import dataclass #Importa el decorador @dataclass, que genera métodos habituales de una clase a partir de sus campos.

print("=================")
print("Tree")

@dataclass
class Nodo:
    valor: int
    izquierdo: Nodo | None = None
    derecho: Nodo | None = None

raiz = Nodo(
    8,
    izquierdo=Nodo(3, Nodo(1), Nodo(6)),
    derecho=Nodo(10, derecho=Nodo(14)),
)

def inorden(nodo: Nodo | None):
    if nodo is None:
        return

    yield from inorden(nodo.izquierdo)
    yield nodo.valor
    yield from inorden(nodo.derecho)

print("in orden (Creating a list which takes additional time and space for that operation)")
print(list(inorden(raiz)))

print("in orden (w/o a list, like an iterator in C++... maybe)")
for valor in inorden(raiz):
    print(valor)

'''
Aquí yield produce valores de uno en uno y yield from delega en el recorrido de cada subárbol.
yield permite que una función produzca valores uno por uno, pausando su ejecución entre cada valor. Una función que contiene yield es una función generadora.

A diferencia de return, que termina la función, yield conserva su estado para continuar después.

Debes conocer:
- Raíz, hijo, padre, hoja, profundidad y altura.
    En un árbol, la profundidad mide la distancia desde la raíz hasta un nodo, mientras que la altura mide el camino más largo desde ese nodo hasta una hoja descendiente.
    Normalmente ambas se cuentan en aristas, no en nodos.
- Recorridos preorden, inorden y postorden.
- Recorrido por niveles usando una cola (BFS).
- DFS usa una pila (o recursion)
- Diferencia entre árbol binario y árbol binario de búsqueda (BST).
Un recorrido completo cuesta O(n). En un BST, buscar cuesta O(h), donde h es su altura: O(log n) si está balanceado y O(n) si degenera en una cadena. El recorrido inorden produce valores ordenados cuando el árbol cumple las reglas de un BST.
'''
'''
print("pre-orden")
def preorden(nodo):
    if nodo is None:
        return

    print(nodo.valor)
    preorden(nodo.izquierdo)
    preorden(nodo.derecho)
'''
def preorden(nodo):
    if nodo is None:
        return

    yield nodo.valor
    yield from preorden(nodo.izquierdo)
    yield from preorden(nodo.derecho)

#preorden(raiz)
print(list(preorden(raiz)))
'''
def postorden(nodo):
    if nodo is None:
        return

    postorden(nodo.izquierdo)
    postorden(nodo.derecho)
    print(nodo.valor)
'''
def postorden(nodo):
    if nodo is None:
        return

    yield from postorden(nodo.izquierdo)
    yield from postorden(nodo.derecho)
    yield nodo.valor
    
print("post-orden")
#postorden(raiz)
print(list(postorden(raiz)))
'''

Recorrido	Orden	Resultado del ejemplo
Preorden	Nodo → izquierdo → derecho	8, 3, 1, 6, 10, 14
Inorden	Izquierdo → nodo → derecho	1, 3, 6, 8, 10, 14
Postorden	Izquierdo → derecho → nodo	1, 6, 3, 14, 10, 8


Estos recorridos sirven para cualquier árbol binario. La particularidad de un BST es que el recorrido inorden devuelve sus valores ordenados.

Ambos algoritmos tienen coste temporal O(n) y espacio auxiliar O(h) por la pila de llamadas, donde h es la altura del árbol.

Binary search tree (BST): Todo BST es un árbol binario, pero no todo árbol binario es un BST.
Un árbol binario (binary tree) es un árbol en el que cada nodo tiene como máximo dos hijos: izquierdo y derecho. Sus valores no necesitan seguir ningún orden.

Un árbol binario de búsqueda (binary search tree, BST) añade una regla: para cada nodo, todos los valores de su subárbol izquierdo son menores y todos los del derecho son mayores. Aquí asumiremos que no hay duplicados.
'''
