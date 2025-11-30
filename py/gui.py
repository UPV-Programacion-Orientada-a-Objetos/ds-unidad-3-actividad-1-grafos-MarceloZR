import tkinter as tk
from tkinter import filedialog, messagebox
import networkx as nx
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from graph_wrapper import PyGrafoDisperso


class NeuroNetGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("NeuroNet - Demo Said (C++ + Cython + Python)")

        self.grafo = PyGrafoDisperso()
        self.dataset_cargado = False

        # --- panel izquierdo (controles) ---
        left = tk.Frame(root)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        tk.Button(left, text="Cargar dataset SNAP",
                  command=self.cargar_dataset).pack(fill=tk.X)

        self.lbl_estado = tk.Label(left, text="Dataset: ninguno", justify="left")
        self.lbl_estado.pack(fill=tk.X, pady=5)

        tk.Label(left, text="Nodo inicio BFS:").pack(anchor="w")
        self.entry_nodo = tk.Entry(left)
        self.entry_nodo.insert(0, "0")
        self.entry_nodo.pack(fill=tk.X)

        tk.Label(left, text="Profundidad máxima:").pack(anchor="w")
        self.entry_prof = tk.Entry(left)
        self.entry_prof.insert(0, "2")
        self.entry_prof.pack(fill=tk.X)

        tk.Button(left, text="Ejecutar BFS y dibujar",
                  command=self.ejecutar_bfs).pack(fill=tk.X, pady=5)

        tk.Label(left, text="Log:").pack(anchor="w")
        self.txt_log = tk.Text(left, height=15, width=50)
        self.txt_log.pack(fill=tk.BOTH, expand=True)

        # --- panel derecho (gráfico) ---
        right = tk.Frame(root)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        fig = Figure(figsize=(6, 6))
        self.ax = fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(fig, master=right)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.log("[GUI] Aplicación iniciada.")

    def log(self, msg: str):
        print(msg)
        self.txt_log.insert(tk.END, msg + "\n")
        self.txt_log.see(tk.END)

    def cargar_dataset(self):
        path = filedialog.askopenfilename(
            title="Seleccionar archivo Edge List",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*")),
        )
        if not path:
            return

        self.log(f"[GUI] Cargando dataset: {path}")
        try:
            self.grafo.cargar_datos(path)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.log(f"[GUI] ERROR: {e}")
            return

        self.dataset_cargado = True
        self.lbl_estado.config(text=f"Dataset cargado:\n{path}")
        self.log("[GUI] Dataset cargado correctamente (C++).")

    def ejecutar_bfs(self):
        if not self.dataset_cargado:
            messagebox.showwarning("Aviso", "Primero carga un dataset.")
            return

        try:
            nodo = int(self.entry_nodo.get())
            prof = int(self.entry_prof.get())
        except ValueError:
            messagebox.showerror("Error", "Nodo y profundidad deben ser enteros.")
            return

        self.log(f"[GUI] Ejecutando BFS desde nodo {nodo} con profundidad {prof}...")
        try:
            nodos = self.grafo.bfs(nodo, prof)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.log(f"[GUI] ERROR: {e}")
            return

        self.log(f"[GUI] BFS retornó {len(nodos)} nodos.")
        if not nodos:
            self.log("[GUI] No se visitó ningún nodo.")
            return

        # ---- Construir un grafo simple para visualización ----
        G = nx.DiGraph()
        G.add_nodes_from(nodos)

        # Para la demo: conectamos el nodo inicial con los demás como estrella
        for v in nodos:
            if v != nodo:
                G.add_edge(nodo, v)

        self.ax.clear()
        pos = nx.spring_layout(G, k=0.5)
        nx.draw(G, pos, ax=self.ax, with_labels=True, node_size=300, font_size=8)
        self.ax.set_title(f"BFS (demo) desde nodo {nodo}, profundidad {prof}")
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = NeuroNetGUI(root)
    root.mainloop()
