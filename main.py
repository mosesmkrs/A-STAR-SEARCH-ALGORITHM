import heapq
import math

# -------------------------------------------------
#                 A* SEARCH
# -------------------------------------------------
def a_star(start, goal, neighbors, heuristic):
    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, current)

        for neighbor, cost in neighbors(current):
            tentative_g = g_score[current] + cost

            if tentative_g < g_score.get(neighbor, math.inf):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal)

                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None


def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return list(reversed(path))


# -------------------------------------------------
#        GRID NEIGHBOR FUNCTION (8-direction)
# -------------------------------------------------
def grid_neighbors(grid):
    rows = len(grid)
    cols = len(grid[0])

    def inside(r, c):
        return 0 <= r < rows and 0 <= c < cols and grid[r][c] == 1

    directions = [
        (1, 0), (-1, 0), (0, 1), (0, -1),
        (1, 1), (1, -1), (-1, 1), (-1, -1)
    ]

    def get_neighbors(cell):
        r, c = cell
        result = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if inside(nr, nc):
                result.append(((nr, nc), 1))
        return result

    return get_neighbors


# -------------------------------------------------
#                HEURISTICS
# -------------------------------------------------
def euclidean(a, b):
    return math.dist(a, b)


# -------------------------------------------------
#         USER INPUT VALIDATION FUNCTIONS
# -------------------------------------------------
def get_coordinate(prompt, grid):
    rows = len(grid)
    cols = len(grid[0])

    while True:
        try:
            raw = input(prompt)
            r, c = map(int, raw.split())

            if not (0 <= r < rows and 0 <= c < cols):
                print("❌ Out of range. Try again.")
                continue

            if grid[r][c] == 0:
                print("❌ That cell is blocked. Try again.")
                continue

            return (r, c)

        except ValueError:
            print("❌ Invalid format. Enter two integers like: 2 3")


# -------------------------------------------------
#                     MAIN
# -------------------------------------------------
if __name__ == "__main__":
    grid = [
    [1,1,1,1,1,1,1,1,1],
    [1,0,0,1,1,1,0,0,1],
    [1,1,1,1,0,1,1,1,1],
    [1,0,1,0,1,0,1,0,1],
    [1,1,1,1,1,1,1,1,1],
    [1,0,1,0,1,0,1,0,1],
    [1,1,1,1,1,1,1,1,1],
    [1,0,0,1,1,1,0,0,1],
    [1,1,1,1,1,1,1,1,1],
]


    print("\n=== A* Search Pathfinding ===")
    print("Grid size:", len(grid), "x", len(grid[0]))
    print("Enter coordinates as: row col\n")

    start = get_coordinate("Enter START (row col): ", grid)
    goal = get_coordinate("Enter GOAL (row col): ", grid)

    neighbors_fn = grid_neighbors(grid)
    path = a_star(start, goal, neighbors_fn, euclidean)

    if path:
        print("\n✅ Path found:")
        print(" -> ".join(str(p) for p in path))
    else:
        print("\n❌ No path found.")
