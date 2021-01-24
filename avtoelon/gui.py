from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import my_parser
import os
from tkinter import filedialog

def ending_of_the_word(num: int, word: list):
    if 5 <= num < 21:
        return word[2]
    elif num%10 == 1:
        return word[0]
    elif 1 < num%10 < 5:
        return word[1]
    else:
        return word[2]

class EnterLeave:
    def __init__(self, enter_bg, leave_bg):
        self.enter_bg = enter_bg
        self.leave_bg = leave_bg

    def enter(self, event):
        event.widget['bg'] = self.enter_bg
    def leave(self, event):
        event.widget['bg'] = self.leave_bg


class CheckButton:
    def __init__(self, master, title, url):
        self.var = StringVar()
        self.var.set("")
        self.title = title
        self.cb = Checkbutton(
            master, text=self.title, variable=self.var,
            onvalue=url, offvalue="", anchor=W,  bg="white")
        self.cb.pack(fill=X)

        self.ass = EnterLeave('#cdcdcd', '#FFFFFF')
        self.cb.bind('<Enter>', self.ass.enter)                 # Запустит метод enter_func если мышка находится в этом виджете
        self.cb.bind('<Leave>', self.ass.leave)                 # Запустит leave_func как только мышка покинет зону виджета


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


class FirstPage:
    def __init__(self, root):
        self.root = root
        self.first_windows = Frame(self.root)

        self.lab = Label(self.first_windows, text='Пожалуйста выберите нужные вам профессии', anchor=W )
        self.lab.config(font=("Calibri", 11))

        # Получаем список профессий
        self.dic_item = my_parser.list_jobs(self.root, messagebox)
        self.list_item = self.dic_item.items()

        # В этом фрэйме будет список профессий чтобы в виде checkbox
        self.inner_frame = Frame(self.first_windows,  bg="white", width=500, height=240, bd=2, relief=GROOVE)

        # Создаем объект который имеет прокрутку
        self.frame_in_canvas = ScrollBar(self.inner_frame)
    
        self.buttons = []
        # Создаем checkbuttons для каждого типа профессий
        for name, url in self.list_item:
            self.buttons.append(CheckButton(self.frame_in_canvas.frame_in_canvas, name, url))
    

        # Кнопки "Все ВКЛ", "Все ОТКЛ"
        self.buttons_on_off = Frame(self.first_windows)
        self.turn_on_all = Button(self.buttons_on_off, text="Все ВКЛ", padx=6, font="Calibri 11", relief=GROOVE, command=lambda: self.all_on_off("on"))
        self.turn_off_all = Button(self.buttons_on_off, text="Все ВЫКЛ", padx=6, font="Calibri 11", relief=GROOVE, command=lambda: self.all_on_off("off"))




        # Кнопка Далее
        self.but = Button(self.first_windows, text="Далее", padx=6, bd=2, relief=GROOVE, font="Calibri 11", command=self.next_page_button)


        # Bind настройки
        ent_leav_object = EnterLeave('#cdcdcd', '#f0f0f0')
        self.turn_on_all.bind('<Enter>', ent_leav_object.enter)
        self.turn_on_all.bind('<Leave>', ent_leav_object.leave)

        self.turn_off_all.bind('<Enter>', ent_leav_object.enter)
        self.turn_off_all.bind('<Leave>', ent_leav_object.leave)

        self.but.bind('<Enter>', ent_leav_object.enter)
        self.but.bind('<Leave>', ent_leav_object.leave)


        # Pack system
        self.first_windows.pack(fill=BOTH, expand=1)
        self.lab.pack(pady=(15,4), fill=X, padx=15)
        self.inner_frame.pack()
        self.inner_frame.pack_propagate(False)
        self.buttons_on_off.pack(side=LEFT)
        self.turn_on_all.pack(side=LEFT, padx=(25, 6))
        self.turn_off_all.pack(side=RIGHT)
        self.but.pack(padx=25, side=RIGHT)

    def all_on_off(self, change):
        if change == "on":
            for ch in self.buttons:
                ch.cb.select()
        elif change == "off":
            for ch in self.buttons:
                ch.cb.deselect()

    def next_page_button(self):
        self.checked_buttons = []

        for ch in self.buttons:
            if ch.var.get():
                self.title_ = ch.title
                self.url_ = str(ch.var.get())

                self.checked_buttons.append((self.title_, self.url_))

        if self.checked_buttons:
            self.first_windows.destroy()
            SecondPage(self.checked_buttons, self.root)
        else:
            messagebox.showerror("Ошибка!", "Вы не выбрали ни одну профессию\nПожалуйста выберите хотябы одну профессию")


class SecondPage:
    def __init__(self,checked_buttons, root):
        self.root = root
        self.main_frame = Frame(root)
        self.checked_buttons = checked_buttons
        lab_text = f"Вы выбрали {len(self.checked_buttons)} {ending_of_the_word(len(self.checked_buttons), ['профессию', 'профессии', 'профессий'])}"
        self.lab = Label(self.main_frame, text=lab_text, font=("Calibri", 11), anchor=W)

        self.frame_file_expansion = LabelFrame(self.main_frame, text="Выберите тип файла", pady=5)

        self.file_expansion_val = StringVar()
        self.file_expansion_val.set("xlsx")


        self.xlsx_expansion = Radiobutton(self.frame_file_expansion,
                                    text="В формате xlsx (Excel)",
                                    value='xlsx',
                                    variable=self.file_expansion_val,
                                    cursor="hand2",
                                    anchor=W,
                                    command=self.asshole
                                    )

        self.csv_expansion = Radiobutton(self.frame_file_expansion,
                                text="В формате csv",
                                value='csv',
                                variable=self.file_expansion_val,
                                cursor="hand2",
                                anchor=W,
                                command=self.asshole
                                )

        self.frame_select_place = LabelFrame(self.main_frame, text="Выберите место для сохранение файла")
        self.selected_place = Entry(self.frame_select_place, width=58)

        self.file_name = 'parsed_data'
        self.file_expansion_val.get()

        if os.name == 'nt':
            self.selected_place.insert(0, os.path.dirname(__file__)+"\parsed_data."+self.file_expansion_val.get())
            self.selected_place.config(state=DISABLED)
        else:
            self.selected_place.insert(0, os.path.dirname(__file__)+"/parsed_data."+self.file_expansion_val.get())
            self.selected_place.config(state=DISABLED)

        self.button_save_as = Button(self.frame_select_place,
                                    text="Сохранить как",
                                    padx=6,
                                    bd=2,
                                    relief=GROOVE,
                                    font="Calibri 10",
                                    command=self.select_place_to_save,
                                )


        # Кнопка "скачать данных"
        self.download_button = Button(self.main_frame,
                                    text="Скачать данных",
                                    padx=6,
                                    bd=2,
                                    relief=GROOVE,
                                    font="Calibri 10",
                                    command=self.download_data)


        # Bind настройки
        ent_leav_object = EnterLeave('#cdcdcd', '#f0f0f0')
        self.download_button.bind('<Enter>', ent_leav_object.enter)
        self.download_button.bind('<Leave>', ent_leav_object.leave)


        # Pack System
        self.main_frame.pack(fill=BOTH, expand=1)
        self.lab.pack(pady=(15,4), fill=X, padx=15)

        self.frame_file_expansion.pack(fill=X, padx=50)
        self.xlsx_expansion.pack(fill=X, padx=15)
        self.csv_expansion.pack(fill=X, padx=15)

        self.frame_select_place.pack(fill=X, padx=50, ipady=15, pady=25)
        self.selected_place.pack(side=LEFT, fill=X, padx=(15,0))
        self.button_save_as.pack(side=RIGHT, padx=15)

        self.download_button.pack(side=RIGHT, padx=25, pady=(20, 0))

    def asshole(self):
        self.selected_place.config(state=NORMAL)

        if self.file_expansion_val.get() == 'xlsx':
            self.place = self.selected_place.get().replace('csv','xlsx')
        elif self.file_expansion_val.get() == 'csv':
            self.place = self.selected_place.get().replace('xlsx', 'csv')


        self.selected_place.delete(0, END)
        self.selected_place.insert(0, self.place)
        self.selected_place.config(state=DISABLED)

    def select_place_to_save(self):
        s = filedialog.asksaveasfilename(title="Куда вы хотите сохранить файл",
                                         initialfile=self.file_name,
                                         defaultextension=self.file_expansion_val.get())

        self.selected_place.config(state=NORMAL)
        self.selected_place.delete(0, END)
        self.selected_place.insert(0, s)
        self.selected_place.config(state=DISABLED)

    def download_data(self):
        if not self.selected_place:
            if os.name == 'nt':
                self.selected_place = os.path.dirname(__file__) + "\parsed_data." + self.file_expansion_val.get()
            else:
                self.selected_place = os.path.dirname(__file__) + "/parsed_data." + self.file_expansion_val.get()

        self.main_frame.destroy()

        #Запускаем 3 страницу
        ThirdPage(self.root, self.checked_buttons)


class ThirdPage:
    def __init__(self, root, checked_buttons):
        self.root = root
        self.main_frame = Frame(self.root)
        info = Label(self.main_frame,
                     text="Идет загрузка данных", 
                     anchor=W, 
                     font=("Calibri", 11))
        
        self.checked_buttons = checked_buttons
        # Тут хранится порядковый номер, чтобы при рекурсивном вызове progress можно было определить где остановился последный раз
        self.checked_buttons_queue = 0
        # Тут хранится экземпляры, и каждый экземпляр хранит в себе данных одного каталога
        self.parsed_data = []
        # После того как полностью загрузится один каталог, в progressbar_value добовляется этот процент
        self.plus_value = int(100/len(self.checked_buttons))
        # Тут хранится на сколько процентов загружено данные
        self.progressbar_value = 0


        self.progressbar = ttk.Progressbar(self.main_frame,
                                           orient=HORIZONTAL,
                                           length=300,
                                           mode='determinate',
                                           maximum=100)
        
        self.progressbar_percent = Label(self.main_frame, 
                                         text=f"{self.progressbar_value}%", 
                                         anchor=W)
        
        
        # Pack System
        self.main_frame.pack()
        info.pack(padx=15, pady=(15, 4))
        self.progressbar.pack(side=LEFT)
        self.progressbar_percent.pack(side=RIGHT)
        
        self.progress()

        
    def progress(self):
        datas_from_one_catalog = my_parser.GetItemsFromCatalog(self.checked_buttons[self.checked_buttons_queue],
                                                                   messagebox, 
                                                                   self.root)        # Мы передаем ей root, это чтобы если будут проблемы с интернетом, то класс GetItemsFromCatalog сам будет закрывать окно
        self.parsed_data.append(datas_from_one_catalog)

        if self.checked_buttons[self.checked_buttons_queue] is self.checked_buttons[-1]:
            self.progressbar["value"] = 100
            self.progressbar_percent["text"] = "100%"
            self.stop()

        self.checked_buttons_queue += 1
        self.progressbar_value += self.plus_value 
        self.progressbar["value"] = self.progressbar_value
        self.progressbar_percent["text"] = f"{self.progressbar_value}%"
            
        self.root.after(100, self.progress)

    def stop(self):
        messagebox.showinfo("Загрузка закончена", "Данные сохранены успешно" )
        self.root.destroy()
            









