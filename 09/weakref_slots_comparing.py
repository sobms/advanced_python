import random
import time
#Polygon class
#покрасить полигон в какой то цвет
#применить какую то трансформацию, например сдвиг

N = 300_000

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class SimplePolygon:
    def __init__(self, points, color=None):
        self.points = points
        self.color = color

    def shift(self, shift_vector):
        for i in range(len(self.points)):
            self.points[i].x += shift_vector[0]
            self.points[i].y += shift_vector[1]
            self.points[i].z += shift_vector[2]

    def paint(self, color):
        self.color = color

class SlotsPolygon:
    __slots__ = ("points", "color")
    def __init__(self, points, color=None):
            self.points = points
            self.color = color

    def shift(self, shift_vector):
        for i in range(len(self.points)):
            self.points[i].x += shift_vector[0]
            self.points[i].y += shift_vector[1]
            self.points[i].z += shift_vector[2]

    def paint(self, color):
        self.color = color

def move_object(polygons, shift_vector):
    for poly in polygons:
        poly.shift(shift_vector)


if __name__ == '__main__':
    points_for_polygons_list = [[Point(*[random.randint(1, 1024) for _ in range(3)]) for _ in range(3)] for _ in range(N)]
    start_ts = time.time()
    object1 = [SimplePolygon(points_for_polygons_list[i]) for i in range(N)]
    end_ts = time.time()
    print(f"Creation time of {N} SimplePolygon instances is {end_ts - start_ts} seconds")
    start_ts = time.time()
    object2 = [SlotsPolygon(points_for_polygons_list[i]) for i in range(N)]
    end_ts = time.time()
    print(f"Creation time of {N} SlotsPolygon instances is {end_ts - start_ts} seconds")

    start_ts = time.time()
    move_object(object1, [100, 100, 100])
    end_ts = time.time()
    print(f"Time of changing of {N} SimplePolygon instances is {end_ts - start_ts} seconds")
    start_ts = time.time()
    move_object(object2, [100, 100, 100])
    end_ts = time.time()
    print(f"Time of changing of {N} SlotsPolygon instances is {end_ts - start_ts} seconds")

    start_ts = time.time()
    del object1
    end_ts = time.time()
    print(f"Time of deletion of {N} SimplePolygon instances is {end_ts - start_ts} seconds")
    start_ts = time.time()
    del object2
    end_ts = time.time()
    print(f"Time of deletion of {N} SlotsPolygon instances is {end_ts - start_ts} seconds")