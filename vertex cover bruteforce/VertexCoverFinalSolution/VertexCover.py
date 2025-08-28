# GEN AI is used in one of the functions i.e is_vertex_cover(g,subset)
# GFG reference for generate subsets 

# if input files note present
# Run the input file generator before running the code 

import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
import time
import csv
import os


def read_graph(filename):
    G = nx.Graph()
    try:
        with open(filename, 'r') as file:
            n, m = map(int, file.readline().split())
            for _ in range(m):
                u, v = map(int, file.readline().split()) 
                G.add_edge(u, v)
    except IOError:
        print(f"Error opening file: {filename}")
        return None
    return G

def print_graph(G):
    print(G)
    print("\nAdjacency list:-")
    print(G.adjacency())
    for node, neighbors in G.adjacency():
        print(f"{node}: {list(neighbors)}")


def generate_subsets(v): # Geek For Geeks
    subsets = []
    for r in range(len(v) + 1):
        subsets.extend(combinations(v, r)) # array of tuples
    return subsets

def is_vertex_cover(G, subset): # GEN AI PART
    covered_edges = set()
    subset_set = set(subset)
    for u, v in G.edges():
        if u in subset_set or v in subset_set:
            covered_edges.add((min(u, v), max(u, v)))

    all_edges = {(min(u, v), max(u, v)) for u, v in G.edges()}
    return covered_edges == all_edges

def find_smallest_vertex_cover(G):
    start=time.time()
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
        print(smallest_vertex_cover)
        print("Size:", len(smallest_vertex_cover))
    else:
        print("\n No vertex cover found")
    
    end=time.time()
    return smallest_vertex_cover, end-start


def plot_graph(G, highlight_nodes=None, title="Graph", pos=None, number=None):
    if not pos:
        pos = nx.spring_layout(G) 
    
    # fixed layout for consistency , can also pass a seed as attribute for consistency across the devices 
    # pos above return the dictionary position of each vertex 
    # print(pos)
    
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=700)
    if highlight_nodes:
        nx.draw_networkx_nodes(G, pos, nodelist=highlight_nodes, node_color='orange', node_size=900)
    plt.title(title)
    if (highlight_nodes):
        plt.savefig(f"output{number}.png")   

    plt.show()
        
    return pos


def writeoutput(solution, time, m, n):
    fileEmptyCheck = (not os.path.exists("output.csv")) or (os.path.getsize("output.csv") == 0)

    if fileEmptyCheck:
        with open("output.csv", 'w', newline='') as output:
            writer = csv.writer(output)
            writer.writerow(["Input size", "Solution", "Time Taken"])
            writer.writerow([f"{m},{n}", solution, time])
    else:
        with open("output.csv", 'a', newline='') as output:
            writer = csv.writer(output)
            writer.writerow([f"{m},{n}", solution, time])

        
# Main function 
def main():
    if os.path.exists("output.csv"):
        os.remove("output.csv")
    for i in range(1,5):
        filename = f"input{i}.txt"
        G = read_graph(filename)
        if G is None:
            return

        print_graph(G)
        postion = plot_graph(G, title="Original Graph") 
        # saving the position of input graph before showing the output

        Solution, time = find_smallest_vertex_cover(G)
        plot_graph(G, highlight_nodes=Solution, title="Graph Highlighting Smallest Vertex Cover", pos=postion, number=i)
        print(f"total time taken {time}s")
        
        if i ==1:
            writeoutput(Solution, time, 10,10)
        elif i ==2 :
            writeoutput(Solution, time, 10,20)
        elif i ==3 :
            writeoutput(Solution, time, 10,30)
        elif i ==4 :
            writeoutput(Solution, time, 10,40)

if __name__ == "__main__":
    main()
