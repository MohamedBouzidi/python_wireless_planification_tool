from MultiCircle import *
from Serializable import *

class Zone(Form, Serializable):

    def __init__(self, canvas, x=150, y=150, r=50, ap=None, color="red"):
        Form.__init__(self, canvas, x, y, color)
        Serializable.__init__(self)
        self._radius = r
        self._start = 0
        self._extent = 359
        self._ap = ap
        self._circles = MultiCircle(self._canvas, self._x, self._y, self._radius, self._start, self._extent)
        self._obs = []

        #### DEBUG ####
        self._outer = {}
        #### END ####

    def draw(self):
        self._circles.draw()

    def move(self, x, y):
        self._circles.move(x,y)
        outer = self._outer.values()
        for o in outer:
            o.move(x,y)
        self._x = x
        self._y = y

    def raise_all(self):
        for i in self._obs:
            self._canvas.tag_raise(i)


    def delete(self):
        self._circles.delete()
        for o in self._outer:
            self._outer.get(o).delete()

    def remove(self, item):
        self._outer.get(item.get_index()).delete()

    def get_coor(self, x0, y, y0):
        return (math.sqrt(self._radius**2 - (y-y0)**2) - x0)

    def has_point(self, x, y):
        return self._circles.has_point(x,y)

    def has_point_obj(self, point):
        return self._circles.has_point(point.x, point.y)

    def get_dims(self):
        pass

    def get_id(self):
        self._circles.get_id()

    def set_radius(self, r):
        self._radius = r
        self._circles.set_radius(r)
        outer = self._outer.values()
        for o in outer:
            o.set_radius(r)

    def collision(self, item):
            dims = item.get_dims()
            x0 = dims[0]
            y0 = dims[1]
            x1 = dims[2]
            y1 = dims[3]

            R = self._radius
            center = Point(self._x, self._y)
            a = Point(x0,y0)
            b = Point(x1,y0)
            c = Point(x1,y1)
            d = Point(x0,y1)

            x = Point(0,0)
            y = Point(0,0)

            if ((self.has_point_obj(d) and self.has_point_obj(b)) and (((d.y < self._y) and (d.x > self._x)) or ((b.y > self._y) and (b.x < self._x)))):
                x.x, x.y = a.x, a.y
                y.x, y.y = c.x, c.y
            elif ((self.has_point_obj(c) and self.has_point_obj(a)) and (((c.y < self._y) and (c.x < self._x)) or ((a.y > self._y) and (a.x > self._x)))):
                x.x, x.y = b.x, b.y
                y.x, y.y = d.x, d.y
            elif ((self.has_point_obj(a) and self.has_point_obj(b)) and (a.x <= self._x) and (a.y >= self._y) and (b.x >= self._x) and (b.y >= self._y)):
                x.x, x.y = b.x, b.y
                y.x, y.y = a.x, a.y
            elif ((self.has_point_obj(b) and self.has_point_obj(c)) and (b.x <= self._x) and (b.y <= self._y) and (c.y >= self._y) and (c.x <= self._x)):
                x.x, x.y = b.x, b.y
                y.x, y.y = c.x, c.y
            elif ((self.has_point_obj(d) and self.has_point_obj(c)) and (d.x <= self._x) and (d.y <= self._y) and (c.y <= self._y) and (c.x >= self._x)):
                x.x, x.y = c.x, c.y
                y.x, y.y = d.x, d.y
            elif ((self.has_point_obj(a) and self.has_point_obj(d)) and (a.x >= self._x) and (a.y <= self._y) and (d.y >= self._y) and (d.x >= self._x)):
                x.x, x.y = a.x, a.y
                y.x, y.y = d.x, d.y

            d1 = center.distance(x)
            d2 = center.distance(y)

            if (d1 == 0):
                d1 = 0.1
            if (d2 == 0):
                d2 = 0.1

            d = (d1 + d2)/2

            o1 = math.acos((x.x - center.x)/d1)*(180/math.pi)
            o2 = math.acos((y.x - center.x)/d2)*(180/math.pi)

            if (a.y > center.y):
                o1 = 360 - o1
                o2 = 360 - o2
            elif ((a.y < center.y) and (c.y > center.y)):
                if (c.x < center.x):
                    o1 = 360 - o1
                elif (c.x > center.x):
                    o2 = 360 - o2

            start = o2
            extent = o1 - o2
             

            # Canvas Update Code
            if ((x.x != 0) and (x.y != 0) and (y.x != 0) and (y.y != 0)):
                o = self._outer.get(item.get_index())
                if (o == None):
                    self._outer[item.get_index()] = MultiCircle(self._canvas, self._x, self._y, self._radius, self._start, self._extent)
                    self._outer[item.get_index()].draw()
                    self._outer[item.get_index()].set_attenuation(item.get_attenuation(), d)
                    self._canvas.tag_raise(self._ap.get_id())
                    self._obs.append(item.get_id())
                    self.raise_all()
                else:
                    o.move(self._x, self._y)
                    o.set_start(start)
                    o.set_extent(extent)
                    self._outer[item.get_index()].set_attenuation(item.get_attenuation(), d)
            else:
                o = self._outer.get(item.get_index())
                if (o != None):
                    o.set_extent(0)

    def save(self):
        pass

    def load(self):
        pass
