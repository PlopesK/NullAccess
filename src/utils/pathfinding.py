from collections import deque

def bfs(start, goal, grid):
    rows = len(grid)
    cols = len(grid[0])

    queue = deque([start])
    came_from = {start: None}

    while queue:
        current = queue.popleft()

        if current == goal:
            break

        x, y = current

        neighbors = [
            (x+1, y),
            (x-1, y),
            (x, y+1),
            (x, y-1)
        ]

        for nx, ny in neighbors:
            if 0 <= nx < cols and 0 <= ny < rows:
                if grid[ny][nx] == 0 and (nx, ny) not in came_from:
                    queue.append((nx, ny))
                    came_from[(nx, ny)] = current

    # reconstrói caminho
    path = []
    cur = goal

    while cur is not None:
        path.append(cur)
        cur = came_from.get(cur)

    path.reverse()

    return path if path and path[0] == start else []