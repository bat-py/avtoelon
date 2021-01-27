import tkinter as tk
import gui
from ttkthemes import ThemedStyle

class Root(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        
        self.title("Парсер сайта tashkent.hh.uz")
        self.geometry('600x400')
        self.resizable(width=False, height=False)

        style = ThemedStyle(self)
        style.set_theme('breeze')

        top_menu = tk.Frame(self, bg="white", height=65)
        top_menu.pack(fill=tk.X)
        top_menu.pack_propagate(False)

        gui.FirstPage(self)

        self.mainloop()

Root()
