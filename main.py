from collections import Counter
from cycle import eulerian_cycle
from entities import Graph, Vertex, Edge


# Função que, após a colagem de vétices, coloca os graus de entrada e de saída dos vértices
def put_vertices_degree(graph):
    for vertex in graph.vertices:
        for edge in graph.edges:
            if edge.origin == vertex:
                vertex.outDegree += 1
                vertex.incidentEdges[edge] = 0
            elif edge.end == vertex:
                vertex.inDegree += 1


# Função que recebe um grafo e realiza a colagem de seus vértices
def join_vertices(graph):
    vertexNames = [vertex.name for vertex in graph.vertices]
    repeatedVertexNames = {name: count for name, count in Counter(vertexNames).items() if count > 1}  # lista que
    # guarda os nomes dos vértices que são repetidos e, portanto, devem ser colados.

    for name in repeatedVertexNames.keys():
        aux = None  # variável usada no caso em que a aresta é composta por todas as letras iguais (ex: ggg).
        flag = False  # variável usada no caso em que a aresta é composta por todas as letras iguais (ex: ggg).
        newVertex = Vertex(name)
        graph.add_vertex(newVertex)

        for edge in graph.edges:
            if edge.origin.name == edge.end.name == name:
                graph.vertices.remove(edge.origin)
                edge.origin = newVertex
                edgesNewVertex = graph.get_edges_vertex(newVertex)

                for edge_ in edgesNewVertex:
                    if edge_.end is not edge.end:
                        edge_.origin = edge.end

                flag = True
                aux = newVertex
                newVertex = edge.end

            elif edge.origin.name == name:
                graph.vertices.remove(edge.origin)
                edge.origin = newVertex

            elif edge.end.name == name:
                graph.vertices.remove(edge.end)
                edge.end = aux if flag else newVertex

    for edge in graph.edges:
        edge.origin.next.append(edge.end)


# Função que recebe o arquivo com os k-mers e retorna a sequência montada
def assembler(filePath):
    with open(filePath, 'r') as file:
        k_mers = file.read().replace('\n', '').replace(' ', '').split(',')

    k = len(k_mers[1])

    graph = Graph()

    for substring in k_mers:
        prefix = Vertex(substring[: k - 1])
        suffix = Vertex(substring[1:])
        edge = Edge(substring, prefix, suffix)

        graph.add_vertex(prefix)
        graph.add_vertex(suffix)
        graph.add_edge(edge)

    join_vertices(graph)

    put_vertices_degree(graph)

    with open('output.txt', 'w') as file:
        file.write(eulerian_cycle(graph))


# Função que dados um valor k e uma string, retorna os k-mers da sequência em ordem léxicográfica
def composition(string, k):
    substrings = []
    i = 0

    while i < len(string) - k + 1:
        substring = string[i:i + k]
        substrings.append(substring)
        i += 1

    return sorted(substrings)


if __name__ == '__main__':
    compositions = composition('taatgccatgggatgtt', 3)
    compositions = ', '.join(map(str, compositions))

    with open('compositions.txt', 'w') as f:
        f.write(compositions)

    assembler('c120.txt')
