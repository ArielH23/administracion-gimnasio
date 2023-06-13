from peewee import *
from tkinter.messagebox import showinfo
from tkinter.messagebox import showerror
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta

# ##############################################
# MODELO
# ##############################################

db = SqliteDatabase("listado_socios.db")


class BaseModel(Model):
    class Meta:
        database = db


class socios(BaseModel):  # Esta es la tabla
    nombre = CharField()
    apellido = CharField()
    edad = IntegerField()
    peso = DoubleField()
    dni = IntegerField()
    fecha_nac = CharField()


db.connect()  # se conecta a la base
db.create_tables([socios])  # se crea la tabla


class Abmc:
    def __init__(self):
        pass

    # COMPROBACIONES
    def comprobacion_alta(
        self,
        nombre_y_apellido,
        nro_documento,
        fecha_nac_d,
        fecha_nac_m,
        fecha_nac_a,
        peso,
    ):
        error = ""
        anio_actual = datetime.today().year
        patron_nro = "^[0-9]*$"
        patron = "^[A-Za-záéíóú\s]*$"

        if (
            nombre_y_apellido == ""
            or nro_documento == ""
            or fecha_nac_d == ""
            or fecha_nac_m == ""
            or fecha_nac_a == ""
            or peso == ""
        ):
            if nombre_y_apellido == "":
                error += "Falta ingresar Nombre y Apellido\n"
            if nro_documento == "":
                error += "Falta ingresar Nro. Documento\n"
            if fecha_nac_d == "":
                error += "Falta ingresar Día de Nacimiento\n"
            if fecha_nac_m == "":
                error += "Falta ingresar Mes de Nacimiento\n"
            if fecha_nac_a == "":
                error += "Falta ingresar Año de Nacimiento\n"
            if peso == "":
                error += "Falta ingresar Peso\n"
            return error

        try:  # Comprobación Nombre y Apellido
            con_espacio = True
            for l in nombre_y_apellido:
                if l.isspace():
                    con_espacio = False
            if con_espacio:
                error += "Nombre y Apellido: 'Nombre' 'Apellido'\n"
            nombre = nombre_y_apellido[0 : nombre_y_apellido.rfind(" ")]
            apellido = nombre_y_apellido[
                nombre_y_apellido.rfind(" ") + 1 : len(nombre_y_apellido)
            ]
            nombre = nombre.capitalize()
            apellido = apellido.capitalize()
            for fila in socios.select():  # que no se repita el nombre y apellido
                if nombre + apellido == fila.nombre + fila.apellido:
                    error += "Nombre y Apellido: repetido\n"
                    break
        except not re.match(patron, nombre_y_apellido):
            error += "Nombre y Apellido: solo letras\n"

        try:  # Comprobación Nro. Documento
            if nro_documento > 99999999:
                error += "Nro. Documento: exede el limite\n"
            if nro_documento < 10000000:
                error += "Nro. Documento: faltan numeros\n"
            for fila in socios.select():  # que no se repita el nro. documento
                if nro_documento == fila.dni:
                    error += "Nro. Documento repetido\n"
                    break
        except not re.match(patron_nro, str(nro_documento)):
            error += "Nro. Documento: solo numeros\n"

        try:  # Comprobación Fecha Nacimiento Día
            if fecha_nac_d > 31:
                error += "Fecha Nacimiento, Día: >31\n"
            if fecha_nac_d < 1:
                error += "Fecha Nacimiento, Día: <1\n"
        except re.match(patron_nro, str(fecha_nac_d)):
            error += "Fecha Nacimiento, Día: solo numeros\n"

        try:  # Comprobación Fecha Nacimiento Mes
            if fecha_nac_m > 12:
                error += "Fecha Nacimiento, Mes: >12\n"
            if fecha_nac_m < 1:
                error += "Fecha Nacimiento, Mes: <1\n"
        except not re.match(patron_nro, str(fecha_nac_m)):
            error += "Fecha Nacimiento, Mes: solo numeros\n"

        try:  # Comprobación Fecha Nacimiento Año
            if fecha_nac_a > anio_actual:  # comprueba q no exeda el año actual
                error += f"Fecha Nacimiento, Año: >{anio_actual}\n"
            if fecha_nac_a < 1930:
                error += "Fecha Nacimiento, Año: <1930\n"
        except not re.match(patron_nro, str(fecha_nac_a)):
            error += "Fecha Nacimiento, Año: solo numeros\n"

        if peso < 0:  # Comprobación Peso
            error += "Peso: <0\n"
        return error

    def comprobacion_modificar(
        self,
        nombre_y_apellido,
        nro_documento,
        fecha_nac_d,
        fecha_nac_m,
        fecha_nac_a,
        peso,
        valor,
        tree,
    ):
        item = tree.item(valor)
        error = ""
        anio_actual = datetime.today().year
        patron_nro = "^[0-9]*$"
        patron = "^[A-Za-záéíóú\s]*$"

        try:  # Comprobación Nombre y Apellido
            con_espacio = True
            for l in nombre_y_apellido:
                if l.isspace():
                    con_espacio = False
            if con_espacio:
                error += "Nombre y Apellido: 'Nombre' 'Apellido'\n"
            nombre = nombre_y_apellido[0 : nombre_y_apellido.rfind(" ")]
            apellido = nombre_y_apellido[
                nombre_y_apellido.rfind(" ") + 1 : len(nombre_y_apellido)
            ]
            nombre = nombre.capitalize()
            apellido = apellido.capitalize()
            for fila in socios.select():
                if (
                    nombre + apellido == fila.nombre + fila.apellido
                    and fila.id != item["text"]
                ):
                    error += "Nombre y Apellido: repetido\n"
                    break
        except not re.match(patron, nombre_y_apellido):
            error += "Nombre y Apellido: solo letras\n"

        try:  # Comprobación Nro. Documento
            if nro_documento > 99999999:
                error += "Nro. Documento: exede el limite\n"
            if nro_documento < 10000000:
                error += "Nro. Documento: faltan numeros\n"
            for fila in socios.select():
                if nro_documento == fila.dni and fila.id != item["text"]:
                    error += "Nro. Documento repetido\n"
                    break
        except not re.match(patron_nro, str(nro_documento)):
            error += "Nro. Documento: solo numeros\n"

        try:  # Comprobación Fecha Nacimiento Día
            if fecha_nac_d > 31:
                error += "Fecha Nacimiento, Día: >31\n"
            if fecha_nac_d < 1:
                error += "Fecha Nacimiento, Día: <1\n"
        except not re.match(patron_nro, str(fecha_nac_d)):
            error += "Fecha Nacimiento, Día: solo numeros\n"

        try:  # Comprobación Fecha Nacimiento Mes
            if fecha_nac_m > 12:
                error += "Fecha Nacimiento, Mes: >12\n"
            if fecha_nac_m < 1:
                error += "Fecha Nacimiento, Mes: <1\n"
        except not re.match(patron_nro, str(fecha_nac_m)):
            error += "Fecha Nacimiento, Mes: solo numeros\n"

        try:  # Comprobación Fecha Nacimiento Año
            if fecha_nac_a > anio_actual:  # comprueba q no exeda el año actual
                error += f"Fecha Nacimiento, Año: >{anio_actual}\n"
            if fecha_nac_a < 1930:
                error += "Fecha Nacimiento, Año: <1930\n"
        except not re.match(patron_nro, str(fecha_nac_a)):
            error += "Fecha Nacimiento, Año: solo numeros\n"

        if peso < 0:  # Comprobación Peso
            error += "Peso: <0\n"
        return error

    # ABMC
    # A
    def alta(
        self,
        nombre_y_apellido_v,
        nro_documento_v,
        fecha_nac_d_v,
        fecha_nac_m_v,
        fecha_nac_a_v,
        peso_v,
        tree,
    ):
        nombre_y_apellido = nombre_y_apellido_v.get()
        nro_documento = nro_documento_v.get()
        fecha_nac_d = fecha_nac_d_v.get()
        fecha_nac_m = fecha_nac_m_v.get()
        fecha_nac_a = fecha_nac_a_v.get()
        peso = peso_v.get()

        error = ""
        error += self.comprobacion_alta(
            nombre_y_apellido,
            nro_documento,
            fecha_nac_d,
            fecha_nac_m,
            fecha_nac_a,
            peso,
        )
        if not error:
            edad = relativedelta(
                datetime.now(), datetime(fecha_nac_a, fecha_nac_m, fecha_nac_d)
            )
            nombre = nombre_y_apellido[0 : nombre_y_apellido.rfind(" ")]
            apellido = nombre_y_apellido[
                nombre_y_apellido.rfind(" ") + 1 : len(nombre_y_apellido)
            ]
            nombre = nombre.capitalize()
            apellido = apellido.capitalize()
            if fecha_nac_d < 10:
                fecha_nac = "0" + str(fecha_nac_d)
            else:
                fecha_nac = str(fecha_nac_d)
            if fecha_nac_m < 10:
                fecha_nac += "0" + str(fecha_nac_m)
            else:
                fecha_nac += str(fecha_nac_m)
            fecha_nac += str(fecha_nac_a)
            fecha_nac += "f"
            socio = socios()
            socio.nombre = nombre
            socio.apellido = apellido
            socio.edad = edad.years
            socio.peso = peso
            socio.dni = nro_documento
            socio.fecha_nac = fecha_nac
            socio.save()
            self.actualizar_treeview(tree)
            showinfo("Alta", "Nuevo socio agregado")
        else:
            showerror("Error al agregar", error)

    # B
    def baja(self, tree):
        item_seleccionado = tree.focus()
        item = tree.item(item_seleccionado)
        borrar = socios.get(socios.id == item["text"])
        borrar.delete_instance()  # borra el registro
        self.actualizar_treeview(tree)

    # M
    def modificacion(
        self,
        nombre_y_apellido_v,
        nro_documento_v,
        fecha_nac_d_v,
        fecha_nac_m_v,
        fecha_nac_a_v,
        peso_v,
        tree,
    ):
        nombre_y_apellido = nombre_y_apellido_v.get()
        nro_documento = nro_documento_v.get()
        fecha_nac_d = fecha_nac_d_v.get()
        fecha_nac_m = fecha_nac_m_v.get()
        fecha_nac_a = fecha_nac_a_v.get()
        peso = peso_v.get()
        if tree.selection():
            valor = tree.selection()
            error = ""
            error += self.comprobacion_modificar(
                nombre_y_apellido,
                nro_documento,
                fecha_nac_d,
                fecha_nac_m,
                fecha_nac_a,
                peso,
                valor,
                tree,
            )
            if not error:
                item_seleccionado = tree.focus()
                valor_id = tree.item(item_seleccionado)
                edad = relativedelta(
                    datetime.now(), datetime(fecha_nac_a, fecha_nac_m, fecha_nac_d)
                )
                nombre = nombre_y_apellido[0 : nombre_y_apellido.rfind(" ")]
                apellido = nombre_y_apellido[
                    nombre_y_apellido.rfind(" ") + 1 : len(nombre_y_apellido)
                ]
                if fecha_nac_d < 10:
                    fecha_nac = "0" + str(fecha_nac_d)
                else:
                    fecha_nac = str(fecha_nac_d)
                if fecha_nac_m < 10:
                    fecha_nac += "0" + str(fecha_nac_m)
                else:
                    fecha_nac += str(fecha_nac_m)
                fecha_nac += str(fecha_nac_a)
                fecha_nac += "f"
                actualizar = socios.update(
                    nombre=nombre,
                    apellido=apellido,
                    edad=edad.years,
                    peso=peso,
                    dni=nro_documento,
                    fecha_nac=fecha_nac,
                ).where(socios.id == valor_id["text"])
                actualizar.execute()
                self.actualizar_treeview(tree)
                showinfo("Modificación exitosa", "El socio ha sido modificado")
            else:
                showerror("Error al modificar", error)
        else:
            showerror("Error al modificar", "Elije primero el socio a modificar")

    # C
    def consulta(self, tree):
        if tree.selection():
            valor = tree.selection()
            item = tree.item(valor)
            info = (
                "Nombre y Apellido: "
                + str(item["values"][0])
                + " "
                + str(item["values"][1])
                + "\n"
            )
            info += "DNI: " + str(item["values"][4]) + "\n"
            info += "Edad: " + str(item["values"][2]) + "\n"
            info += "Peso: " + str(item["values"][3])
            showinfo("Información del socio", info)

    def actualizar_treeview(self, mitreview):
        records = mitreview.get_children()
        for element in records:
            mitreview.delete(element)
        for fila in socios.select().order_by(socios.id.desc()):
            mitreview.insert(
                "",
                0,
                text=fila.id,
                values=(
                    fila.nombre,
                    fila.apellido,
                    fila.edad,
                    fila.peso,
                    fila.dni,
                    fila.fecha_nac,
                ),
            )
