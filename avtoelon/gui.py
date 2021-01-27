from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import my_parser
import os
from tkinter import filedialog
import writer 

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
        
        self.check_but_style = ttk.Style()
        self.check_but_style.configure('ass.TCheckbutton', background='white')

        self.cb = ttk.Checkbutton(master,
                                  text=self.title, 
                                  variable=self.var,
                                  onvalue=url, 
                                  offvalue="",
                                  style='ass.TCheckbutton'
                                  )
        self.cb.pack(fill=X)


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
        self.frame_in_canvas  = ttk.Frame(self.my_canvas)

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

        self.lab = ttk.Label(self.first_windows, text='Пожалуйста выберите нужные вам профессии', anchor=W )
        self.lab.config(font=("Calibri", 11))

        # Получаем список профессий
        self.dic_item = my_parser.list_jobs(self.root, messagebox)
        self.list_item = self.dic_item.items()

        # В этом фрэйме будет список профессий чтобы в виде checkbox
        self.inner_frame = Frame(self.first_windows, bg="white", width=500, height=240, bd=2, relief=GROOVE)

        # Создаем объект который имеет прокрутку
        self.frame_in_canvas = ScrollBar(self.inner_frame)

        self.buttons = []
        # Создаем checkbuttons для каждого типа профессий
        for name, url in self.list_item:
            self.buttons.append(CheckButton(self.frame_in_canvas.frame_in_canvas, name, url))
    

        # Кнопки "Все ВКЛ", "Все ОТКЛ"
        self.buttons_on_off = ttk.Frame(self.first_windows)
        self.turn_on_all = ttk.Button(self.buttons_on_off, text="ВКЛ все", command=lambda: self.all_on_off(1))
        self.turn_off_all = ttk.Button(self.buttons_on_off, text="ВЫКЛ все", command=lambda: self.all_on_off(0))




        # Кнопка Далее
        self.but = ttk.Button(self.first_windows, text="Далее", command=self.next_page_button)



        # Pack system
        self.first_windows.pack(fill=BOTH, expand=1)
        self.lab.pack(pady=(15,6), fill=X, padx=15)
        self.inner_frame.pack()
        self.inner_frame.pack_propagate(False)
        self.buttons_on_off.pack(side=LEFT)
        self.turn_on_all.pack(side=LEFT, padx=(25, 6))
        self.turn_off_all.pack(side=RIGHT)
        self.but.pack(padx=25, side=RIGHT)

    def all_on_off(self, on_or_off):
        '''Функция сначала выберит все checkbuttons и
        если было нажата кнопка ВЫКЛ тогда через invoke() отключает их всех'''
        for ch in self.buttons:
            ch.cb.state(['selected'])

        if not on_or_off:
            for ch in self.buttons:
                ch.cb.invoke()


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
        self.lab = ttk.Label(self.main_frame, text=lab_text, anchor=W)

        self.frame_file_expansion = ttk.LabelFrame(self.main_frame, text="Выберите тип файла")

        self.file_expansion_val = StringVar()
        self.file_expansion_val.set("xlsx")

        self.xlsx_expansion = ttk.Radiobutton(self.frame_file_expansion,
                                    text="В формате xlsx (Excel)",
                                    value='xlsx',
                                    variable=self.file_expansion_val,
                                    cursor="hand2",
                                    command=self.asshole,
                                    )

        self.csv_expansion = ttk.Radiobutton(self.frame_file_expansion,
                                text="В формате csv",
                                value='csv',
                                variable=self.file_expansion_val,
                                cursor="hand2",
                                command=self.asshole
                                )

        self.frame_select_place = ttk.LabelFrame(self.main_frame, text="Выберите место для сохранение файла")
        self.selected_place = ttk.Entry(self.frame_select_place, width=52)


        self.file_name = 'parsed_data'

        if os.name == 'nt':
            self.selected_place.insert(0, os.path.dirname(__file__)+"\parsed_data."+self.file_expansion_val.get())
            self.selected_place.config(state=DISABLED)
        else:
            self.selected_place.insert(0, os.path.dirname(__file__)+"/parsed_data."+self.file_expansion_val.get())
            self.selected_place.config(state=DISABLED)

        self.s = ttk.Style()
        self.s.configure('TButton', font=('Helvetica', 8))


        self.button_save_as = ttk.Button(self.frame_select_place,
                                    text="Сохранить как",
                                    command=self.select_place_to_save,
                                    style='TButton'
                                )


        # Кнопка "скачать данных"
        self.download_button = ttk.Button(self.main_frame,
                                    text="Скачать данных",
                                    command=self.download_data)




        # Pack System
        self.main_frame.pack(fill=BOTH, expand=1)
        self.lab.pack(pady=(15,4), fill=X, padx=15)

        self.frame_file_expansion.pack(fill=X, padx=40, ipady=5)
        self.xlsx_expansion.pack(fill=X, padx=15)
        self.csv_expansion.pack(fill=X, padx=15)

        self.frame_select_place.pack(fill=X, padx=40, ipady=15, pady=25)
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

        self.selected_place.config(state=NORMAL)
        expansion = self.file_expansion_val.get()
        place = self.selected_place.get()
        self.main_frame.destroy()
        #Запускаем 3 страницу
        ThirdPage(self.root, self.checked_buttons,expansion, place)


class ThirdPage:
    def __init__(self, root, checked_buttons, file_expansion_val, selected_place):
        self.root = root
        self.main_frame = Frame(self.root)
        info = ttk.Label(self.main_frame,
                     text="Идет загрузка данных", 
                    )
        
        self.file_expansion_val = file_expansion_val
        self.selected_place = selected_place 
        self.checked_buttons = checked_buttons
        # Тут хранится порядковый номер, чтобы при рекурсивном вызове progress можно было определить где остановился последный раз
        self.checked_buttons_queue = 0
        # Тут хранится экземпляры, и каждый экземпляр хранит в себе данных одного каталога
        self.parsed_data = []
        # После того как полностью загрузится один каталог, в progressbar_value добовляется этот процент
        self.plus_value = int(100/len(self.checked_buttons))
        # Тут хранится на сколько процентов загружено данные
        self.progressbar_value = 0

        self.progressbar_frame = Frame(self.main_frame)
        self.progressbar = ttk.Progressbar(self.progressbar_frame,
                                           orient=HORIZONTAL,
                                           length=450,
                                           mode='determinate',
                                           maximum=100,
                                           value=0
                                           )
        
        self.progressbar_percent = ttk.Label(self.progressbar_frame,
                                         text=f"{self.progressbar_value}%", 
                                         anchor=W)
        
        
        # Pack System
        self.main_frame.pack(fill=BOTH)
        info.pack(padx=15, pady=(15, 4), fill=X)
        self.progressbar_frame.pack()
        self.progressbar.grid(row=0, column=0)
        self.progressbar_percent.grid(row=0, column=1)
         
        self.root.after(10, self.progress)

        
    def progress(self):
        datas_from_one_catalog = my_parser.GetItemsFromCatalog(self.checked_buttons[self.checked_buttons_queue],
                                                                   messagebox, 
                                                                   self.root)        # Мы передаем ей root, это чтобы если будут проблемы с интернетом, то класс GetItemsFromCatalog сам будет закрывать окно
        self.parsed_data.append(datas_from_one_catalog)

        if self.checked_buttons[self.checked_buttons_queue] is self.checked_buttons[-1]:
            self.progressbar["value"] = 100
            self.progressbar_percent["text"] = "100%"
            self.writer_to_file()
            return 0

        self.checked_buttons_queue += 1
        self.progressbar_value += self.plus_value 
        self.progressbar["value"] = self.progressbar_value
        self.progressbar_percent["text"] = f"{self.progressbar_value}%"
            
        self.root.after(100, self.progress)
    
    def writer_to_file(self):
            if self.file_expansion_val == 'csv':
                writer.CsvWriter(self.selected_place, self.parsed_data, self.stop)
            else:
                writer.ExcelWriter(self.selected_place, self.parsed_data, self.stop)



    def stop(self):
        messagebox.showinfo("Загрузка закончена", "Данные сохранены успешно" )
        self.root.destroy()
            









