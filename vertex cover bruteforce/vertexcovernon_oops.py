import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations

def read_graph(filename):
    G = nx.Graph()
    try:
        with open(filename, 'r') as fin:
            n, m = map(int, fin.readline().split())
            for _ in range(m):
                u, v = map(int, fin.readline().split())
                G.add_edge(u, v)
    except IOError:
        print(f"Error opening file: {filename}")
        return None
    return G

def print_graph(G):
    print(G)
    print("\nAdjacency list:")
    print(G.adjacency())
    for node, neighbors in G.adjacency():
        print(f"{node}: {list(neighbors)}")

    # print("Adjacency list for the Graph:")
    # for node in G.nodes():
    #     neighbors = ' '.join(str(neigh) for neigh in G.neighbors(node))
    #     print(f"{node} -> {neighbors}")

def generate_subsets(vertices):
    subsets = []
    for r in range(len(vertices) + 1):
        subsets.extend(combinations(vertices, r))
    return subsets

def is_vertex_cover(G, subset):
    covered_edges = set()
    subset_set = set(subset)
    for u, v in G.edges():
        if u in subset_set or v in subset_set:
            covered_edges.add((min(u, v), max(u, v)))

    all_edges = {(min(u, v), max(u, v)) for u, v in G.edges()}
    return covered_edges == all_edges

def find_smallest_vertex_cover(G):
    vertices = list(G.nodes())
    subsets = generate_subsets(vertices)

    min_size = len(vertices) + 1
    smallest_vertex_cover = []

    for subset in subsets:
        if is_vertex_cover(G, subset):
            if len(subset) < min_size:
                min_size = len(subset)
                smallest_vertex_cover = subset

    if smallest_vertex_cover:
        print("\nSmallest Vertex Cover:")
        print("{", ' '.join(map(str, smallest_vertex_cover)), "}")
        print("Size:", len(smallest_vertex_cover))
    else:
        print("\nNo valid vertex cover found.")
    return smallest_vertex_cover

def plot_graph(G, highlight_nodes=None, title="Graph"):
    pos = nx.spring_layout(G)  # fixed layout for consistency , can also pass a seed as attribute for consistency across the devices 
    # pos above return the dictionary position of each vertex 
    # print(pos)
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=700)
    if highlight_nodes:
        nx.draw_networkx_nodes(G, pos, nodelist=highlight_nodes, node_color='orange', node_size=900)
    plt.title(title)
    plt.show()

def main():
    filename = "input.txt"
    G = read_graph(filename)
    if G is None:
        return

    print_graph(G)
    plot_graph(G, title="Original Graph")

    smallest_vertex_cover = find_smallest_vertex_cover(G)
    plot_graph(G, highlight_nodes=smallest_vertex_cover, title="Graph Highlighting Smallest Vertex Cover")

if __name__ == "__main__":
    main()
