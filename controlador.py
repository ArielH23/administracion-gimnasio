from tkinter import Tk
from vista import Ventana

if (
    __name__ == "__main__"
):  # si se abre directamente adg_vista.py se ejecuta lo de adentro sinoroot = Tk()
    root = Tk()
    obj1 = Ventana(root)
    root.mainloop()
