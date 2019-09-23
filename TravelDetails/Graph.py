import sys


class Graph:

    def __init__(self, vertices, graph):
        self.V = vertices
        self.graph = graph

    def minDistance(self, dist, path):
        min = min_index = sys.maxsize
        for v in range(self.V):
            if dist[v] < min and not path[v]:
                min = dist[v]
                min_index = v
        return min_index

    def dijkstra(self, src):
        dist = [sys.maxsize] * self.V
        dist[src] = 0
        path = [False] * self.V
        parent = [-1] * self.V
        for i in range(self.V):
            u = self.minDistance(dist, path)
            path[u] = True
            for v in range(self.V):
                if self.graph[u][v] > 0 and not path[v] and dist[v] > dist[u] + self.graph[u][v]:
                    dist[v] = dist[u] + self.graph[u][v]
                    parent[v] = u
        return parent
