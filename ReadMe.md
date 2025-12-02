A* (“A-star”) is a best-first search algorithm used in pathfinding and graph traversal.
It is one of the most widely used algorithms in:

video games (NPC navigation, enemies, tower defense)

robotics and autonomous movement

map routing applications (Google Maps–type navigation)

general AI search problems

A* finds a path from a start state to a goal state by combining:

the actual cost traveled so far, and

the estimated cost remaining to reach the goal

This balance makes A* both optimal (when using an admissible heuristic) and efficient (typically expanding fewer nodes than Dijkstra’s or BFS).

🎯 Goal of This Program

This project implements a clean and modular A* in Python.
The program allows the user to:

enter a start coordinate

enter a goal coordinate

run A* on a 9×9 grid

navigate around blocked (unwalkable) cells

view the printed shortest path if one exists

The implementation uses:

Euclidean distance as the heuristic

8-direction movement (up, down, left, right, and diagonals)
