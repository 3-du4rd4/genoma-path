import random
from entities import Edge


# Função que retorna se um grafo é balanceado ou não
def is_balanced(graph):
    for vertex in graph.vertices:
        if vertex.inDegree != vertex.outDegree:
            return False

    return True


# Função que procura os dois vértices desbalanceado do grafo, retornando se é euleriano,
# caso a quantidade de vértices desbalanceado realmente for 2
def unbalanced_vertices(graph):
    originVertex = None
    destinationVertex = None
    isEulerian = False

    unbalancedVertices = [vertex for vertex in graph.vertices if vertex.inDegree != vertex.outDegree]

    if len(unbalancedVertices) == 2:
        isEulerian = True

        if unbalancedVertices[0].outDegree > unbalancedVertices[0].inDegree:
            destinationVertex = unbalancedVertices[0]
            originVertex = unbalancedVertices[1]
        else:
            originVertex = unbalancedVertices[0]
            destinationVertex = unbalancedVertices[1]

    return isEulerian, originVertex, destinationVertex


# Função que adiciona novas arestas ao grafo para ser possível encontrar o ciclo euleriano e retorna o vértice que antes
# era desbalanceado e tinha o grau de entrada menor que o de saída, o que indica que deve ser o vértice que inicia a
# sequência a ser remontada
def add_new_edge(graph):
    isEulerian, originVertex, destinationVertex = unbalanced_vertices(graph)

    numberOfEdges = abs(destinationVertex.inDegree - destinationVertex.outDegree)

    for i in range(numberOfEdges):
        edge = Edge(originVertex.name + destinationVertex.name[-1], originVertex, destinationVertex)
        originVertex.next.append(destinationVertex)
        originVertex.incidentEdges[edge] = 0
        originVertex.outDegree += 1
        destinationVertex.inDegree += 1
        graph.add_edge(edge)

    return destinationVertex


# Função que retorna se um grafo é euleriano ou não
def is_eulerian(graph):
    if not is_balanced(graph):
        isEulerian, originVertex, destinationVertex = unbalanced_vertices(graph)
        return isEulerian

    return True


# Função que escolhe um vértice que ainda tem arestas não visitadas
def choose_new_vertex(cycle):
    for vertex in cycle:
        if len(vertex.get_unvisited_edges()) > 0:
            return vertex


# Função que une o ciclo principal e o novo ciclo formado
def merge_cycle(eulerianCycle, cycle):
    if len(eulerianCycle) == 0:
        for vertex in cycle:
            eulerianCycle.append(vertex.name)
    else:
        cycleNames = [vertex.name for vertex in cycle]
        startVertex = cycle[0]
        indexStartVertex = eulerianCycle.index(startVertex.name)
        eulerianCycle = eulerianCycle[:indexStartVertex] + cycleNames + eulerianCycle[indexStartVertex + 1:]

    return eulerianCycle


# Função que percorre os vértices do ciclo euleriano formando a sequência
def show_cycle(eulerianCycle):
    cycle = eulerianCycle[0]

    for i in range(1, len(eulerianCycle)-1):
        cycle += eulerianCycle[i][-1]

    return cycle


# Função principal que dado um grafo retorna a sequência formada pelo ciclo euleriano dele
def eulerian_cycle(graph):
    currentVertex = None

    if not is_balanced(graph):
        currentVertex = add_new_edge(graph)

    visitedEdges = []
    unvisitedEdges = graph.edges
    # currentVertex = random.choice(graph.vertices)
    eulerianCycle = []
    cycle = []

    while len(unvisitedEdges) > 0:
        while len(currentVertex.get_unvisited_edges()) > 0:
            cycle.append(currentVertex)
            currentEdge = random.choice(currentVertex.get_unvisited_edges())
            visitedEdges.append(currentEdge)
            unvisitedEdges.remove(currentEdge)
            currentVertex.incidentEdges[currentEdge] = 1
            currentVertex = currentEdge.end

        cycle.append(currentVertex)
        currentVertex = choose_new_vertex(cycle)
        eulerianCycle = merge_cycle(eulerianCycle, cycle)
        cycle = []

    return show_cycle(eulerianCycle)
