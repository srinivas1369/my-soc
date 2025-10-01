import sys
import random
import heapq
from collections import deque

def create_maze(rows, cols, seed):
    random.seed(seed)
    maze = [['.' for _ in range(cols)] for _ in range(rows)]
    
    start_row = random.randint(0, rows - 1)
    start_col = random.randint(0, cols - 1)
    end_row = random.randint(0, rows - 1)
    end_col = random.randint(0, cols - 1)

    while (start_row == end_row and start_col == end_col):
        end_row = random.randint(0, rows - 1)
        end_col = random.randint(0, cols - 1)

    maze[start_row][start_col] = 'S'
    maze[end_row][end_col] = 'E'

    for i in range(rows):
        for j in range(cols):
            if maze[i][j] not in ['S', 'E']:
                chance = random.random()
                if chance < 0.1:
                    maze[i][j] = 'T'  # trap
                elif chance < 0.2:
                    maze[i][j] = 'M'  # monster

    portals = {}
    number_of_portals = random.randint(0, 2)

    for _ in range(number_of_portals):
        while True:
            r1 = random.randint(0, rows - 1)
            c1 = random.randint(0, cols - 1)
            if maze[r1][c1] == '.':
                break

        while True:
            r2 = random.randint(0, rows - 1)
            c2 = random.randint(0, cols - 1)
            if maze[r2][c2] == '.' and (r2, c2) != (r1, c1):
                break

        maze[r1][c1] = 'P'
        maze[r2][c2] = 'P'
        portals[(r1, c1)] = (r2, c2)
        portals[(r2, c2)] = (r1, c1)

    return maze, (start_row, start_col), (end_row, end_col), portals

def dijkstra(maze, start, end, portals):
    rows = len(maze)
    cols = len(maze[0])
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    visited = set()
    heap = []
    heapq.heappush(heap, (0, 0, start))  # cost, monsters, position
    came_from = {}
    cost_to_reach = {}

    cost_to_reach[start] = 0

    while heap:
        cost, monsters, current = heapq.heappop(heap)
        if current in visited:
            continue
        visited.add(current)

        if current == end:
            return cost, monsters

        r, c = current
        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                cell = maze[nr][nc]
                if cell == '#':
                    continue
                extra_cost = 3 if cell == 'T' else 1
                monster_hit = 1 if cell == 'M' else 0
                new_cost = cost + extra_cost

                if (nr, nc) not in cost_to_reach or new_cost < cost_to_reach[(nr, nc)]:
                    cost_to_reach[(nr, nc)] = new_cost
                    came_from[(nr, nc)] = (r, c)
                    heapq.heappush(heap, (new_cost, monsters + monster_hit, (nr, nc)))

        if maze[r][c] == 'P' and (r, c) in portals:
            pr, pc = portals[(r, c)]
            if (pr, pc) not in visited:
                if (pr, pc) not in cost_to_reach or cost + 1 < cost_to_reach[(pr, pc)]:
                    cost_to_reach[(pr, pc)] = cost + 1
                    came_from[(pr, pc)] = (r, c)
                    heapq.heappush(heap, (cost + 1, monsters, (pr, pc)))

    return float('inf'), 0

def print_maze(maze):
    for row in maze:
        print("".join(row))
    print()

def main():
    lines = sys.stdin.read().splitlines()
    T = int(lines[0])
    index = 1
    total_cost = 0
    total_monsters = 0

    for test in range(T):
        row, col, seed = map(int, lines[index].split())
        index += 1
        maze, start, end, portals = create_maze(row, col, seed)
        
        print(f"Test Case {test + 1} Maze:")
        print_maze(maze)
        
        cost, monsters = dijkstra(maze, start, end, portals)
        if cost == float('inf'):
            print(f"Case {test + 1}: No path found\n")
        else:
            print(f"Case {test + 1}: Cost = {cost}, Monsters = {monsters}\n")
            total_cost += cost
            total_monsters += monsters

    if T > 0:
        print(f"Average Cost: {total_cost / T:.2f}, Average Monsters: {total_monsters / T:.2f}")

if __name__ == "__main__":
    main()

