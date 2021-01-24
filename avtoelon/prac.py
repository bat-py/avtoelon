import sys
from tkinter import ttk
from tkinter import *

mGui = Tk()

mGui.geometry('450x450')
mGui.title('Hanix Downloader')

mpb = ttk.Progressbar(mGui,orient ="horizontal",length = 200, mode ="determinate", maximum=100)
mpb.pack()
mpb["value"] = 50

mGui.mainloop()