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


        # Top Frame settings
        self.top_menu = tk.Frame(self, bg="white", height=65, pady=5)
        self.top_menu.pack(fill=tk.X)
        self.top_menu.pack_propagate(False)
        
        # Image In the LEFT side of Frame
        my_image = Image.open('images/hh.png')
        my_image = my_image.resize((53, 53), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(my_image)
        
        image_lab = tk.Label(self.top_menu, image=image)
        image_lab.pack(side=tk.LEFT, padx=5)

        about_program = 'С помощью этой программы вы можете скачать объявления из сайта tashkent.hh.uz\nОбъявления можно сохранить в xlsx (Excel) или в csv формате'
        doc_label = tk.Label(self.top_menu, text=about_program)
        doc_label.pack(side=tk.RIGHT)
        
        gui.FirstPage(self)



        self.mainloop()
Root()
