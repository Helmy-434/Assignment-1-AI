import time


def get_neighbors(state):
    neighbors = []
    index = state.index('0')
    row, col = index // 3, index % 3

    moves = {
        "UP": (-1, 0),
        "DOWN": (1, 0),
        "LEFT": (0, -1),
        "RIGHT": (0, 1)
    }

    for move, (dr, dc) in moves.items():
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_state = list(state)
            target_index = new_row * 3 + new_col
            new_state[index], new_state[target_index] = new_state[target_index], new_state[index]
            neighbors.append([int(x) for x in new_state])

    return neighbors


def dfs(initial):
    start_time = time.time()

    # Convert string to list of ints
    if isinstance(initial, str):
        initial = [int(x) for x in initial]

    goal = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    # Stack stores tuples of: (current_state, parent_state, depth)
    stack = [(initial, None, 0)]
    visited = set()
    parent_map = {}
    nodes_expanded = 0
    max_depth = 0

    while stack:
        current, parent_tuple, depth = stack.pop()
        state_tuple = tuple(current)

        if state_tuple in visited:
            continue

        visited.add(state_tuple)
        parent_map[state_tuple] = parent_tuple
        nodes_expanded += 1
        max_depth = max(max_depth, depth)

        if current == goal:
            # Reconstruct the path backwards using the parent_map
            path = []
            curr = state_tuple
            while curr is not None:
                path.append(list(curr))
                curr = parent_map[curr]
            path.reverse()

            stats = {
                "nodes_expanded": nodes_expanded,
                "max_search_depth": max_depth,
                "running_time": time.time() - start_time
            }
            return path, stats

        for neighbor in get_neighbors([str(x) for x in current]):
            if tuple(neighbor) not in visited:
                stack.append((neighbor, state_tuple, depth + 1))

    return None, {"nodes_expanded": nodes_expanded, "max_search_depth": max_depth,
                  "running_time": time.time() - start_time}


def idfs(initial):
    start_time = time.time()

    # Convert string to list of ints
    if isinstance(initial, str):
        initial = [int(x) for x in initial]

    goal = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    nodes_expanded = 0
    max_depth = 0

    def dls(current, path, limit):
        """Depth Limited Search without a shared visited set across branches"""
        nonlocal nodes_expanded, max_depth

        if current == goal:
            return path

        if limit == 0:
            return 'cutoff'

        nodes_expanded += 1
        max_depth = max(max_depth, len(path) - 1)
        cutoff_occurred = False

        for neighbor in get_neighbors([str(x) for x in current]):
            # Cycle checking: only ensure we don't visit nodes already in the current path
            if neighbor not in path:
                result = dls(neighbor, path + [neighbor], limit - 1)
                if result == 'cutoff':
                    cutoff_occurred = True
                elif result is not None:
                    return result

        return 'cutoff' if cutoff_occurred else None

    # Iteratively increase depth limit (Max optimal moves in 8-puzzle is 31)
    for depth_limit in range(0, 50):
        result = dls(initial, [initial], depth_limit)
        if result != 'cutoff' and result is not None:
            stats = {
                "nodes_expanded": nodes_expanded,
                "max_search_depth": max_depth,
                "running_time": time.time() - start_time
            }
            return result, stats

    return None, {"nodes_expanded": nodes_expanded, "max_search_depth": max_depth,
                  "running_time": time.time() - start_time}