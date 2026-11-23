print("=================")
print("Graph")
print("Source: https://uchile.progcomp.cl/apunte/grafos/busqueda_en_grafos/")
#Pendiente : bipartite check
# Caminos y ciclos eulerianos
# Minimum spanning tree
# Shortest paths

'''
Los algoritmos básicos que debes conocer son:
|Algoritmo	                    |Estructura auxiliar	| Utilidad                                                                          |
|BFS: búsqueda en anchura	    |Cola (FIFO)            |Explorar por niveles; encontrar caminos con menos aristas en grafos sin pesos.     |
|DFS: búsqueda en profundidad	|Pila o recursión	    |Explorar ramas, detectar ciclos y analizar conectividad.                           |
|                               |                       | Dijkstra's shortest path, Kahn's Algorithm, and Prim's algorithm are based on BFS.|
|Dijkstra	                    |Cola de prioridad      |Encontrar caminos de menor coste con pesos no negativos.                           |
|Ordenamiento topológico	    | Cola o DFS	        | Ordenar dependencias en un grafo dirigido sin ciclos.                             |


Con listas de adyacencia, BFS y DFS tienen complejidad O(V + E), donde V es el número de vértices y E el de aristas.
grafo = { #no dirigido
    "A": ["B", "C"],
    "B": ["A", "D"],
    "C": ["A", "D"],
    "D": ["B", "C"],
}
'''

grafo = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B"],
    "E": ["B"],
    "F": ["C"],
}

from collections import deque

def bfs(grafo: dict[str, list[str]], inicio: str) -> list[str]:
    pendientes = deque([inicio])# en una cola vamos agregando los nodos vecinos por visitar 
    visitados = {inicio} #Conjunto de visitados
    recorrido = [] #lista

    while pendientes:
        actual = pendientes.popleft()
        recorrido.append(actual)

        for vecino in grafo.get(actual, []):
            if vecino not in visitados:
                visitados.add(vecino)
                pendientes.append(vecino)

    return recorrido

print(bfs(grafo, "A"))  # ['A', 'B', 'C', 'D']


def dfs(grafo, inicio): #Se puede implementar con una pila o con recursión. Esta última implementación es trivial
    pila = [inicio]
    visitados = set()

    while pila:
        actual = pila.pop()

        if actual in visitados:
            continue

        visitados.add(actual)
        yield actual

        # Invertimos los vecinos para visitar primero
        # el que aparece primero en la lista.
        for vecino in reversed(grafo.get(actual, [])):
            if vecino not in visitados:
                pila.append(vecino)


print(list(dfs(grafo, "A")))
# ['A', 'B', 'D', 'E', 'C', 'F']



visitados = set()
recorrido = list()    
def dfs_recursive(grafo, nodo):
    visitados.add(nodo)
    recorrido.append(nodo)
    if nodo is None:
        return
    
    vecinos = grafo.get(nodo, [])
    for vecino in vecinos:
        if vecino not in visitados:
            dfs_recursive(grafo, vecino)
    return recorrido

print(dfs_recursive(grafo, "A")) # ['A', 'B', 'D', 'E', 'C', 'F']