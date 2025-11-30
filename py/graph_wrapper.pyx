# cython: language_level=3
# distutils: language = c++

from libcpp.vector cimport vector

cdef extern from "../cpp/GrafoDisperso.h":
    cdef cppclass GrafoDisperso:
        GrafoDisperso() except +
        void cargarDatos(const char* fname)
        int obtenerGrado(int nodo)
        vector[int] getVecinos(int nodo)
        vector[int] BFS(int inicio, int profundidad)

cdef class PyGrafoDisperso:
    cdef GrafoDisperso* g

    def __cinit__(self):
        self.g = new GrafoDisperso()

    def __dealloc__(self):
        if self.g != NULL:
            del self.g
            self.g = NULL

    def cargar_datos(self, fname: str):
        cdef bytes b = fname.encode("utf-8")
        self.g.cargarDatos(b)   # b se pasa como const char*

    def obtener_grado(self, nodo: int):
        return self.g.obtenerGrado(nodo)

    def get_vecinos(self, nodo: int):
        cdef vector[int] vec = self.g.getVecinos(nodo)
        return [vec[i] for i in range(vec.size())]

    def bfs(self, inicio: int, profundidad: int):
        cdef vector[int] res = self.g.BFS(inicio, profundidad)
        return [res[i] for i in range(res.size())]
