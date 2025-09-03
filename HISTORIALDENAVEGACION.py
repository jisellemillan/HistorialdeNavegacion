import tkinter as tk
from tkinter import messagebox, simpledialog
class Nodo:
    def __init__(self, url):
        self.url = url
        self.siguiente = None
        self.anterior = None

class HistorialNavegador:
    def __init__(self):
        self.inicio = None
        self.actual = None

    def agregar_pagina(self, url):
        nuevo = Nodo(url)
        if self.inicio is None:
            self.inicio = nuevo
            self.actual = nuevo
        else:
            self.actual.siguiente = None
            nuevo.anterior = self.actual
            self.actual.siguiente = nuevo
            self.actual = nuevo

    def atras(self):
        if self.actual and self.actual.anterior:
            self.actual = self.actual.anterior
            return self.actual.url
        return None

    def adelante(self):
        if self.actual and self.actual.siguiente:
            self.actual = self.actual.siguiente
            return self.actual.url
        return None

    def mostrar_historial(self):
        paginas = []
        nodo = self.inicio
        while nodo:
            paginas.append(nodo.url)
            nodo = nodo.siguiente
        return paginas

    def buscar(self, texto):
        resultados = []
        nodo = self.inicio
        while nodo:
            if texto.lower() in nodo.url.lower():
                resultados.append(nodo.url)
            nodo = nodo.siguiente
        return resultados

    def eliminar_pagina(self, url):
        nodo = self.inicio
        while nodo:
            if nodo.url == url:
                if nodo.anterior:
                    nodo.anterior.siguiente = nodo.siguiente
                else:
                    self.inicio = nodo.siguiente
                if nodo.siguiente:
                    nodo.siguiente.anterior = nodo.anterior
                if self.actual == nodo:
                    self.actual = nodo.anterior or nodo.siguiente
                return True
            nodo = nodo.siguiente
        return False

    def limpiar_historial(self):
        self.inicio = None
        self.actual = None

class InterfazNavegador:
    def __init__(self, root):
        self.navegador = HistorialNavegador()

        root.title("Caso 3: Historial de Navegador Web")
        root.geometry("600x450")
        root.configure(bg="#1e1e2f")

        frame_top = tk.Frame(root, bg="#1e1e2f")
        frame_top.pack(pady=10)

        self.entry = tk.Entry(frame_top, width=40, font=("Arial", 12))
        self.entry.grid(row=0, column=0, padx=5)

        tk.Button(frame_top, text="Agregar Pagina", bg="#4CAF50", fg="white",
                  font=("Arial", 10, "bold"), command=self.agregar).grid(row=0, column=1, padx=5)

        # botones para navegar
        nav_frame = tk.Frame(root, bg="#1e1e2f")
        nav_frame.pack(pady=5)

        tk.Button(nav_frame, text="⏪ Atras", width=12, bg="#0078D7", fg="white",
                  font=("Arial", 10, "bold"), command=self.atras).grid(row=0, column=0, padx=10)

        tk.Button(nav_frame, text="⏩ Adelante", width=12, bg="#0078D7", fg="white",
                  font=("Arial", 10, "bold"), command=self.adelante).grid(row=0, column=1, padx=10)

        #historial con barra
        list_frame = tk.Frame(root, bg="#1e1e2f")
        list_frame.pack(pady=10)

        self.scrollbar = tk.Scrollbar(list_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(list_frame, width=70, height=12, font=("Consolas", 11),
                                  yscrollcommand=self.scrollbar.set, bg="#2d2d3a", fg="white", selectbackground="#444")
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        self.scrollbar.config(command=self.listbox.yview)

        # Botones 
        op_frame = tk.Frame(root, bg="#1e1e2f")
        op_frame.pack(pady=10)

        tk.Button(op_frame, text="Buscar", width=15, bg="#FF9800", fg="white",
                  font=("Arial", 10, "bold"), command=self.buscar).grid(row=0, column=0, padx=10)

        tk.Button(op_frame, text="Eliminar Página", width=15, bg="#F44336", fg="white",
                  font=("Arial", 10, "bold"), command=self.eliminar).grid(row=0, column=1, padx=10)

        tk.Button(op_frame, text="Limpiar Historial", width=15, bg="#9C27B0", fg="white",
                  font=("Arial", 10, "bold"), command=self.limpiar).grid(row=0, column=2, padx=10)

        # Pagina
        self.label_actual = tk.Label(root, text="Pagina actual: Ninguna",
                                     font=("Arial", 12, "bold"), fg="white", bg="#1e1e2f")
        self.label_actual.pack(pady=10)

    def actualizar_lista(self):
        self.listbox.delete(0, tk.END)
        historial = self.navegador.mostrar_historial()
        for url in historial:
            indicador = " <--- actual" if self.navegador.actual and self.navegador.actual.url == url else ""
            self.listbox.insert(tk.END, f"{url}{indicador}")

        if self.navegador.actual:
            self.label_actual.config(text=f"Página actual: {self.navegador.actual.url}")
        else:
            self.label_actual.config(text="Pagina actual: Ninguna")

    def agregar(self):
        url = self.entry.get().strip()
        if url:
            self.navegador.agregar_pagina(url)
            self.entry.delete(0, tk.END)
            self.actualizar_lista()
        else:
            messagebox.showwarning("Advertencia", "Ingresa una URL valida")

    def atras(self):
        pagina = self.navegador.atras()
        if pagina:
            self.actualizar_lista()
        else:
            messagebox.showinfo("Info", "No hay paginas anteriores")

    def adelante(self):
        pagina = self.navegador.adelante()
        if pagina:
            self.actualizar_lista()
        else:
            messagebox.showinfo("Info", "No hay paginas siguientes")

    def buscar(self):
        texto = simpledialog.askstring("Buscar", "Ingresa texto a buscar en el historial:")
        if texto:
            resultados = self.navegador.buscar(texto)
            if resultados:
                messagebox.showinfo("Resultados", "\n".join(resultados))
            else:
                messagebox.showinfo("Resultados", "No se encontraron coincidencias")

    def eliminar(self):
        seleccion = self.listbox.curselection()
        if seleccion:
            url = self.listbox.get(seleccion[0]).replace(" <--- actual", "")
            self.navegador.eliminar_pagina(url)
            self.actualizar_lista()
        else:
            messagebox.showwarning("Advertencia", "Selecciona una pagina para eliminar")

    def limpiar(self):
        self.navegador.limpiar_historial()
        self.actualizar_lista()
if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazNavegador(root)
    root.mainloop()
