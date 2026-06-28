def matrix_to_string(matrix):
    return "".join("".join(str(value) for value in row) for row in matrix)

def possible_moves(matrix, x, y):
    moves = []
    if matrix[x][y] == 1:
        moves.append("SUCK")
    if x > 0:   moves.append("UP")
    if x < 2:   moves.append("DOWN")
    if y > 0:   moves.append("LEFT")
    if y < 2:   moves.append("RIGHT")
    return moves

def act(matrix, action, x, y):
    matrix_copy = [row[:] for row in matrix]
    i, j = x, y
    if action == "UP":     i -= 1
    elif action == "DOWN":  i += 1
    elif action == "LEFT":  j -= 1
    elif action == "RIGHT": j += 1
    elif action == "SUCK":  matrix_copy[i][j] = 0
    return matrix_copy, i, j

def heuristic(matrix):
    return sum(row.count(1) for row in matrix)

def get_value(matrix, x, y):
    dirt_positions = []
    for r in range(len(matrix)):
        for c in range(len(matrix[0])):
            if matrix[r][c] == 1:
                dirt_positions.append((r, c))
    if not dirt_positions:
        return 900
    nearest = min(abs(x - r) + abs(y - c) for r, c in dirt_positions)
    dirt_count = len(dirt_positions)
    return 100 * (9 - dirt_count) - nearest

def heuristic_beam(matrix, x, y):
    return -get_value(matrix, x, y)

def is_vacuum_goal(matrix):
    return sum(sum(row) for row in matrix) == 0

def apply_vacuum_action_advanced(matrix, action, x, y):
    matrix_copy = [row[:] for row in matrix]
    nx, ny = x, y
    if action == "UP":
        if x > 0: nx -= 1
        else: return None, x, y
    elif action == "DOWN":
        if x < 2: nx += 1
        else: return None, x, y
    elif action == "LEFT":
        if y > 0: ny -= 1
        else: return None, x, y
    elif action == "RIGHT":
        if y < 2: ny += 1
        else: return None, x, y
    elif action == "SUCK":
        if matrix_copy[x][y] == 1: matrix_copy[x][y] = 0
        else: return None, x, y 
    return matrix_copy, nx, ny
