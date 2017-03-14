from CanvasItem import *
from Form import *

class Obstacle(Form, CanvasItem):

    MATERIALS = {"air" : 0, "bois" : 220, "eau" : 50, "mur" : 90, "batiment" : 20, "verre" : 280}

    def __init__(self, canvas, x=150, y=150, w=15, h=80, type="batiment", color="black"):
        Form.__init__(self, canvas, x, y, color)
        CanvasItem.__init__(self)
        self._w = w
        self._h = h
        self._type = type

    def draw(self):
        self._id = self._canvas.create_rectangle(self._x - self._w/2, self._y - self._h/2, self._x + self._w/2, self._y + self._h/2, fill=self._color)

    def rotate(self):
        self._w, self._h = self._h, self._w
        self._canvas.coords(self._id, self._x - self._w/2, self._y - self._h/2, self._x + self._w/2, self._y + self._h/2)

    def has_point(self, x, y):
        if ((x >= self._x - self._w/2) and (x <= self._x + self._w/2)):
            if ((y >= self._y - self._h/2) and (y <= self._y + self._h/2)):
                return True
        return False

    def move(self, x, y):
        self._canvas.move(self._id, x - self._x, y - self._y)
        self._x = x
        self._y = y

    def delete(self):
        self._canvas.delete(self._id)

    def set_radius(self, r):
        if (self._w > self._h):
            self._w = r
        else:
            self._h = r
        self._canvas.coords(self._id, self._x - self._w/2, self._y - self._h/2, self._x + self._w/2, self._y + self._h/2)

    def get_dims(self):
        return (self._x - self._w/2, self._y - self._h/2, self._x + self._w/2, self._y + self._h/2)

    def get_type(self):
        return self._type

    def set_type(self, type):
        self._type = type

    def get_attenuation(self):
        return self.MATERIALS[self._type]

    # Serialization code:
    def save(self, file):
        file.write(CanvasItem.OBSTACLE.to_bytes(4, "little"))
        file.write(self._x.to_bytes(4, "little"))
        file.write(self._y.to_bytes(4, "little"))
        file.write(self._w.to_bytes(4, "little"))
        file.write(self._h.to_bytes(4, "little"))

    def load(self, file):
        self._x = int.from_bytes(file.read(4), "little")
        self._y = int.from_bytes(file.read(4), "little")
        self._w = int.from_bytes(file.read(4), "little")
        self._h = int.from_bytes(file.read(4), "little")
