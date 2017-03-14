from CanvasItem import *
from Form import *

IMAGESIZE = 47

class Station(Form, CanvasItem):

    NO_SELECTION = -1

    def __init__(self, canvas, x=150, y=150, color="red"):
        Form.__init__(self, canvas, x, y, color)
        CanvasItem.__init__(self)
        self._image = tk.PhotoImage(file="assets/station.png")
        self._center = Point(self._x, self._y)
        self._connected = False
        self._current_index = self.NO_SELECTION
        self._current_pos = Point(self._x, self._y)
        self._current_distance = 0
        self._current_power = 0
        self._line = None

    def draw(self):
        self._id = self._canvas.create_image(self._x, self._y, image=self._image)
        self._line = self._canvas.create_line(self._x, self._y, self._current_pos.x, self._current_pos.y, fill="black", width=4)

    def delete(self):
        self._canvas.delete(self.get_id())
        self._canvas.delete(self._line)

    def disconnect(self, ap):
        if (ap.get_index() == self._current_index):
            self._connected = False
            self._current_index = self.NO_SELECTION
            self._current_distance = 0
            self._current_power = 0
            self._canvas.coords(self._line, self._center.x, self._center.y, self._center.x, self._center.y)

    def check(self, ap):
        pos = ap.get_coords()
        distance = self._center.distance(pos)
        power = ap.get_radius()
        index = ap.get_index()
        #print ("Distance: %d | Power: %d | Connected: %s" % (distance, power, self._connected))
        if (self._connected == False):
            self._canvas.coords(self._line, self._center.x, self._center.y, self._center.x, self._center.y)
        if (distance < power):
            if (self._connected):
                if ((distance < self._current_distance) or ((distance >= self._current_distance) and (power > self._current_power))):
                    self._current_distance = distance
                    self._current_power = power
                    self._current_index = index
                    self._current_pos.x, self._current_pos.y = pos.x, pos.y
                    self._canvas.coords(self._line, self._center.x, self._center.y, self._current_pos.x, self._current_pos.y)
                elif (self._current_index == index):
                    self._connected = False
            else:
                self._current_distance = distance
                self._current_power = power
                self._current_index = index
                self._current_pos.x, self._current_pos.y = pos.x, pos.y
                self._canvas.coords(self._line, self._center.x, self._center.y, self._current_pos.x, self._current_pos.y)
                self._connected = True
        elif (self._connected == False):
            self._canvas.coords(self._line, self._center.x, self._center.y, self._center.x, self._center.y)

    def move(self, x, y):
        self._canvas.move(self._id, x - self._x, y - self._y)
        if (self._connected == False):
            self._current_pos.x, self._current_pos.y = x, y
        self._canvas.coords(self._line, x, y, self._current_pos.x, self._current_pos.y)
        self._center.x = self._x = x
        self._center.y = self._y = y

    def has_point(self, x, y):
        if ((x >= self._x - IMAGESIZE/2) and (x <= self._x + IMAGESIZE/2)):
            if ((y >= self._y - IMAGESIZE/2) and (y <= self._y + IMAGESIZE/2)):
               return True
        return False

    # Serialization code:
    def save(self, file):
        file.write(CanvasItem.STATION.to_bytes(4, "little"))
        file.write(self._x.to_bytes(4, "little"))
        file.write(self._y.to_bytes(4, "little"))

    def load(self, file):
        self._x = int.from_bytes(file.read(4), "little")
        self._y = int.from_bytes(file.read(4), "little")
