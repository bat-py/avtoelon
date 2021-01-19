from tkinter import *
from tkinter import ttk           # ttk нужно импортировать отдельно


root = Tk()
root.geometry("600x400")

# Create a Main Frame
main_frame = Frame(root, bg="green")
main_frame.pack(fill=BOTH, expand=1)


# Create a Canvas
my_canvas = Canvas(main_frame)
my_canvas.pack(side=LEFT, fill=BOTH, expand=1)      # side=LEFT потому что мы еще должны поместить в правую сторону наш scrollbar


# Add a scrollbar to the canvas
my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)  # обрати внимание scrollbar должен находится не внутри Canvas а внутри main_frame
my_scrollbar.pack(side=RIGHT, fill=Y)


# Configure The Canvas
my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))



# Configure mousewheel
def on_mousewheel(event):
    my_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

# For Windows
#my_canvas.bind_all("<MouseWheel>", on_mousewheel)

# For X11
my_canvas.bind_all("<Button-4>", on_mousewheel)
my_canvas.bind_all("<Button-5>", on_mousewheel)




# Create Another Frame INSIDE the canvas
frame_in_canvas  = Frame(my_canvas)


# Add that New Frame to a Window in the canvas
my_canvas.create_window((0,0), window=frame_in_canvas, anchor=N+W)




for thing in range(100):
    Button(frame_in_canvas, text=f"Button {thing+1}").grid(column=0, row=thing)



root.mainloop()
