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
       
        self.iconbitmap(self.path+'images/hh.ico')

        style = ThemedStyle(self)
        style.set_theme('breeze')


    # Top Frame settings
        self.top_menu = tk.Frame(self, bg="white", height=65, pady=5)
        self.top_menu.pack(fill=tk.X)
        self.top_menu.pack_propagate(False)
        
        # Image In the LEFT side of Top Menu
        my_image = Image.open(self.path+'images/hh.png')
        my_image = my_image.resize((53, 53), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(my_image)
        image_lab = tk.Label(self.top_menu, image=image)

        # DOC in the RIGHT side of Top Top Menu
        style = ttk.Style().configure('top.TLabel', background='white')
        about_program = 'С помощью этой программы вы можете скачать объявления из сайта tashkent.hh.uz\nОбъявления можно сохранить в xlsx (Excel) или в csv форматах'
        doc_label = ttk.Label(self.top_menu, text=about_program, style='top.TLabel')

        image_lab.grid(row=0, column=0, padx=7)
        doc_label.grid(row=0, column=1)






        gui.FirstPage(self)
        self.mainloop()
Root()
