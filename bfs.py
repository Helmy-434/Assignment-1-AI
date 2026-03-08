from collections import deque
import time
from helpers import *

def bfs(start):
    start_time = time.time() 
    frontier = deque([[start]])  
    visited = {start}  
    nodes_expanded = 0
    max_depth = 0

    while frontier:
        path = frontier.popleft()
        node = path[-1]
        
        max_depth = max(max_depth, len(path))

        if node == GOAL_STATE:
            end_time = time.time()
            return path, {
                'cost': len(path) - 1,
                'nodes_expanded': nodes_expanded,
                'search_depth': len(path) - 1,
                'running_time': end_time - start_time
            }

        nodes_expanded += 1
        for neighbor in states(node):
            if neighbor not in visited:
                frontier.append(path + [neighbor])
                visited.add(neighbor)
    
    return None, {}