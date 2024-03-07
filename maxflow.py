
from collections import defaultdict, deque


def read_graph(filename):
    graph = defaultdict(dict)
    all_nodes = set()
    with open(filename, 'r') as file:
        for line in file:
            start, end, capacity = line.strip().split()
            graph[start][end] = int(capacity)
            all_nodes.update([start, end])
    return graph, all_nodes


def ford_fulkerson(graph, nodes, source, sink):
    def bfs(graph, source, sink, parent):
        visited = {node: False for node in nodes}
        queue = deque([source])
        visited[source] = True

        while queue:
            u = queue.popleft()
            for v, capacity in graph[u].items():
                if not visited[v] and capacity - flow_passed[u][v] > 0:
                    parent[v] = u
                    visited[v] = True
                    queue.append(v)
                    if v == sink:
                        return True
        return False

    flow_passed = {node: defaultdict(int) for node in nodes}
    parent = {node: None for node in nodes}
    max_flow = 0
    paths = []

    while bfs(graph, source, sink, parent):
        path_flow = float('Inf')
        s = sink
        path = []

        while s != source:
            path.append(s)
            path_flow = min(path_flow, graph[parent[s]][s] - flow_passed[parent[s]][s])
            s = parent[s]
        path.append(source)
        path.reverse()

        max_flow += path_flow
        paths.append((path, path_flow))

        v = sink
        while v != source:
            u = parent[v]
            flow_passed[u][v] += path_flow
            flow_passed[v][u] -= path_flow
            v = parent[v]

    return max_flow, paths


if __name__ == "__main__":
    input_filename = 'input1.txt'
    output_filename = 'output1.txt'

    graph, nodes = read_graph(input_filename)
    source = 'S'
    sink = 'T'

    max_flow, paths = ford_fulkerson(graph, nodes, source, sink)

    with open(output_filename, 'w') as file:
        file.write(f"The maximum possible flow is: {max_flow}\n")
        file.write("Paths used:\n")
        for path, flow in paths:
            file.write(f"Path: {' -> '.join(path)}, Flow: {flow}\n")
