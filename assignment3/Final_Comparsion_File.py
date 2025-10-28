# IMPORTANT INSTRUCTION
''' if input files not present
 Run the inputfilegenerator.py before running the code 
 for consistent input all the time
 '''

# gen AI is used in few of the functions i.e is_vertex_cover(g,subset) and also in creating timeplots
# GFG reference for generate subsets


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


def generate_subsets(v):  # geek for geeks
    subsets = []
    for r in range(len(v) + 1):
        subsets.extend(combinations(v, r))  # array of tuples
    return subsets


def is_vertex_cover(G, subset):  # GEN AI PART
    covered_edges = set()
    subset_set = set(subset)
    for u, v in G.edges():
        if u in subset_set or v in subset_set:
            covered_edges.add((min(u, v), max(u, v)))

    all_edges = {(min(u, v), max(u, v)) for u, v in G.edges()}
    return covered_edges == all_edges


def find_smallest_vertex_cover(G):
    start = time.time()
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

    end = time.time()
    return smallest_vertex_cover, end-start


def greedy_vertex_cover(G):
    start = time.time()

    # Find a maximal matching
    matching = nx.maximal_matching(G)

    # Build the vertex cover from matched edges
    cover = set()
    for u, v in matching:
        cover.add(u)
        cover.add(v)

    end = time.time()
    return list(cover), end - start


def plot_graph(G, axs, x, y, highlight_nodes=None, title="Graph", pos=None):
    if not pos:
        pos = nx.spring_layout(G, seed=42)  # fixed seed for consistent layout

    ax = axs[x, y]
    ax.clear()  # clear any previous drawing on the subplot

    nx.draw(G, pos, with_labels=True, node_color='lightblue',
            edge_color='gray', node_size=400, ax=ax)

    if highlight_nodes:
        nx.draw_networkx_nodes(
            G, pos, nodelist=highlight_nodes, node_color='orange', node_size=400, ax=ax)

    # ax parameter = tells NetworkX which subplot (Axes) to draw on.
    ax.set_title(title)
    ax.axis('off')  # optionally hide axis ticks

    return pos



def writeoutput_bruteforce(solution, time_taken, m, n):
    fileEmptyCheck = (not os.path.exists("bruteforce_output.csv")) or (
        os.path.getsize("bruteforce_output.csv") == 0)

    if fileEmptyCheck:
        with open("bruteforce_output.csv", 'w', newline='') as output:
            writer = csv.writer(output)
            writer.writerow(["Input size", "Solution", "Time Taken"])
            writer.writerow([f"{m},{n}", solution, time_taken])
    else:
        with open("bruteforce_output.csv", 'a', newline='') as output:
            writer = csv.writer(output)
            writer.writerow([f"{m},{n}", solution, time_taken])


def writeoutput_greedy(solution, time, m, n, sol_len, approxfactor):
    fileEmptyCheck = (not os.path.exists("greedy_output.csv")) or (
        os.path.getsize("greedy_output.csv") == 0)

    if fileEmptyCheck:
        with open("greedy_output.csv", 'w', newline='') as output:
            writer = csv.writer(output)
            writer.writerow(["Input size", "Solution", "Solution Length", "Time Taken", "Approximation Factor"])
            writer.writerow([f"{m},{n}", solution,sol_len, time, approxfactor])
            
    else:
        with open("greedy_output.csv", 'a', newline='') as output:
            writer = csv.writer(output)
            writer.writerow([f"{m},{n}", solution, sol_len, time, approxfactor])



# Main function
def main():
    if os.path.exists("bruteforce_output.csv"):
        os.remove("bruteforce_output.csv")
    if os.path.exists("greedy_output.csv"):
        os.remove("greedy_output.csv")

    fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(12, 10))
    fig2, axs2 = plt.subplots(nrows=2, ncols=2, figsize=(12, 10))
    fig3, axs3 = plt.subplots(nrows=2, ncols=2, figsize=(12, 10))
    
    timebruteforce=[]
    timegreedy=[]

    for i in range(1, 5):
        filename = f"input{i}.txt"
        G = read_graph(filename)
        if G is None:
            return

        x = (i - 1) // 2
        y = (i - 1) % 2

        position = plot_graph(G, axs, x, y, title=f"Original Graph {i}")

        Solution_bruteforce, time_taken_bruteforce = find_smallest_vertex_cover(G) # brute force
        bruteforce_sol_len=len(Solution_bruteforce)
        
        timebruteforce.append(time_taken_bruteforce)
        
        print(f"Bruteforce Vertex Cover: {Solution_bruteforce}")
        print(f"Size: {bruteforce_sol_len}, Time: {time_taken_bruteforce}s")
        print()
        
        Solution_greedy, time_taken_greedy = greedy_vertex_cover(G) # greedy solution
        greedy_sol_len=len(Solution_greedy)
        
        print(f"Greedy Vertex Cover: {Solution_greedy}")
        print(f"Size: {greedy_sol_len}, Time: {time_taken_greedy}s")
        
        approxfactor=greedy_sol_len/bruteforce_sol_len
        
        timegreedy.append(time_taken_greedy)
        
        print(f"approximation factor(comparison with bruteforce results): {approxfactor} ")

        plot_graph(G, axs2, x, y, highlight_nodes=Solution_bruteforce,
                   title=f"Vertex Cover {i}", pos=position)
        

        plot_graph(G, axs3, x, y, highlight_nodes=Solution_greedy,
                   title=f"Vertex Cover {i}", pos=position)
        
        
        
        if i == 1:
            writeoutput_bruteforce(Solution_bruteforce, time_taken_bruteforce, 20, 20)
            
            writeoutput_greedy(Solution_greedy, time_taken_greedy, 20, 20,greedy_sol_len,approxfactor)

        elif i == 2:
            writeoutput_bruteforce(Solution_bruteforce, time_taken_bruteforce, 20, 30)
            
            writeoutput_greedy(Solution_greedy, time_taken_greedy, 20, 30,greedy_sol_len,approxfactor)

        elif i == 3:
            writeoutput_bruteforce(Solution_bruteforce, time_taken_bruteforce, 20, 40)
            
            writeoutput_greedy(Solution_greedy, time_taken_greedy, 20, 40,greedy_sol_len,approxfactor)

        elif i == 4:
            writeoutput_bruteforce(Solution_bruteforce, time_taken_bruteforce, 20, 50)
            
            writeoutput_greedy(Solution_greedy, time_taken_greedy, 20, 50,greedy_sol_len,approxfactor)
            
        

    fig.suptitle("Original Graphs")
    fig2.suptitle("Graphs Highlighting Smallest Vertex Cover BRUTE FORCE solution")
    fig3.suptitle("Graphs Highlighting Vertex Cover GREEDY solution")
    fig.savefig("inputgraph.png")
    fig2.savefig("output_bruteforce.png")
    fig3.savefig("output_greedy.png")
    
        
    x_labels = ["20 20", "20 30", "20 40", "20 50"]
    
    plt.figure(figsize=(8, 4))
    plt.plot(x_labels, timebruteforce, marker='o', linestyle='-', color="blue", label="Brute Force")
    plt.xlabel("Input Graph Size")
    plt.ylabel("Time (seconds)")
    plt.title("Brute Force Execution Time")
    plt.legend()
    plt.tight_layout()
    plt.savefig("time_bruteforce.png")

    plt.figure(figsize=(8, 4))
    plt.plot(x_labels, timegreedy, marker='s', linestyle='--', color="green", label="Greedy")
    plt.xlabel("Input Graph Size")
    plt.ylabel("Time (seconds)")
    plt.title("Greedy Execution Time")
    plt.legend()
    plt.tight_layout()
    plt.savefig("time_greedy.png")

    plt.show()


if __name__ == "__main__":
    main()
