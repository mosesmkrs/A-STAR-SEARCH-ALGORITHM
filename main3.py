import tkinter as tk
from tkinter import filedialog
import heapq, math, time, json

CELL = 35

# ============================================================
#                    A* SEARCH (Generator Mode)
# ============================================================
def astar_generator(start, goal, neighbors, heuristic):
    open_set = []
    heapq.heappush(open_set, (0, start))

    came = {}
    g = {start: 0}
    f = {start: heuristic(start, goal)}

    visited = set()

    while open_set:
        _, current = heapq.heappop(open_set)
        visited.add(current)

        yield ("expand", current, dict(g), dict(f), visited)

        if current == goal:
            path = []
            c = current
            while c in came:
                path.append(c)
                c = came[c]
            path.append(start)
            path.reverse()
            yield ("done", path, g, f, visited)
            return

        for neighbor, cost in neighbors(current):
            tentative = g[current] + cost

            if tentative < g.get(neighbor, math.inf):
                came[neighbor] = current
                g[neighbor] = tentative
                f[neighbor] = tentative + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f[neighbor], neighbor))

                yield ("update", neighbor, dict(g), dict(f), visited)

    yield ("fail", None, g, f, visited)


# ============================================================
def euclid(a, b):
    return math.dist(a, b)


def grid_neighbors(grid):
    R, C = len(grid), len(grid[0])

    def inside(r, c):
        return 0 <= r < R and 0 <= c < C and grid[r][c] == 1

    dirs = [
        (1,0),(-1,0),(0,1),(0,-1),
        (1,1),(1,-1),(-1,1),(-1,-1)
    ]

    def get(cell):
        r, c = cell
        out = []
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if inside(nr, nc):
                out.append(((nr, nc), 1))
        return out

    return get


# ============================================================
#                       GUI APPLICATION
# ============================================================
class AStarGUI:
    def __init__(self, root):
        self.root = root
        root.title("A* Pathfinding Visualizer – Advanced")

        self.rows = 15
        self.cols = 15

        self.start = None
        self.goal = None
        self.grid = [[1] * self.cols for _ in range(self.rows)]

        self.canvas = tk.Canvas(root, width=self.cols * CELL, height=self.rows * CELL)
        self.canvas.grid(row=0, column=0, columnspan=7)

        self.canvas.bind("<Button-1>", self.left_click)
        self.canvas.bind("<Button-3>", self.right_click)

        tk.Button(root, text="Run A*", command=self.run).grid(row=1, column=0)
        tk.Button(root, text="Step", command=self.step).grid(row=1, column=1)
        tk.Button(root, text="Reset", command=self.reset).grid(row=1, column=2)
        tk.Button(root, text="Save Map", command=self.save_map).grid(row=1, column=3)
        tk.Button(root, text="Load Map", command=self.load_map).grid(row=1, column=4)

        tk.Label(root, text="Speed:").grid(row=1, column=5)
        self.speed = tk.Scale(root, from_=1, to=200, orient="horizontal")
        self.speed.set(80)
        self.speed.grid(row=1, column=6)

        self.generator = None
        self.draw()

    # =====================================================
    def draw(self, g=None, f=None, visited=None, path=None):
        self.canvas.delete("all")
        for r in range(self.rows):
            for c in range(self.cols):
                x1, y1 = c * CELL, r * CELL
                x2, y2 = x1 + CELL, y1 + CELL

                val = self.grid[r][c]

                if val == 0:
                    fill = "black"
                else:
                    fill = "white"

                if visited and (r, c) in visited:
                    fill = "#bde0fe"

                if g and (r, c) in g:
                    shade = max(0, 255 - min(200, int(g[(r, c)] * 5)))
                    fill = f"#{shade:02x}{255:02x}{shade:02x}"

                if path and (r, c) in path:
                    fill = "red"

                if self.start == (r, c):
                    fill = "blue"
                if self.goal == (r, c):
                    fill = "red"

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="gray")

    # =====================================================
    def left_click(self, e):
        c = e.x // CELL
        r = e.y // CELL

        if self.start is None:
            self.start = (r, c)
        elif self.goal is None:
            self.goal = (r, c)
        else:
            self.start = (r, c)
            self.goal = None

        self.draw()

    # =====================================================
    def right_click(self, e):
        c = e.x // CELL
        r = e.y // CELL
        if (r, c) == self.start or (r, c) == self.goal:
            return
        self.grid[r][c] = 1 - self.grid[r][c]
        self.draw()

    # =====================================================
    def run(self):
        if not self.start or not self.goal:
            print("Pick start & goal")
            return

        neigh = grid_neighbors(self.grid)
        self.generator = astar_generator(self.start, self.goal, neigh, euclid)
        self.animate()

    def animate(self):
        try:
            event, data, g, f, visited = next(self.generator)

            if event in ("expand", "update"):
                self.draw(g, f, visited)
            elif event == "done":
                self.draw(g, f, visited, path=data)
                return
            elif event == "fail":
                self.draw()
                print("No path.")
                return

            delay = int(500 / self.speed.get())
            self.root.after(delay, self.animate)

        except StopIteration:
            return

    # =====================================================
    def step(self):
        if self.generator is None:
            self.run()
            return

        try:
            event, data, g, f, visited = next(self.generator)
            if event == "done":
                self.draw(g, f, visited, path=data)
            else:
                self.draw(g, f, visited)

        except StopIteration:
            return

    # =====================================================
    def reset(self):
        self.generator = None
        self.start = None
        self.goal = None
        self.grid = [[1] * self.cols for _ in range(self.rows)]
        self.draw()

    # =====================================================
    def save_map(self):
        path = filedialog.asksaveasfilename(defaultextension=".json")
        if not path:
            return
        data = {
            "rows": self.rows,
            "cols": self.cols,
            "grid": self.grid
        }
        with open(path, "w") as f:
            json.dump(data, f)

    def load_map(self):
        path = filedialog.askopenfilename()
        if not path:
            return
        with open(path) as f:
            data = json.load(f)
        self.rows = data["rows"]
        self.cols = data["cols"]
        self.grid = data["grid"]

        self.canvas.config(width=self.cols * CELL, height=self.rows * CELL)
        self.draw()


# ============================================================
root = tk.Tk()
AStarGUI(root)
root.mainloop()
