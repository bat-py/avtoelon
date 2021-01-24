import tkinter as tk
from tkinter import ttk


class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)                                # мы не создаем root. Просто теперь вместо self.root используем просто self
        self.geometry("400x400")
        self.button = ttk.Button(text="start", command=self.start)
        self.button.pack()
        self.progress = ttk.Progressbar(self, orient="horizontal",       # Как видишь первый парамет у нас теперь self а не root или к>
                                        length=200, mode="determinate")
        self.progress.pack()

        self.bytes = 0
        self.maxbytes = 50000

    def start(self):
        self.progress["value"] = 0
        self.progress["maximum"] = 50000
        self.read_bytes()

    def read_bytes(self):
        '''simulate reading 500 bytes; update progress bar'''
        self.bytes += 500
        self.progress["value"] = self.bytes
        if self.bytes < self.maxbytes:
            # read more bytes after 100 ms
            self.after(100, self.read_bytes)             # 100 это сколько ждать перед запускам (Он будет ждать 100миллисикунд и запус>

app = SampleApp()
app.mainloop()

