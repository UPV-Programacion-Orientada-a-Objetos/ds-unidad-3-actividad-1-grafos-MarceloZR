from libcpp.vector cimport vector

cdef extern from "../cpp/GrafoDisperso.h":
    cdef cppclass GrafoDisperso:
        GrafoDisperso() except +
        void cargarDatos(const char* fname)
        int obtenerGrado(int nodo)
        vector[int] getVecinos(int nodo)
        vector[int] BFS(int inicio, int profundidad)
