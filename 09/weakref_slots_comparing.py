import random
import time
import weakref
import numpy as np



N = 100_000


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class SlotsPoint:
    __slots__ = ("x", "y", "z")

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class SimplePolygon:
    def __init__(self, points: [Point], color=None):
        self.points = points
        self.color = color
        self.texture = Texture(self, (256, 128))

    def shift(self, shift_vector):
        for i in range(len(self.points)):
            self.points[i].x += shift_vector[0]
            self.points[i].y += shift_vector[1]
            self.points[i].z += shift_vector[2]

    def paint(self, color):
        self.color = color


class SlotsPolygon:
    __slots__ = ("points", "color", "texture")

    def __init__(self, points: [SlotsPoint], color=None):
        self.points = points
        self.color = color
        self.texture = Texture(self, (256, 128))

    def shift(self, shift_vector):
        for i in range(len(self.points)):
            self.points[i].x += shift_vector[0]
            self.points[i].y += shift_vector[1]
            self.points[i].z += shift_vector[2]

    def paint(self, color):
        self.color = color


class PolygonWithWeakRefTexture:
    def __init__(self, points: [Point], color=None):
        self.points = points
        self.color = color
        self.texture = TextureWithWeakRef(self, (256, 128))

    def shift(self, shift_vector):
        for i in range(len(self.points)):
            self.points[i].x += shift_vector[0]
            self.points[i].y += shift_vector[1]
            self.points[i].z += shift_vector[2]

    def paint(self, color):
        self.color = color


class Texture:  # HeightMap
    def __init__(self, polygon, shape):
        self.shape = shape
        self.height_map = np.empty(self.shape)
        self.polygon = polygon


class TextureWithWeakRef:
    def __init__(self, polygon, shape):
        self.shape = shape
        self.height_map = np.empty(self.shape)
        self.polygon = weakref.ref(polygon)


def move_object(polygons, shift_vector):
    for poly in polygons:
        poly.shift(shift_vector)


if __name__ == "__main__":
    start_ts = time.time()
    object1 = [
        SimplePolygon(
            [Point(*[random.randint(1, 1024) for _ in range(3)])
             for _ in range(4)]
        )
        for i in range(N)
    ]
    end_ts = time.time()
    print(
        f"Creation time of {N} SimplePolygon instances is"
        f" {end_ts - start_ts} seconds"
    )
    start_ts = time.time()
    object2 = [
        SlotsPolygon(
            [SlotsPoint(*[random.randint(1, 1024) for _ in range(3)])
             for _ in range(4)]
        )
        for i in range(N)
    ]
    end_ts = time.time()
    print(f"Creation time of {N} SlotsPolygon instances is"
          f" {end_ts - start_ts} seconds")
    start_ts = time.time()
    object3 = [
        PolygonWithWeakRefTexture(
            [Point(*[random.randint(1, 1024) for _ in range(3)])
             for _ in range(4)]
        )
        for i in range(N)
    ]
    end_ts = time.time()
    print(
        f"Creation time of {N} PolygonWithWeakRefTexture instances is"
        f" {end_ts - start_ts} seconds"
    )

    start_ts = time.time()
    move_object(object1, [100, 100, 100])
    end_ts = time.time()
    print(
        f"Time of changing of {N} SimplePolygon instances is"
        f" {end_ts - start_ts} seconds"
    )
    start_ts = time.time()
    move_object(object2, [100, 100, 100])
    end_ts = time.time()
    print(
        f"Time of changing of {N} SlotsPolygon instances is"
        f" {end_ts - start_ts} seconds"
    )
    start_ts = time.time()
    move_object(object3, [100, 100, 100])
    end_ts = time.time()
    print(
        f"Time of changing of {N} PolygonWithWeakRefTexture instances is"
        f" {end_ts - start_ts} seconds"
    )

    start_ts = time.time()
    del object1
    end_ts = time.time()
    print(
        f"Time of deletion of {N} SimplePolygon instances is"
        f" {end_ts - start_ts} seconds"
    )
    start_ts = time.time()
    del object2
    end_ts = time.time()
    print(
        f"Time of deletion of {N} SlotsPolygon instances is"
        f" {end_ts - start_ts} seconds"
    )
    start_ts = time.time()
    del object3
    end_ts = time.time()
    print(
        f"Time of deletion of {N} PolygonWithWeakRefTexture instances is"
        f" {end_ts - start_ts} seconds"
    )
