from Serializable import *

class CanvasItem(Serializable):

    COUNT = 0
    DATAFILE = "data.plt"

    OBSTACLE     = 0
    STATION      = 1
    ACCESS       = 2

    def __init__(self):
        Serializable.__init__(self)
        self._index = self.COUNT
        CanvasItem.COUNT = CanvasItem.COUNT + 1

    def get_index(self):
        return self._index

    def collision(self, item):
        pass

    def set_type(self, type):
        pass

    def get_type(self):
        return None

    def save(self, file):
        pass

    def load(self, file):
        pass