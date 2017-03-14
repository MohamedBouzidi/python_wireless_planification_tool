from Circle import *

class MultiCircle(Form):

    #COLORS = ["#1100ff", "#3300ff", "#4400ff", "#5500dd", "#7700dd", "#aa00dd", "#bb00dd", "#cc00dd", "#dd00cc", "#ee00ff",
    #          "#ff00ee", "#ff00dd", "#ff00cc", "#ff00bb", "#ff00aa", "#ff0077", "#ff0055", "#ff0044", "#ff0033", "#ff0011"]
    #COLORS = ["#1111ff", "#1133ee", "#1155dd", "#1177cc", "#11aabb", "#11aaaa", "#11aacc", "#11aabb", "#11aaaa",
    #          "#11aa77", "#339955", "#557733", "#775511", "#aa3311", "#bb3311", "#bb1111", "#cc1111", "#dd1111", "#ee1111", "#ff1111"]
    COLORS = ["#1111ff", "#1133ff", "#1155ff", "#1155ee", "#1177ee", "#1177dd", "#11aadd", "#11aacc", "#11bbcc", "#11bbbb", "#11ccbb",
              "#11cccc", "#11ddcc", "#11ddbb", "#11eebb", "#11eeaa", "#11ffaa", "#11ff77", "#11ff55", "#11ff33", "#11ff11", "#33ff11",
              "#55ff11", "#55ee11", "#77ee11", "#77dd11", "#aadd11", "#bbdd11", "#bbcc11", "#cccc11", "#ccbb11", "#ddbb11", "#ddaa11",
              "#eeaa11", "#ee7711", "#ff5511", "#ff3311", "#ff1111"]
    RESOLUTION = len(COLORS)

    def __init__(self, canvas, x, y, r, s, e):
        Form.__init__(canvas, x, y, r, "red")
        self._circles = []
        self._prev_radius = []
        self._radius = r
        outline = r
        for i in range(0, self.RESOLUTION):
            c = Circle(canvas, x, y, outline, self.COLORS[i], s, e)
            self._circles.append(c)
            self._prev_radius.append(outline)
            outline = outline - 2*(self._radius / self.RESOLUTION)
            if outline < 0:
                outline = 10

    def draw(self):
        for i in self._circles:
            i.draw()

    def move(self, x, y):
        for i in self._circles:
            i.move(x,y)

    def delete(self):
        for i in self._circles:
            i.delete()

    def has_point(self, x, y):
        return self._circles[0].has_point(x,y)

    def get_id(self):
        return self._circles[0].get_id()

    def set_radius(self, r):
        outline = r
        for i in range(0, self.RESOLUTION):
            self._circles[i].set_radius(outline)
            self._prev_radius[i] = outline
            outline = outline - 2*(self._radius / self.RESOLUTION)
            if outline < 0:
                outline = 10

    def set_attenuation(self, v, d):
        index = int(v/10)
        if (index >= self.RESOLUTION):
            index = self.RESOLUTION - 1
        for i in range(index, self.RESOLUTION):
            if (self._prev_radius[i] > d):
                self._circles[i].set_radius(d)
            else:
                self._circles[i].set_radius(self._prev_radius[i])

    def set_start(self, s):
        for c in self._circles:
            c.set_start(s)

    def set_extent(self, e):
        for c in self._circles:
            c.set_extent(e)
