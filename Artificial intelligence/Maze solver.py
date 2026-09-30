from collections import deque

maze = [
    ['S', '.', '.', '#', '.', '.'],
    ['#', '#', '.', '#', '.', '#'],
    ['.', '.', '.', '.', '.', '.'],
    ['.', '#', '#', '#', '#', '.'],
    ['.', '.', '.', '.', '#', '.'],
    ['#', '#', '.', 'G', '.', '.']
]

ROWS = len(maze)
COLS = len(maze[0])



def find_position(symbol):
    for i in range(ROWS):
        for j in range(COLS):
            if maze[i][j] == symbol:
                return (i, j)

      
start = find_position('S')
goal = find_position('G')

def get_neighbors(position):
    row,col = position
    directions=[
        (-1, 0),  
        (1, 0),   
        (0, -1), 
        (0, 1)   
     ]
    neighbors=[]
    for dr,dc in directions:
        new_row = row + dr
        new_col = col + dc
        if 0 <= new_row < ROWS and 0 <= new_col < COLS:
            if maze[new_row][new_col] != '#':
                neighbors.append((new_row, new_col))
    return neighbors
  

     







def reconstruct_path(parent, goal):

    path = []

    current = goal

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()

    return path


def bfs(start, goal):

    queue = deque([start])

    visited = set([start])

    parent = {start: None}

    nodes_expanded = 0

    max_memory = 1

    while queue:

        max_memory = max(max_memory, len(queue))

        current = queue.popleft()

        nodes_expanded += 1

        if current == goal:
            path = reconstruct_path(parent, goal)
            return path, nodes_expanded, max_memory

        for neighbor in get_neighbors(current):

            if neighbor not in visited:

                visited.add(neighbor)

                parent[neighbor] = current

                queue.append(neighbor)

    return None, nodes_expanded, max_memory


def dfs(start, goal):

    stack = [start]

    visited = set([start])

    parent = {start: None}

    nodes_expanded = 0

    max_memory = 1

    while stack:

        max_memory = max(max_memory, len(stack))

        current = stack.pop()

        nodes_expanded += 1

        if current == goal:
            path = reconstruct_path(parent, goal)
            return path, nodes_expanded, max_memory

        for neighbor in reversed(get_neighbors(current)):

            if neighbor not in visited:

                visited.add(neighbor)

                parent[neighbor] = current

                stack.append(neighbor)

    return None, nodes_expanded, max_memory



def depth_limited_search(current, goal, limit, visited, parent, stats):

    stats["expanded"] += 1

    if current == goal:
        return True

    if limit == 0:
        return False

    for neighbor in get_neighbors(current):

        if neighbor not in visited:

            visited.add(neighbor)

            parent[neighbor] = current

            stats["memory"] = max(stats["memory"], len(visited))

            found = depth_limited_search(
                neighbor,
                goal,
                limit - 1,
                visited,
                parent,
                stats
            )

            if found:
                return True

    return False



def ids(start, goal):

    depth = 0

    while True:

        visited = set([start])

        parent = {start: None}

        stats = {
            "expanded": 0,
            "memory": 1
        }

        found = depth_limited_search(
            start,
            goal,
            depth,
            visited,
            parent,
            stats
        )

        if found:

            path = reconstruct_path(parent, goal)

            return path, stats["expanded"], stats["memory"]

        depth += 1



# _______________________print maze
def print_maze():

    print("Maze:\n")

    for row in maze:
        print(" ".join(row))

    print()


# _______________________print path

def show_path(path):

    display = [row[:] for row in maze]

    for r, c in path:

        if display[r][c] == '.':
            display[r][c] = '*'

    print()

    for row in display:
        print(" ".join(row))

    print()

# _______________________starting of main funcition

print("=" * 50)
print("Maze Solving using Uninformed Search")
print("=" * 50)

print_maze()


# _______________________bfs

bfs_path, bfs_nodes, bfs_memory = bfs(start, goal)

print("BFS Result")
print("--------------------")
print("Path :", bfs_path)
print("Path Length :", len(bfs_path))
print("Nodes Expanded :", bfs_nodes)
print("Memory Used :", bfs_memory)

show_path(bfs_path)


# _______________________dfs

dfs_path, dfs_nodes, dfs_memory = dfs(start, goal)

print("DFS Result")
print("--------------------")
print("Path :", dfs_path)
print("Path Length :", len(dfs_path))
print("Nodes Expanded :", dfs_nodes)
print("Memory Used :", dfs_memory)

show_path(dfs_path)


# _______________________ids

ids_path, ids_nodes, ids_memory = ids(start, goal)

print("IDS Result")
print("--------------------")
print("Path :", ids_path)
print("Path Length :", len(ids_path))
print("Nodes Expanded :", ids_nodes)
print("Memory Used :", ids_memory)

show_path(ids_path)


# _______________________comparison table

print("=" * 60)
print("Comparison")
print("=" * 60)

print("{:<10} {:<15} {:<20} {:<15}".format(
    "Method",
    "Path Length",
    "Nodes Expanded",
    "Memory Used"
))

print("-" * 60)

print("{:<10} {:<15} {:<20} {:<15}".format(
    "BFS",
    len(bfs_path),
    bfs_nodes,
    bfs_memory
))

print("{:<10} {:<15} {:<20} {:<15}".format(
    "DFS",
    len(dfs_path),
    dfs_nodes,
    dfs_memory
))

print("{:<10} {:<15} {:<20} {:<15}".format(
    "IDS",
    len(ids_path),
    ids_nodes,
    ids_memory
))