import random
from memory_profiler import profile
from weakref_slots_comparing import (
    SimplePolygon,
    SlotsPolygon,
    PolygonWithWeakRefTexture,
    Point,
    SlotsPoint,
    move_object,
    N,
)


@profile
def run():
    object1 = [
        SimplePolygon(
            [Point(*[random.randint(1, 1024) for _ in range(3)])
             for _ in range(4)]
        )
        for i in range(N)
    ]
    object2 = [
        SlotsPolygon(
            [SlotsPoint(*[random.randint(1, 1024) for _ in range(3)])
             for _ in range(4)]
        )
        for i in range(N)
    ]
    object3 = [
        PolygonWithWeakRefTexture(
            [Point(*[random.randint(1, 1024) for _ in range(3)])
             for _ in range(4)]
        )
        for i in range(N)
    ]

    move_object(object1, [100, 100, 100])
    move_object(object2, [100, 100, 100])
    move_object(object3, [100, 100, 100])

    del object1
    del object2
    del object3


if __name__ == "__main__":
    run()
