#include <iostream>
#include <fstream>
#include <list>
#include <map>
#include <vector>
#include <set>
using namespace std;

class Graph {
    map<int, list<int>> adjList;
    vector<vector<int>> subsets;

public:
    vector<int> smallestVertexCover;

    void add_edge(int u, int v)
    {
        adjList[u].push_back(v);
        adjList[v].push_back(u);
    }

    void print()
    {
        cout << "Adjacency list for the Graph:\n";
        for (auto i : adjList) {
            cout << i.first << " -> ";
            for (auto j : i.second) {
                cout << j << " ";
            }
            cout << endl;
        }
    }

    void generateSubsets()
    {
        subsets.clear();
        vector<int> vertices;
        for (auto it : adjList) {
            vertices.push_back(it.first);
        }

        vector<int> currentSubset;
        generateSubsetsRecursive(vertices, 0, currentSubset);
    }

    void generateSubsetsRecursive(const vector<int>& vertices, int index, vector<int>& currentSubset)
    {
        if (index == vertices.size()) {
            subsets.push_back(currentSubset);
            return;
        }
        currentSubset.push_back(vertices[index]);
        generateSubsetsRecursive(vertices, index + 1, currentSubset);
        currentSubset.pop_back();
        generateSubsetsRecursive(vertices, index + 1, currentSubset);
    }

    bool isVertexCover(const vector<int>& subset)
    {
        set<pair<int, int>> coveredEdges;

        for (int u : subset) {
            for (int v : adjList[u]) {
                coveredEdges.insert({min(u, v), max(u, v)});
            }
        }

        set<pair<int, int>> allEdges;
        for (const auto& pair : adjList) {
            int u = pair.first;
            for (int v : pair.second) {
                allEdges.insert({min(u, v), max(u, v)});
            }
        }

        return coveredEdges == allEdges;
    }

    void verifyAndFindSmallestVertexCover()
    {
        generateSubsets();

        int minSize = adjList.size() + 1;
        smallestVertexCover.clear();

        for (const auto& subset : subsets) {
            if (isVertexCover(subset)) {
                if (subset.size() < minSize) {
                    minSize = subset.size();
                    smallestVertexCover = subset;
                }
            }
        }

        if (!smallestVertexCover.empty()) {
            cout << "\nSmallest Vertex Cover:\n{ ";
            for (int v : smallestVertexCover) {
                cout << v << " ";
            }
            cout << "}\nSize: " << smallestVertexCover.size() << endl;
        } else {
            cout << "\nNo valid vertex cover found.\n";
        }
    }

    // Read graph from input file
    bool readFromFile(const string& filename)
    {
        ifstream fin(filename);
        if (!fin) {
            cerr << "Error opening file: " << filename << endl;
            return false;
        }

        int n, m;
        fin >> n >> m;

        for (int i = 0; i < m; i++) {
            int u, v;
            fin >> u >> v;
            add_edge(u, v);
        }

        fin.close();
        return true;
    }
};

int main()
{
    Graph g;
    if (!g.readFromFile("input.txt")) {
        return 1; 
    }

    g.print();
    g.verifyAndFindSmallestVertexCover();

    return 0;
}
