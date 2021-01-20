from tkinter import *

root = Tk()
root.geometry("600x400")
root.resizable(False, False)

fram_one = Frame(root)
lab = Label(fram_one, text="hello world", pady=20, bg="white")
line = Frame(root, bg="grey")

fram_one.pack(fill=X)
line.pack(fill=X)
lab.pack(fill=X)

root.mainloop()
