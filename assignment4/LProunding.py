# IMPORTANT INSTRUCTION
'''  
INPUT files are same as input for bruteforce vertex cover 
to maintain consistency 
run this file to see the results 
 '''
 
# gen AI is used in one of the functions i.e ast library (Abstract Syntax Trees) 
# used for parsing string to tuple/list


import networkx as nx
import matplotlib.pyplot as plt
import time
import csv
import os
import ast

import pulp
from pulp import LpProblem, LpMinimize, LpVariable, lpSum



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
    
    # Define LP problem
    prob = LpProblem("LP_Relaxed_Vertex_Cover", LpMinimize)
    
    # Relax binary constraints → continuous between 0 and 1
    x = {v: LpVariable(f"x_{v}", lowBound=0, upBound=1, cat='Continuous') for v in G.nodes()}
    
    # Objective: minimize sum of x[v]
    prob += lpSum(x[v] for v in G.nodes())
    
    # Constraints: for each edge, at least one endpoint should be covered
    for u, v in G.edges():
        prob += x[u] + x[v] >= 1
    
    # Solve LP
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    
    # Fractional solution
    fractional_sol = {v: pulp.value(x[v]) for v in G.nodes()}
    
    # Rounding heuristic: if x[v] >= 0.5 → select that vertex
    cover = [v for v in G.nodes() if fractional_sol[v] >= 0.5]
    
    end = time.time()
    
    print("Fractional solution:")
    print(fractional_sol)
    print("\nRounded cover:")
    print(cover)
    
    return cover, end - start

# Example usage:
# G = nx.cycle_graph(5)
# cover, duration = greedy_vertex_cover(G)
# print("Vertex cover:", cover)
# print("Time taken:", duration)


def plot_graph(G, highlight_nodes=None, title="Graph", pos=None, number=None):
    if not pos:
        pos = nx.spring_layout(G)

    
    # fixed layout for consistency , can also pass a seed as attribute for consistency across the devices 
    # pos above return the dictionary position of each vertex 
    # print(pos)
    
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


def calculate_approxfactor(index, lplen , filename="previous_outputs.csv"):
    
    fileEmptyCheck = (not os.path.exists(filename)) or (os.path.getsize(filename) == 0)

    if fileEmptyCheck :
        print(f"error: {filename} not found. .")
        return
    
    greedy_sol_len=0
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        csv_reader=list(csv_reader)
        
        greedy_sol_len=len(ast.literal_eval(csv_reader[index][1])) # GEN AI USED HERE
    
    return greedy_sol_len ,lplen/greedy_sol_len
        



def main():
    if os.path.exists("output.csv"):
        os.remove("output.csv")

    for i in range(1, 9):
        filename = f"input{i}.txt"
        G = read_graph(filename)
        if G is None:
            return


        print(f"\nGraph from {filename}")
        pos = plot_graph(G, title="Original Graph") # saving the position of input graph before showing the output
        
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
        elif i == 5:
            writeoutput(solution, time_taken, 20, 20,sol_len,approxfactor)

        elif i == 6:
            writeoutput(solution, time_taken, 20, 30,sol_len,approxfactor)

        elif i == 7:
  
            writeoutput(solution, time_taken, 20, 40,sol_len,approxfactor)

        elif i == 8:
            writeoutput(solution, time_taken, 20, 50,sol_len,approxfactor)            


if __name__ == "__main__":
    main()
