from Form import *

class Circle(Form):
    def __init__(self, canvas, x, y, r, color, start=0, extent=359):
        super().__init__(canvas, x, y, color)
        self._r = r
        self._start = start
        self._extent = extent
        self._id = None
        

    def draw(self):
        self._id = self._canvas.create_arc(self._x - self._r, self._y - self._r, self._x + self._r, self._y + self._r, fill=self._color, outline="", start=self._start, extent=self._extent)

    def change_color(self, color):
        self._canvas.itemconfig(self._id, fill=color)

    def set_start(self, s):
        self._canvas.itemconfig(self._id, start=s)

    def set_extent(self, e):
        self._canvas.itemconfig(self._id, extent=e)

    def set_radius(self, r):
        self._r = r
        self._canvas.coords(self._id, self._x - self._r, self._y - self._r, self._x + self._r, self._y + self._r)

    def get_radius(self):
        return self._r

    @staticmethod
    def equation(radius, x0, y, y0):
        return -(math.sqrt(radius**2 - (y-y0)**2) - x0)

    def has_point(self, x, y):
        if ((x > self._x - self._r) and (x < self._x + self._r)):
            if ((y > self._y - self._r) and (y < self._y + self._r)):
               return True
        return False