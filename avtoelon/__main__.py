from tkinter import * 
import gui



root = Tk()
root.title("Парсер сайта tashkent.hh.uz")
root.geometry('600x400')
root.resizable(width=False, height=False)

top_menu = Frame(root, bg="white", height=65)
top_menu.pack(fill=X)
top_menu.pack_propagate(False)

gui.first_page(root)

root.mainloop()
