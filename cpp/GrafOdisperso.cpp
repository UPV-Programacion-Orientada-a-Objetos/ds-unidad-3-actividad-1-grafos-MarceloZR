#include "GrafoDisperso.h"
#include <fstream>
#include <sstream>
#include <queue>
#include <iostream>

GrafoDisperso::GrafoDisperso() {}

void GrafoDisperso::cargarDatos(const char* fname) {
    std::ifstream file(fname);
    if (!file.is_open()) {
        std::cerr << "[C++ Core] Error: No se pudo abrir el archivo." << std::endl;
        return;
    }

    int u, v;
    std::vector<std::vector<int>> adj;

    while (file >> u >> v) {
        int maxnode = std::max(u, v);
        if (maxnode >= adj.size()) adj.resize(maxnode + 1);

        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    numNodes = adj.size();
    row_ptr.resize(numNodes + 1);

    int total = 0;
    for (int i = 0; i < numNodes; i++) {
        row_ptr[i] = total;
        total += adj[i].size();
        col_indices.insert(col_indices.end(), adj[i].begin(), adj[i].end());
    }
    row_ptr[numNodes] = total;
}

int GrafoDisperso::obtenerGrado(int nodo) {
    return row_ptr[nodo + 1] - row_ptr[nodo];
}

std::vector<int> GrafoDisperso::getVecinos(int nodo) {
    std::vector<int> res;
    for (int i = row_ptr[nodo]; i < row_ptr[nodo + 1]; i++)
        res.push_back(col_indices[i]);
    return res;
}

std::vector<int> GrafoDisperso::BFS(int inicio, int profundidadMax) {
    std::vector<int> visitado(numNodes, -1);
    std::queue<int> q;

    visitado[inicio] = 0;
    q.push(inicio);

    std::vector<int> resultado;
    resultado.push_back(inicio);

    while (!q.empty()) {
        int nodo = q.front();
        q.pop();

        if (visitado[nodo] >= profundidadMax) continue;

        for (int i = row_ptr[nodo]; i < row_ptr[nodo + 1]; i++) {
            int vecino = col_indices[i];
            if (visitado[vecino] == -1) {
                visitado[vecino] = visitado[nodo] + 1;
                q.push(vecino);
                resultado.push_back(vecino);
            }
        }
    }
    return resultado;
}
