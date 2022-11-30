import cProfile
import io
import pstats
import numpy as np


class ProfileDeco:
    def __init__(self, function):
        print("INIT")
        self.function = function
        self.pr = cProfile.Profile()

    def __call__(self, *args, **kwargs):
        print("CALL")
        self.pr.enable()
        result = self.function(*args, **kwargs)
        self.pr.disable()
        return result

    def print_stat(self):
        s = io.StringIO()
        sortby = "cumulative"
        ps = pstats.Stats(self.pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())


# the graph is represented as an adjacency matrix
@ProfileDeco
# equivalent to: dfs = ProfileDeco(dfs)
def dfs(graph: [list], v: int):
    visited = [False for _ in range(len(graph))]

    def process_top(v: int):
        visited[v] = True
        print(f"entered the top {v}")
        for top in range(len(graph[v])):
            if graph[v][top] == 1 and top != v and not visited[top]:
                process_top(top)
        print(f"left the top {v}")

    process_top(v)
    print(f"Visited {sum(visited)} tops")


if __name__ == "__main__":
    N = 400
    graph_matrix = [
        [np.random.choice([0, 1], p=[0.995, 0.005])
         for _ in range(N)] for _ in range(N)
    ]
    print(type(dfs))
    # ProfileDeco.__call__()
    dfs(graph_matrix, np.random.randint(0, N - 1))
    dfs.print_stat()
