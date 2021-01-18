from tkinter import * 
import parser
import gui



root = Tk()
root.title("Парсер сайта tashkent.hh.uz")
root.geometry('600x400')
root.resizable(width=False, height=False)

gui.first_page(root)


root.mainloop()
