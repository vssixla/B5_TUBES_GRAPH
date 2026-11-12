# Disjoint Set Union, struktur data pendukung kruskal 
class UnionFind:
    def __init__(self, nodes):
        self.parent = {n: n for n in nodes}
        self.size = {n: 1 for n in self.parent}
        self.count = len(self.parent)

    def find(self, node):
        while self.parent[node] != node:
            self.parent[node] = self.parent[self.parent[node]]
            node = self.parent[node]
        return node

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]
        self.count -= 1
        return True


