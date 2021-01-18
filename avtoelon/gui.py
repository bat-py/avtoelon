from tkinter import *
import my_parser

class CheckButton:
    def __init__(self, master, title, url):
        self.var = StringVar()
        self.var.set("")
        self.title = title
        self.url = url
        self.cb = Checkbutton(
            master, text=title, variable=self.var,
            onvalue=self.url, offvalue="", anchor=W, bg="white")
        self.cb.pack(fill=X)




def first_page(root):
    first_windows = Frame(root)
    first_windows.pack(fill=BOTH)
    
    lab = Label(first_windows, text='Пожалуйста выберите нужные вам профессии')
    lab.config(font=("Arial", 14, "bold"))


# В этом фрэйме будет список профессий чтобы в виде checkbox  
    inner_frame = Frame(first_windows,  bg="white", width=500, height=280)

    dic_item = my_parser.list_jobs()
    list_item = dic_item.items()

    
    buttons = []
    for name, url in list_item:
        buttons.append(CheckButton(inner_frame, name, url))


# Переход на 2 страницу
    but = Button(first_windows, text="Далее", padx=5, pady=2, font="Arial")

# Pack system
    lab.pack(pady=18)
    inner_frame.pack()
    inner_frame.pack_propagate(False)
    but.pack(padx=25, pady=15, side=RIGHT)
