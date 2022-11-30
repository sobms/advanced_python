import cProfile
import pstats
import io
import random
from weakref_slots_comparing import (
    move_object,
    SlotsPolygon,
    SimplePolygon,
    PolygonWithWeakRefTexture,
    Point,
    SlotsPoint,
    N,
)


if __name__ == "__main__":
    object1 = [
        SimplePolygon(
            [Point(*[random.randint(1, 1024) for _ in range(3)])
             for _ in range(3)]
        )
        for i in range(N)
    ]
    object2 = [
        SlotsPolygon(
            [SlotsPoint(*[random.randint(1, 1024) for _ in range(3)])
             for _ in range(3)]
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

    pr = cProfile.Profile()
    pr.enable()
    move_object(object1, [100, 100, 100])
    move_object(object2, [100, 100, 100])
    move_object(object3, [100, 100, 100])
    pr.disable()

    s = io.StringIO()
    SORTBY = "cumulative"
    ps = pstats.Stats(pr, stream=s).sort_stats(SORTBY)
    ps.print_stats()

    print(s.getvalue())
