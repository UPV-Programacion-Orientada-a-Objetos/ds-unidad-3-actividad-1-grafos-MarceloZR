#ifndef GRAFODISPERSO_H
#define GRAFODISPERSO_H

#include "GrafoBase.h"
#include <vector>
#include <string>

class GrafoDisperso : public GrafoBase {
private:
    std::vector<int> row_ptr;
    std::vector<int> col_indices;
    int numNodes = 0;

public:
    GrafoDisperso();
    void cargarDatos(const char* fname) override;
    int obtenerGrado(int nodo) override;
    std::vector<int> getVecinos(int nodo) override;
    std::vector<int> BFS(int inicio, int profundidad) override;
};

#endif
