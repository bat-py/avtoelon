import tkinter as tk
import gui
from ttkthemes import ThemedStyle
from PIL import ImageTk, Image
import os

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

        self.top_menu = tk.Frame(self, bg="white", height=65, width=600)
        self.top_menu.pack()
        self.top_menu.pack_propagate(False)

        self.top_frame()
        gui.FirstPage(self)

        self.mainloop()

    def top_frame(self):
        my_image = ImageTk.PhotoImage(Image.open('./images/hh.jpg'))
        image_lab = tk.Label(self.top_menu, image=my_image)
        image_lab.pack()
#        image = tk.PhotoImage(file='images/hh.png')
#        lab = tk.Label(self.top_menu, image=image, text='Helo').pack()

Root()
