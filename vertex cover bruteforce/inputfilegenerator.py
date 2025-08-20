import random

def generate_graph_input(filename, n, m):
    """
    Generates a random undirected graph input file.

    Args:
        filename (str): Output filename.
        n (int): Number of vertices.
        m (int): Number of edges.

    The vertices are numbered from 0 to n-1.
    """
    if m > n * (n - 1) // 2:
        raise ValueError("Too many edges for given number of vertices.")

    edges = set()
    while len(edges) < m:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v:
            edge = tuple(sorted((u, v)))  # avoid duplicates and self loops
            edges.add(edge)

    with open(filename, 'w') as f:
        f.write(f"{n} {m}\n")
        for u, v in edges:
            f.write(f"{u} {v}\n")

if __name__ == "__main__":
    # Customize these parameters:
    n = 8  # number of vertices
    m = 11  # number of edges
    output_file = "input.txt"

    generate_graph_input(output_file, n, m)
    print(f"Generated graph input file '{output_file}' with {n} vertices and {m} edges.")
