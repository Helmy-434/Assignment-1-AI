import heapq
import math
import time


class State:
    def __init__(self, tiles, g=0, h=0, parent=None,depth=0):
        self.tiles = tiles
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = parent
        self.depth = depth

    def __lt__(self, other):
        return self.f < other.f #for heap comparison

def get_children(parent_state, min_heap, heuristic,goal):
    index = parent_state.tiles.index(0)
    size = 3
    row, col = index // size, index % size

    #Define possible moves
    moves = {
        "UP": (-1, 0),
        "DOWN": (1, 0),
        "LEFT": (0, -1),
        "RIGHT": (0, 1)
    }

    for move, (dr, dc) in moves.items():
        new_row, new_col = row + dr, col + dc

        #Check boundaries
        if 0 <= new_row < size and 0 <= new_col < size:
            new_tiles = list(parent_state.tiles)# Create a copy of the state to modify
            target_index = new_row * size + new_col
            new_tiles[index], new_tiles[target_index] = new_tiles[target_index], new_tiles[index]
            if heuristic == 0:
                h  = get_manhattan_distance(new_tiles,goal)
            else:
                h = get_euclidean_distance(new_tiles,goal)

            new_state = State(new_tiles, g=parent_state.g +1, h=h, parent=parent_state,depth=parent_state.depth + 1)
            heapq.heappush(min_heap, new_state)



def get_manhattan_distance(current_state,goal):
    distance = 0
    size = 3

    for i in range(len(current_state)):
        tile = current_state[i]

        # Current position
        current_row, current_col = i // size, i % size

        # Goal position
        goal_index = goal.index(tile)
        goal_row, goal_col = goal_index // size, goal_index % size

        distance += abs( goal_row - current_row)  + abs(goal_col - current_col)

    return distance


def get_euclidean_distance(current_state,goal):
    distance = 0
    size = 3

    for i in range(len(current_state)):
        tile = current_state[i]

        # Current position
        current_row, current_col = i // size, i % size

        # Goal position
        goal_index = goal.index(tile)
        goal_row, goal_col = goal_index // size, goal_index % size

        distance += math.sqrt((goal_row - current_row) ** 2 + (goal_col - current_col) ** 2)

    return distance



def A_star(initial_tiles,goal,heuristic=0):
    start_time = time.time()
    heap = []
    visited = set()
    nodes_expanded = 0
    max_search_depth = 0
    initial_state = State(tiles=initial_tiles)
    heapq.heappush(heap,initial_state)
    while heap:
        current_node = heapq.heappop(heap)
        nodes_expanded += 1
        max_search_depth = max(max_search_depth, current_node.depth)
        if current_node.tiles == goal:
            running_time = time.time() - start_time
            return current_node, {"nodes_expanded": nodes_expanded, "max_search_depth": max_search_depth, "running_time": running_time}

        state = tuple(current_node.tiles) #to be able to compare it in visited list
        if state in visited:
            continue

        visited.add(state)
        get_children(current_node,heap,heuristic,goal)

    return None, {"nodes_expanded": nodes_expanded, "max_search_depth": max_search_depth, "running_time": running_time}

def print_solution(final_node):
    path = []
    current = final_node
    while current is not None:
        path.append(current.tiles)
        current = current.parent
    path.reverse()  # Start -> Goal
    return path
    # for step, node in enumerate(path):
    #     print(f"Step {step}:")
    #     board = node.tiles
    #     for i in range(0, 9, 3):
    #         row = board[i: i + 3]
    #         # Join numbers with spaces, then wrap in brackets
    #         formatted_row = " ".join(str(tile) for tile in row)
    #         print(f"[  {formatted_row}  ]")
    #     print("-" * 15)

    # print("--- SEARCH REPORT ---")
    # print(f"Cost of Path (g): {final_node.g}")
    # print(f"Nodes Expanded: {nodes_expanded}")
    # print(f"Search Depth: {max_depth}")
    # print(f"Running Time: {running_time:.4f} seconds")
    # print("-" * 21)


def A_star_main(initial,heuristic):
    goal = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    #initial = [1, 4, 2, 3, 0, 5, 6, 7, 8]
    if isinstance(initial, str):
        initial = [int(x) for x in initial]
    else:
        initial = [int(x) for x in initial]
    final, stats = A_star(initial,goal,heuristic)
    if final:
        path = print_solution(final)
        return path , stats
    else:
        return None
