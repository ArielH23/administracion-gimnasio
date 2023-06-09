from tkinter import Tk
from vista import Ventana

if (
    __name__ == "__main__"
):  # si se abre directamente controlador.py se ejecuta lo de adentro sino no
    root = Tk()
    obj1 = Ventana(root)
    root.mainloop()
