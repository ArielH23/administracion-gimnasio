from tkinter import StringVar
from tkinter import DoubleVar
from tkinter import Label
from tkinter import Entry
from tkinter import ttk
from tkinter import Button
from tkinter import IntVar
from modelo import Abmc


# ##############################################
# MAIN
# ##############################################


class Ventana:
    def __init__(self, window):
        self.objeto_base = Abmc()
        self.root = window
        self.root.title("Administración de gimnasio")
        self.root.geometry("500x403")

        self.titulo = Label(
            self.root, text="Nuevo Socio", bg="#6300FF", fg="white", height=1, width=60
        )
        self.titulo.grid(
            row=0, column=0, columnspan=4, padx=1, pady=1, sticky="w" + "e"
        )

        self.Nombre_y_Apellido = Label(
            self.root, text="Nombre y Apellido:", font=("Times")
        )
        self.nro_documento = Label(self.root, text="Nro. Documento:", font=("Times"))
        self.fecha_nacimento = Label(
            self.root, text="Fecha Nacimiento:", font=("Times")
        )
        self.fecha_dia = Label(self.root, text="                 Día:", font=("Times"))
        self.fecha_mes = Label(self.root, text="         Mes:", font=("Times"))
        self.fecha_anio = Label(self.root, text="Año:", font=("Times"))
        self.peso = Label(self.root, text="Peso:", font=("Times"))

        self.Nombre_y_Apellido.grid(row=1, column=0, sticky="e", padx=6)
        self.nro_documento.grid(row=2, column=0, sticky="e")
        self.fecha_nacimento.grid(row=3, column=1)
        self.fecha_dia.grid(row=4, column=0)
        self.fecha_mes.grid(row=4, column=1, sticky="w")
        self.fecha_anio.grid(row=4, column=1, sticky="e")
        self.peso.grid(row=5, column=0, sticky="e")

        (
            self.nya_val,
            self.dni_val,
            self.fnd_val,
            self.fnm_val,
            self.fna_val,
            self.p_val,
        ) = (
            StringVar(),
            IntVar(),
            IntVar(),
            IntVar(),
            IntVar(),
            DoubleVar(),
        )
        # ENTRADAS
        self.entrada_n_y_a = Entry(self.root, textvariable=self.nya_val, width=25)
        self.entrada_dni = Entry(self.root, textvariable=self.dni_val, width=8)
        self.entrada_f_n_d = Entry(self.root, textvariable=self.fnd_val, width=5)
        self.entrada_f_n_m = Entry(self.root, textvariable=self.fnm_val, width=5)
        self.entrada_f_n_a = Entry(
            self.root,
            textvariable=self.fna_val,
            width=10,
        )
        self.entrada_p = Entry(self.root, textvariable=self.p_val, width=10)

        self.entrada_n_y_a.grid(row=1, column=1, sticky="w")
        self.entrada_dni.grid(row=2, column=1, sticky="w")
        self.entrada_f_n_d.grid(row=4, column=0, sticky="e")
        self.entrada_f_n_m.grid(row=4, column=1)
        self.entrada_f_n_a.grid(row=4, column=2, sticky="w")
        self.entrada_p.grid(row=5, column=1, sticky="w")

        # TREEVIEW
        self.tree = ttk.Treeview(self.root)
        self.tree["columns"] = ("col1", "col2", "col3", "col4", "col5", "col6")
        self.tree.column("#0", width=30, minwidth=50, anchor="w")
        self.tree.column("col1", width=100, minwidth=80)
        self.tree.column("col2", width=100, minwidth=80)
        self.tree.column("col3", width=50, minwidth=50)
        self.tree.column("col4", width=100, minwidth=80)
        self.tree.column("col5", width=120, minwidth=80)
        self.tree.column("col6", width=0, minwidth=0)
        self.tree.heading("#0", text="ID")
        self.tree.heading("col1", text="Nombre")
        self.tree.heading("col2", text="Apellido")
        self.tree.heading("col3", text="Edad")
        self.tree.heading("col4", text="Peso")
        self.tree.heading("col5", text="Nro. Documento")
        self.tree.grid(row=10, column=0, columnspan=4, sticky="nsew")
        self.objeto_base.actualizar_treeview(self.tree)
        self.tree.bind(
            "<Button-1>", self.SimpleClick
        )  # haciendo un click, aparecen los datos del socio para modificar

        # BOTONES
        boton_vaciar = Button(
            self.root,
            text="Limpiar",
            command=lambda: self.vaciar_entradas(self.tree),
        )
        boton_alta = Button(
            self.root,
            text="Agregar",
            command=lambda: self.objeto_base.alta(
                self.nya_val,
                self.dni_val,
                self.fnd_val,
                self.fnm_val,
                self.fna_val,
                self.p_val,
                self.tree,
            ),
        )
        boton_baja = Button(
            self.root, text="Eliminar", command=lambda: self.objeto_base.baja(self.tree)
        )
        boton_modificacion = Button(
            self.root,
            text="Modificar",
            command=lambda: self.objeto_base.modificacion(
                self.nya_val,
                self.dni_val,
                self.fnd_val,
                self.fnm_val,
                self.fna_val,
                self.p_val,
                self.tree,
            ),
        )
        boton_consulta = Button(
            self.root,
            text="Consulta",
            command=lambda: self.objeto_base.consulta(self.tree),
        )

        boton_vaciar.grid(row=2, column=3)
        boton_alta.grid(row=6, column=1)
        boton_baja.grid(row=6, column=2)
        boton_modificacion.grid(row=6, column=0, sticky="e")
        boton_consulta.grid(row=6, column=0, sticky="w")

    def SimpleClick(self, event):
        self.entrada_n_y_a.delete(0, "end")
        self.entrada_dni.delete(0, "end")
        self.entrada_f_n_d.delete(0, "end")
        self.entrada_f_n_m.delete(0, "end")
        self.entrada_f_n_a.delete(0, "end")
        self.entrada_p.delete(0, "end")
        if self.tree.selection():
            valor = self.tree.selection()
            item = self.tree.item(valor)
            self.entrada_n_y_a.insert(
                0, str(item["values"][0]) + " " + str(item["values"][1])
            )
            self.entrada_dni.insert(0, item["values"][4])
            self.entrada_f_n_d.insert(0, int(item["values"][5][0:2]))
            self.entrada_f_n_m.insert(0, int(item["values"][5][2:4]))
            self.entrada_f_n_a.insert(0, int(item["values"][5][4:8]))
            self.entrada_p.insert(0, item["values"][3])
            self.nya_val.set(str(item["values"][0]) + " " + str(item["values"][1]))
            self.dni_val.set(item["values"][4])
            self.fnd_val.set(int(item["values"][5][0:2]))
            self.fnm_val.set(int(item["values"][5][2:4]))
            self.fna_val.set(int(item["values"][5][4:8]))
            self.p_val.set(item["values"][3])

    def vaciar_entradas(self, tree):
        self.nya_val.set("")
        self.dni_val.set(0)
        self.fnd_val.set(0)
        self.fnm_val.set(0)
        self.fna_val.set(0)
        self.p_val.set(0.0)
