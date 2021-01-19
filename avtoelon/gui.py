from tkinter import *
from tkinter import ttk
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
    
        def enter_leave(event):
            if str(event.type) == 'Enter':
                event.widget['bg'] = 'grey'
            elif str(event.type) == 'Leave':
                event.widget['bg'] = 'white'
    
        self.cb.bind('<Enter>', enter_leave)
        self.cb.bind('<Leave>', enter_leave)






class ScrollBar:
    def __init__(self, main_frame):
        self.main_frame = main_frame

        # Create a Canvas
        self.my_canvas = Canvas(self.main_frame)
        self.my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        # Add a scrollbar to the canvas
        self.my_scrollbar = ttk.Scrollbar(self.main_frame, orient=VERTICAL, command=self.my_canvas.yview)
        self.my_scrollbar.pack(side=RIGHT, fill=Y)

        # Configure The Canvas
        self.my_canvas.configure(yscrollcommand=self.my_scrollbar.set)
        self.my_canvas.bind('<Configure>', lambda e: self.my_canvas.configure(scrollregion = self.my_canvas.bbox("all")))


        # Configure mousewheel
        def on_mousewheel(event):
            self.my_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.my_canvas.bind_all("<MouseWheel>", on_mousewheel)

        # Create Another Frame INSIDE the canvas
        self.frame_in_canvas  = Frame(self.my_canvas)

        # Add that New Frame to a Window in the canvas
        self.my_canvas.create_window((0,0), window=self.frame_in_canvas, anchor=N+W)

    



def first_page(root):
    first_windows = Frame(root)
    first_windows.pack(fill=BOTH)
    
    lab = Label(first_windows, text='Пожалуйста выберите нужные вам профессии')
    lab.config(font=("Arial", 14, "bold"))


# В этом фрэйме будет список профессий чтобы в виде checkbox  
    inner_frame = Frame(first_windows,  bg="white", width=500, height=280)

    dic_item = my_parser.list_jobs()
    list_item = dic_item.items()

    frame_in_canvas = ScrollBar(inner_frame)
    
    buttons = []
    for name, url in list_item:
        buttons.append(CheckButton(frame_in_canvas.frame_in_canvas, name, url))
    


# Переход на 2 страницу
    but = Button(first_windows, text="Далее", padx=5, pady=2, font="Arial")

# Pack system
    lab.pack(pady=18)
    inner_frame.pack()
    inner_frame.pack_propagate(False)
    but.pack(padx=25, pady=15, side=RIGHT)
