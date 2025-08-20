import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations

class Graph:
    def __init__(self):
        self.G = nx.Graph()
        self.smallest_vertex_cover = []

    def add_edge(self, u, v):
        self.G.add_edge(u, v)

    def print(self):
        print("Adjacency list for the Graph:")
        for node in self.G.nodes():
            print(f"{node} -> {' '.join(str(neigh) for neigh in self.G.neighbors(node))}")

    def generate_subsets(self):
        vertices = list(self.G.nodes())
        subsets = []
        # Generate all subsets using combinations of different sizes
        for r in range(len(vertices) + 1):
            subsets.extend(combinations(vertices, r))
        return subsets

    def is_vertex_cover(self, subset):
        covered_edges = set()
        subset_set = set(subset)
        for u, v in self.G.edges():
            # An edge is covered if either endpoint is in the subset
            if u in subset_set or v in subset_set:
                covered_edges.add((min(u, v), max(u, v)))

        all_edges = {(min(u, v), max(u, v)) for u, v in self.G.edges()}
        return covered_edges == all_edges

    def verify_and_find_smallest_vertex_cover(self):
        subsets = self.generate_subsets()
        min_size = len(self.G.nodes()) + 1
        self.smallest_vertex_cover = []

        for subset in subsets:
            if self.is_vertex_cover(subset):
                if len(subset) < min_size:
                    min_size = len(subset)
                    self.smallest_vertex_cover = subset

        if self.smallest_vertex_cover:
            print("\nSmallest Vertex Cover:")
            print("{", ' '.join(map(str, self.smallest_vertex_cover)), "}")
            print("Size:", len(self.smallest_vertex_cover))
        else:
            print("\nNo valid vertex cover found.")

    def read_from_file(self, filename):
        try:
            with open(filename, 'r') as fin:
                n, m = map(int, fin.readline().split())
                for _ in range(m):
                    u, v = map(int, fin.readline().split())
                    self.add_edge(u, v)
            return True
        except IOError:
            print(f"Error opening file: {filename}")
            return False

    def plot_graph(self, highlight_nodes=None, title="Graph"):
        pos = nx.spring_layout(self.G, seed=42)  # Fixed layout for consistency
        plt.figure(figsize=(8, 6))
        nx.draw(self.G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=700)

        if highlight_nodes:
            nx.draw_networkx_nodes(self.G, pos,
                                   nodelist=highlight_nodes,
                                   node_color='orange',
                                   node_size=900)

        plt.title(title)
        plt.show()


def main():
    g = Graph()
    if not g.read_from_file("input.txt"):
        return

    g.print()
    g.plot_graph(title="Original Graph")
    g.verify_and_find_smallest_vertex_cover()
    g.plot_graph(highlight_nodes=g.smallest_vertex_cover, title="Graph Highlighting Smallest Vertex Cover")


if __name__ == "__main__":
    main()
