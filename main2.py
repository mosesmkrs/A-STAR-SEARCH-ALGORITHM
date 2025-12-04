import tkinter as tk
import heapq
import math

# ===================================================================
#                            A* SEARCH
# ===================================================================
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
            tentative = g_score[current] + cost

            if tentative < g_score.get(neighbor, math.inf):
                came_from[neighbor] = current
                g_score[neighbor] = tentative
                f_score[neighbor] = tentative + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    return None


def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return list(reversed(path))


# ===================================================================
#                        GRID NEIGHBORS
# ===================================================================
def grid_neighbors(grid):
    rows, cols = len(grid), len(grid[0])

    def inside(r, c):
        return 0 <= r < rows and 0 <= c < cols and grid[r][c] == 1

    directions = [
        (1,0), (-1,0), (0,1), (0,-1),
        (1,1), (1,-1), (-1,1), (-1,-1)
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


def euclidean(a, b):
    return math.dist(a, b)


# ===================================================================
#                       TKINTER GUI APP
# ===================================================================
CELL_SIZE = 40

class PathfindingGUI:
    def __init__(self, root, grid):
        self.root = root
        self.grid = grid
        
        self.rows = len(grid)
        self.cols = len(grid[0])

        self.start = None
        self.goal = None

        self.canvas = tk.Canvas(
            root, width=self.cols * CELL_SIZE, height=self.rows * CELL_SIZE
        )
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.on_click)

        self.button = tk.Button(root, text="Run A*", command=self.run_astar)
        self.button.pack(pady=10)

        self.draw_grid()

    # -----------------------------------------------------------
    def draw_grid(self, path=None):
        self.canvas.delete("all")

        for r in range(self.rows):
            for c in range(self.cols):

                x1 = c * CELL_SIZE
                y1 = r * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                cell = self.grid[r][c]

                # default colors
                fill = "white" if cell == 1 else "black"

                # path highlight
                if path and (r, c) in path:
                    fill = "lightgreen"

                # start and goal markers
                if self.start == (r, c):
                    fill = "blue"
                if self.goal == (r, c):
                    fill = "red"

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="gray")

    # -----------------------------------------------------------
    def on_click(self, event):
        c = event.x // CELL_SIZE
        r = event.y // CELL_SIZE

        if self.grid[r][c] == 0:
            return  # cannot select blocked cell

        # If start not set → set start
        if self.start is None:
            self.start = (r, c)
        # If goal not set → set goal
        elif self.goal is None:
            self.goal = (r, c)
        # Reset both if both already set (for reselecting)
        else:
            self.start = (r, c)
            self.goal = None

        self.draw_grid()

    # -----------------------------------------------------------
    def run_astar(self):
        if self.start is None or self.goal is None:
            print("Choose START and GOAL first.")
            return

        neighbors = grid_neighbors(self.grid)
        path = a_star(self.start, self.goal, neighbors, euclidean)

        if path:
            self.draw_grid(path=path)
        else:
            print("No path found.")


# ===================================================================
#                           MAIN APP
# ===================================================================
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

root = tk.Tk()
root.title("A* Pathfinding Visualizer (Basic Tkinter)")

app = PathfindingGUI(root, grid)

root.mainloop()
