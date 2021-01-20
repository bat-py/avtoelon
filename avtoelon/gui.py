from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import my_parser

def ending_of_the_word(num: int, word: list):
    if 5 <= num < 21:
        return word[2]
    elif num%10 == 1:
        return word[0]
    elif 1 < num%10 < 5:
        return word[1]
    else:
        return word[2]


class CheckButton:
    def __init__(self, master, title, url):
        self.var = StringVar()
        self.var.set("")
        self.title = title
        self.cb = Checkbutton(
            master, text=self.title, variable=self.var,
            onvalue=url, offvalue="", anchor=W,  bg="white")
        self.cb.pack(fill=X)

        self.cb.bind('<Enter>', self.enter_func)                 # Запустит метод enter_func если мышка находится в этом виджете
        self.cb.bind('<Leave>', self.leave_func)                 # Запустит leave_func как только мышка покинет зону виджета

    def enter_func(self, event):
            event.widget['bg'] = 'grey'

    def leave_func(self, event):
            event.widget['bg'] = 'white'


class ScrollBar:
    def __init__(self, main_frame):
        # Create a Canvas
        self.my_canvas = Canvas(main_frame)
        self.my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        # Add a scrollbar to the canvas
        self.my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=self.my_canvas.yview)
        self.my_scrollbar.pack(side=RIGHT, fill=Y)

        # Configure The Canvas
        self.my_canvas.configure(yscrollcommand=self.my_scrollbar.set)

        # Configure mousewheel
        self.my_canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        # Create Another Frame INSIDE the canvas
        self.frame_in_canvas  = Frame(self.my_canvas)

        # Add that New Frame to a Window in the canvas
        self.my_canvas.create_window((0,0), window=self.frame_in_canvas, anchor="nw", tags="my_tag")

        # Continue of canvas' configuration
        self.my_canvas.bind('<Configure>', self.canvas_configure)              # <Configure> можно использовать только один раз. Если создать два конфига то первый работать не будет.


    def on_mousewheel(self, event):
        self.my_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def canvas_configure(self, event):
        self.width = event.width - 4                                           # Это чтобы узнать размер canvas. От него отнемали 4, это потому что в конце 4 пикчеля занимает scrollbar
        self.my_canvas.itemconfigure("my_tag", width=self.width)               # Без этого frame внутри canvas не сможет занимать всё пространство. Мы узнали горизонтальный размер canvas и размер frame_in_canvas сделали столько же
        self.my_canvas.configure(scrollregion=self.my_canvas.bbox("all"))      # Без него список можно прокручивать бесконечно, даже если елементы закончились


def all_on_off(change):
    if change == "on":
        for ch in buttons:
            ch.cb.select()
    elif change == "off":
        for ch in buttons:
            ch.cb.deselect()


def next_page_button(first_window, root):
    checked_buttons = []
    for ch in buttons:
        if ch.var.get():
            title = ch.title
            url = str(ch.var.get())

            checked_buttons.append((title, url))

    if checked_buttons:
        first_window.destroy()
        second_page(checked_buttons, root)
    else:
        messagebox.showwarning("Ошибка!", "Вы не выбрали ни одну профессию\nПожалуйста выберите хотябы одну профессию")


def first_page(root):
    first_windows = Frame(root)

    lab = Label(first_windows, text='Пожалуйста выберите нужные вам профессии')
    lab.config(font=("Calibri", 14, "bold"))


    # Получаем список профессий
    dic_item = my_parser.list_jobs()
    list_item = dic_item.items()

    # В этом фрэйме будет список профессий чтобы в виде checkbox
    inner_frame = Frame(first_windows,  bg="white", width=500, height=260, bd=2, relief=GROOVE)

    # Создаем объект который имеет прокрутку
    frame_in_canvas = ScrollBar(inner_frame)
    
    global buttons
    buttons = []
    for name, url in list_item:
        buttons.append(CheckButton(frame_in_canvas.frame_in_canvas, name, url))
    

    # Кнопки "Все ВКЛ", "Все ОТКЛ"
    buttons_on_off = Frame(first_windows)
    Button(buttons_on_off, text="Все ВКЛ", padx=6, font="Calibri 11", relief=GROOVE, command=lambda: all_on_off("on")).pack(side=LEFT, padx=(25, 6))
    Button(buttons_on_off, text="Все ВЫКЛ", padx=6, font="Calibri 11", relief=GROOVE, command=lambda: all_on_off("off")).pack(side=RIGHT)



    # Кнопка Далее
    but = Button(first_windows, text="Далее", padx=6, bd=2, relief=GROOVE, font="Calibri", command=lambda: next_page_button(first_windows, root))


    # Pack system
    first_windows.pack(fill=BOTH, expand=1)
    lab.pack(pady=18)
    inner_frame.pack()
    inner_frame.pack_propagate(False)
    buttons_on_off.pack(side=LEFT)
    but.pack(padx=25, pady=15, side=RIGHT)


def second_page(checked_buttons, root):
    main_frame = Frame(root)

    lab_text = f"Вы выбрали {len(checked_buttons)} {ending_of_the_word(len(checked_buttons), ['профессию', 'профессии', 'профессий'])}"
    lab = Label(main_frame, text=lab_text, font=("Calibri", 14, "bold"))

    # Pack System
    main_frame.pack(fill=BOTH, expand=1)
    lab.pack(pady=18)

    