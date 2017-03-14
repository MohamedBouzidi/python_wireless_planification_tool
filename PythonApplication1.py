from Window import *

WINDOW_WIDTH  = 1024
WINDOW_HEIGHT = 640

root = tk.Tk()
root.geometry(str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT))
root.minsize(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
root.title("Planificateur")
win = Window(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
win.pack(fill=tk.BOTH, expand=1)
root.mainloop()