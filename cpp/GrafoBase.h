#ifndef GRAFOBASE_H
#define GRAFOBASE_H

#include <vector>
#include <string>

class GrafoBase {
public:
    virtual void cargarDatos(const char* fname) = 0;
    virtual int obtenerGrado(int nodo) = 0;
    virtual std::vector<int> getVecinos(int nodo) = 0;
    virtual std::vector<int> BFS(int inicio, int profundidad) = 0;
    virtual ~GrafoBase() {}
};

#endif
