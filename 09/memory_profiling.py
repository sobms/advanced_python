from memory_profiler import profile
from weakref_slots_comparing import *

@profile
def run():
    points_for_polygons_list = [[Point(*[random.randint(1, 1024)
                                         for _ in range(3)]) for _ in range(3)]
                                for _ in range(N)]
    object1 = [SimplePolygon(points_for_polygons_list[i]) for i in range(N)]
    object2 = [SlotsPolygon(points_for_polygons_list[i]) for i in range(N)]

    move_object(object1, [100, 100, 100])
    move_object(object2, [100, 100, 100])

    del object1
    del object2

    return None

if __name__ == '__main__':
    run()

