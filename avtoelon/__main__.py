from tkinter import * 
import parser

root = Tk()
root.title("Парсер сайта tashkent.hh.uz")
root.geometry('600x400')
root.resizable(width=False, height=False)


# Первая страница (выбор по марке или по городу)
def first_page():
    first_windows = Frame()
    first_windows.pack(fill=BOTH)
    
    lab = Label(first_windows, text='\n  Пожалуйста выберите нужные вам профессии\n', anchor=E, bg='grey')

# В r нем хранится выбор пользователя

# Переход на 2 страницу
    but = Button(first_windows, text="Далее", padx=5, pady=2)

# Pack system
    lab.pack(pady=(10,300))
    but.pack()




first_page()

root.mainloop()
