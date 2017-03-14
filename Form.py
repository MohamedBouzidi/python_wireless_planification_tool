import tkinter as tk
from Point import *

class Form:
    def __init__(self, canvas, x, y, color):
        self._x = x
        self._y = y
        self._color = color
        self._canvas = canvas

    def draw(self):
        raise NotImplementedError("draw() should be implemented")

    def move(self, x, y):
        self._canvas.move(self._id, x - self._x, y - self._y)
        self._x = x
        self._y = y

    def has_point(self, x, y):
        raise NotImplementedError("has_point() should be implemented")

    def delete(self):
        self._canvas.delete(self.get_id())

    def rotate(self):
        pass

    def set_radius(self, r):
        pass

    def get_coords(self):
        return self._x, self._y

    def get_dims(self):
        raise NotImplementedError("get_dims() should be implemented")

    def get_id(self):
        return self._id