GOAL_STATE = "012345678"
def states(current_state):

    pos = current_state.index('0')
    moves = []
    directions = [(-3, 'up'), (3, 'down'), (-1, 'left'), (1, 'right')]

    for move, _ in directions:
        new_pos = pos + move
        if 0 <= new_pos < 9:
            if (pos % 3 == 0 and move == -1) or (pos % 3 == 2 and move == 1): # if illegal move ie at inde 3 and wants to go left
                continue
            lst = list(current_state)
            lst[pos], lst[new_pos] = lst[new_pos], lst[pos]
            moves.append(''.join(lst))
    return moves