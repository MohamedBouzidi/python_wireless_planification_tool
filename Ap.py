from Zone import *
from CanvasItem import *

IMAGESIZE = 47

class Ap(Form, CanvasItem):
    def __init__(self, canvas, x=150, y=150, r=100, color="red"):
        Form.__init__(self, canvas, x, y, color)
        CanvasItem.__init__(self)
        self._image = tk.PhotoImage(file="assets/ap.png")

        if (r > 0):
            self._radius = r
        else:
            self._radius = 50

        self._id = None
        self._cover = Zone(self._canvas, self._x, self._y, self._radius, self)

    def draw(self):
        self._cover.draw()
        self._id = self._canvas.create_image(self._x, self._y, image=self._image)

    def delete(self):
        self._canvas.delete(self.get_id())
        self._cover.delete()

    def collision(self, item):
        self._cover.collision(item)

    def distance(self, x, y):
        center = Point(self._x, self._y)
        return center.distance(x,y)

    def remove(self, item):
        self._cover.remove(item)

    def move(self, x, y):
        self._cover.move(x, y)
        self._canvas.move(self._id, x - self._x, y - self._y)
        self._x = x
        self._y = y

    def has_point(self, x, y):
        if ((x >= self._x - IMAGESIZE/2) and (x <= self._x + IMAGESIZE/2)):
            if ((y >= self._y - IMAGESIZE/2) and (y <= self._y + IMAGESIZE/2)):
               return True
        return False

    def get_dims(self):
        pass

    def get_coords(self):
        return Point(self._x, self._y)

    def get_radius(self):
        return self._radius

    def set_radius(self, r):
        self._cover.set_radius(r)
        self._radius = r

    # Serialization code:
    def save(self, file):
        file.write(CanvasItem.ACCESS.to_bytes(4, "little"))
        file.write(self._x.to_bytes(4, "little"))
        file.write(self._y.to_bytes(4, "little"))
        file.write(self._radius.to_bytes(4, "little"))

    def load(self, file):
        self._x = int.from_bytes(file.read(4), "little")
        self._y = int.from_bytes(file.read(4), "little")
        self._radius = int.from_bytes(file.read(4), "little")
        self._cover = Zone(self._canvas, self._x, self._y, self._radius)
