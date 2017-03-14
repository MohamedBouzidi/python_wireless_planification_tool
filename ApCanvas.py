from Ap import *
from Obstacle import *
from Station import *


class ApCanvas(tk.Canvas):

    SPAWN_X      = 580
    SPAWN_Y      = 250
    DATA_FILE    = "hello.plt"
    NO_SELECTION = -1

    def __init__(self, master, *args, **kwargs):
        tk.Canvas.__init__(self, master, *args, **kwargs)

        self._index = self.NO_SELECTION
        self._items = {}

        self._aps = {}
        self._obs = {}
        self._sts = {}
      
        self.bind("<B1-Motion>", self.move_item)
        self.bind("<Button-1>", self.select_item)
        self.bind("<Button-3>", self.rotate_item)

    ## This may change soon ######
    def get_items(self):
        return self._items.values()

    def get_aps(self):
        return self._aps

    def get_obs(self):
        return self._obs

    def get_sts(self):
        return self._sts
        
    ## End of temporary section ##

    def select_item(self, event):
        if (self._items):
            items = self._items.values()
            for item in items:
                if item.has_point(event.x, event.y):
                    self._index = item.get_index()

    def collision(self, item):
        if (isinstance(item, Obstacle)):
            items = self.get_aps().values()
            for i in items:
                i.collision(item)
        elif (isinstance(item, Ap)):
            items = self.get_obs().values()
            for i in items:
                item.collision(i)

    def connect(self, item):
        if (isinstance(item, Station)):
            aps = self.get_aps().values()
            for a in aps:
                item.check(a)
        elif (isinstance(item, Ap)):
            sts = self.get_sts().values()
            for s in sts:
                s.check(item)

    def update_zone(self, value):
        if (self._index != self.NO_SELECTION):
            item = self._items[self._index]
            item.set_radius(value)
            self.connect(item)
            self.collision(item)

    def update_material(self, value):
        if (self._index != self.NO_SELECTION):
            item = self._items[self._index]
            item.set_type(value)
            self.collision(item)

    def move_item(self, event):
        if self._items and (self._index != self.NO_SELECTION):
            item = self._items.get(self._index)
            item.move(event.x, event.y)
            self.connect(item)
            self.collision(item)

    def rotate_item(self, event):
        if self._items and (self._index != self.NO_SELECTION):
            self._items[self._index].rotate()

    def add_item(self, type):
        if type == CanvasItem.ACCESS:
            item = Ap(self, self.SPAWN_X, self.SPAWN_Y)
            self._aps[item.get_index()] = item
        elif type == CanvasItem.STATION:
            item = Station(self, self.SPAWN_X, self.SPAWN_Y)
            self._sts[item.get_index()] = item
        elif type == CanvasItem.OBSTACLE:
            item = Obstacle(self, self.SPAWN_X, self.SPAWN_Y)
            self._obs[item.get_index()] = item

        self._items[item.get_index()] = item
        self._index = item.get_index()
        item.draw()
        self.connect(item)

        ### DEBUG ###
        #print ("Aps: %d | Obs: %d | Sts: %d | Index: %d" % (len(self._aps), len(self._obs), len(self._sts), item.get_index()))
        #### END ####

    def remove_item(self):
        if self._items and (self._index != self.NO_SELECTION):
            item = self._items.pop(self._index, 0)
            self._index = self.NO_SELECTION
            if (isinstance(item, Ap)):
                self._aps.pop(item.get_index())
                stations = self._sts.values()
                for station in stations:
                    station.disconnect(item)
            elif (isinstance(item, Station)):
                self._sts.pop(item.get_index())
            elif (isinstance(item, Obstacle)):
                self._obs.pop(item.get_index())
                items = self.get_aps().values()
                for i in items:
                    i.remove(item)
            item.delete()

            ### DEBUG ###
            #print ("Aps: %d | Obs: %d | Sts: %d | Index: %d" % (len(self._aps), len(self._obs), len(self._sts), item.get_index()))
            #### END ####

    def save(self):
        file = open(self.DATA_FILE, "wb")
        count = len(self._items)
        index = self._index
        if index == self.NO_SELECTION:
            index = 31337
        file.write(count.to_bytes(4, "little"))
        file.write(index.to_bytes(4, "little"))
        items = self._items.values()
        for item in items:
            item.save(file)
        file.close()

    def load(self):
        file = open(self.DATA_FILE, "rb")
        count = int.from_bytes(file.read(4), "little")
        index = int.from_bytes(file.read(4), "little")
        for i in range(0,count):
            type = int.from_bytes(file.read(4), "little")
            if type == CanvasItem.OBSTACLE:
                item = Obstacle(self)
                self._obs[item.get_index] = item
            elif type == CanvasItem.ACCESS:
                item = Ap(self)
                self._aps[item.get_index] = item
            elif type == CanvasItem.STATION:
                item = Station(self)
                self._sts[item.get_index] = item
            item.load(file)
            self._items[item.get_index()] = item

        if index == 31337:
            index = self.NO_SELECTION
        self._index = index
        items = self._items.values()
        for item in items:
            item.draw()
        file.close()
