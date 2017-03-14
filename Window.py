from ApCanvas import *
from tkinter import ttk


class Window(tk.Frame):

    CONTROLS_SIZE = 80

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Frame panels
        self._control = None
        self._canvas = None

        # Button images
        self._new_image = tk.PhotoImage(file="assets_small/new.png")
        #self._del_image = tk.PhotoImage(file="assets_small/delete.png")
        self._bar_image = tk.PhotoImage(file="assets_small/barriere.png")
        #self._fit_image = tk.PhotoImage(file="assets_small/fit.png")
        #self._zin_image = tk.PhotoImage(file="assets_small/zoomin.png")
        #self._zou_image = tk.PhotoImage(file="assets_small/zoomout.png")
        self._sig_image = tk.PhotoImage(file="assets_small/signalstrength.png")
        self._sav_image = tk.PhotoImage(file="assets_small/save.png")
        self._opn_image = tk.PhotoImage(file="assets_small/open.png")
        self._stn_image = tk.PhotoImage(file="assets_small/new_station.png")
        self._remove = tk.PhotoImage(file="assets_small/remove.png")

        # Dropdown menus
        self._drop_menu= None
        self._drop_label = None
        self._drop_label_var = tk.StringVar()
        self._drop_label_var.set("Obstacle")
        self._drop_menu_var = tk.StringVar()
        self._drop_values = tuple(Obstacle.MATERIALS.keys())

        # Frame indicator
        #self._indicator_label = None

        # Slider Thing
        self._slider = None
        self._slider_label = None
        self._slider_label_var = tk.StringVar()
        self._slider_label_var.set("Puissance")

        # Fetch window size for widget placement
        keys = kwargs.keys()
        if "height" in keys:
            self._height = kwargs.get("height")
        if "width" in keys:
            self._width = kwargs.get("width")

        self.build_layout()

    def update_slider(self, event):
        self._canvas.update_zone(int(self._slider.get()))

    def update_dropdown(self, event):
        self._canvas.update_material(self._drop_menu.get())

    def build_layout(self):
        self._control = tk.LabelFrame(self, width=self._width, height=self.CONTROLS_SIZE, background="#EEE")
        self._canvas = ApCanvas(self, background="Blue", width=self._width, height=self._height - self.CONTROLS_SIZE)
        self._control.pack(side=tk.TOP, fill=tk.X)
        self._canvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

        # Widget Definitions
        # Buttons
        #button_zin = tk.Button(self._control, image=self._zin_image, borderwidth=0)
        #button_zou = tk.Button(self._control, image=self._zou_image, borderwidth=0)
        #button_fit = tk.Button(self._control, image=self._fit_image, borderwidth=0)
        button_sav = tk.Button(self._control, image=self._sav_image, borderwidth=0, command=self._canvas.save)
        button_opn = tk.Button(self._control, image=self._opn_image, borderwidth=0, command=self._canvas.load)
        #button_del = tk.Button(self._control, image=self._del_image, borderwidth=0, command=self._canvas.remove_item)
        button_remove = tk.Button(self._control, image=self._remove, borderwidth=0, command=self._canvas.remove_item)
        button_new = tk.Button(self._control, image=self._new_image, borderwidth=0, command=lambda: self._canvas.add_item(CanvasItem.ACCESS))
        button_stn = tk.Button(self._control, image=self._stn_image, borderwidth=0, command=lambda: self._canvas.add_item(CanvasItem.STATION))
        button_bar = tk.Button(self._control, image=self._bar_image, borderwidth=0, command=lambda: self._canvas.add_item(CanvasItem.OBSTACLE))

        # Indicator bar
        #self._indicator_label = tk.LabelFrame(self._control)
        #label_left = tk.Label(self._indicator_label, text="-35dbm", font="Arial 16")
        #label_right = tk.Label(self._indicator_label, text="-90dbm", font="Arial 16")
        #label_img = tk.Label(self._indicator_label, image=self._sig_image)
        #label_left.pack(side="left")
        #label_img.pack(side="left")
        #label_right.pack(side="right")

        # Slider Thing
        self._slider = ttk.Scale(self._control, from_=100, to=250, orient=tk.HORIZONTAL)
        self._slider_label = ttk.Label(self._control, textvariable=self._slider_label_var, font=("Arial 12"), width=9)

        # Dropdown menus
        self._drop_menu = ttk.Combobox(self._control, textvariable=self._drop_menu_var, font=("Arial 12"), width=10, state='readonly')
        self._drop_label = ttk.Label(self._control, textvariable=self._drop_label_var, font=("Arial 12"), width=8)
        self._drop_menu["values"] = self._drop_values
        self._drop_menu.current(0)

        # Widget Placement
        button_opn.pack(side=tk.LEFT)
        button_sav.pack(side=tk.LEFT)
        self._slider_label.pack(side=tk.LEFT, padx=10)
        #self._indicator_label.pack(side=tk.LEFT, expand=1)
        self._slider.pack(side=tk.LEFT)
        self._drop_label.pack(side=tk.LEFT, padx=10)
        self._drop_menu.pack(side=tk.LEFT)
        #button_zin.pack(side=tk.RIGHT)
        #button_zou.pack(side=tk.RIGHT)
        #button_fit.pack(side=tk.RIGHT)
        button_remove.pack(side=tk.RIGHT, padx=10)
        button_stn.pack(side=tk.RIGHT)
        button_bar.pack(side=tk.RIGHT)
        #button_del.pack(side=tk.RIGHT)
        button_new.pack(side=tk.RIGHT)

        self._slider.bind("<B1-Motion>", self.update_slider)
        self._drop_menu.bind("<Button-1>", self.update_dropdown)
