import tkinter as tk
import gui
from ttkthemes import ThemedStyle
from PIL import ImageTk, Image
import os
from tkinter import ttk

class Root(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        
        self.title("Парсер сайта tashkent.hh.uz")
        self.geometry('600x400')
        self.resizable(width=False, height=False)
       
        path = os.path.dirname(__file__)
#        self.iconbitmap(path+'/images/hh.ico')

        style = ThemedStyle(self)
        style.set_theme('breeze')

        self.top_menu = tk.Frame(self)
        self.top_menu.pack()

        imag = tk.PhotoImage(file='hh.png')
        lab = tk.Label(self, image=imag)
        lab.pack()
 
        gui.FirstPage(self)


#        my_image = ImageTk.PhotoImage(Image.open('./images/hh.png'))
#        image_lab = tk.Label(self.top_menu, image=my_image)
#        image_lab.pack()

        self.mainloop()
Root()
