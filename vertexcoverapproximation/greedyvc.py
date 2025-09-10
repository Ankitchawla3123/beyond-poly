import networkx as nx
import matplotlib.pyplot as plt
import time
import csv
import os
import ast



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


def greedy_vertex_cover(G):
    start = time.time()
    cover = set()
    H = G.copy()  

    while H.number_of_edges() > 0:
        u, v = list(H.edges())[0]  
        cover.add(u)
        cover.add(v)

        for edge in list(H.edges()):
            if u in edge or v in edge:
                H.remove_edge(edge[0],edge[1])

    end = time.time()
    return list(cover), end - start

def plot_graph(G, highlight_nodes=None, title="Graph", pos=None, number=None):
    if not pos:
        pos = nx.spring_layout(G)

    plt.figure(figsize=(8, 6))

    nx.draw(G, pos, with_labels=True, node_color='lightblue',
            edge_color='gray', node_size=700)

    if highlight_nodes:
        nx.draw_networkx_nodes(
            G, pos, nodelist=highlight_nodes, node_color='orange', node_size=900)
    plt.title(title)

    if highlight_nodes:
        plt.savefig(f"output{number}.png")
    plt.show()

    return pos


def writeoutput(solution, time, m, n, sol_len, approxfactor):
    fileEmptyCheck = (not os.path.exists("output.csv")) or (
        os.path.getsize("output.csv") == 0)

    if fileEmptyCheck:
        with open("output.csv", 'w', newline='') as output:
            writer = csv.writer(output)
            writer.writerow(["Input size", "Solution", "Solution Length", "Time Taken", "Approximation Factor"])
            writer.writerow([f"{m},{n}", solution,sol_len, time, approxfactor])
            
    else:
        with open("output.csv", 'a', newline='') as output:
            writer = csv.writer(output)
            writer.writerow([f"{m},{n}", solution, sol_len, time, approxfactor])


def calculate_approxfactor(index, greedylen , filename="assignment1_output.csv"):
    
    fileEmptyCheck = (not os.path.exists(filename)) or (os.path.getsize(filename) == 0)

    if fileEmptyCheck :
        print(f"error: {filename} not found. .")
        return
    
    optimalsol_len=0
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        csv_reader=list(csv_reader)
        
        optimalsol_len=len(ast.literal_eval(csv_reader[index][1]))
    
    return optimalsol_len ,greedylen/optimalsol_len
        



def main():
    if os.path.exists("output.csv"):
        os.remove("output.csv")

    for i in range(1, 5):
        filename = f"input{i}.txt"
        G = read_graph(filename)
        if G is None:
            return

        print(f"\nGraph from {filename}")
        pos = plot_graph(G, title="Original Graph")
        solution, time_taken = greedy_vertex_cover(G)
        sol_len=len(solution)
        print(f"Greedy Vertex Cover: {solution}")
        print(f"Size: {sol_len}, Time: {time_taken}s")
        optimalsol_len, approxfactor=calculate_approxfactor(i,sol_len)
        print(f"optimal solution length from assignment one: {optimalsol_len} ")
        print(f"approximation factor(comparison with prac 1 results): {approxfactor} ")
        
        
        plot_graph(G, highlight_nodes=solution, title="Graph with Greedy Vertex Cover", pos=pos, number=i)

        if i == 1:
            writeoutput(solution, time_taken, 10, 10,sol_len,approxfactor)
        elif i == 2:
            writeoutput(solution, time_taken, 10, 20,sol_len,approxfactor)
        elif i == 3:
            writeoutput(solution, time_taken, 10, 30,sol_len,approxfactor)
        elif i == 4:
            writeoutput(solution, time_taken, 10, 40,sol_len,approxfactor)


if __name__ == "__main__":
    main()
