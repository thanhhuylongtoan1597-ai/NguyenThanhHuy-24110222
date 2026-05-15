import random

percept = [
    [1, 2, 3],
    [4, 6, 0],
    [7, 5, 8]
]

goal = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

rules = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1)
}

visited_states = []

def interpret_input(percept):
    for i in range(3):
        for j in range(3):
            if percept[i][j] == 0:
                return (i, j)

def is_goal(percept):
    return percept == goal


def move_blank(percept, move):
    x, y = interpret_input(percept)
    dx, dy = rules[move]
    nx = x + dx
    ny = y + dy
    percept[x][y], percept[nx][ny] = percept[nx][ny], percept[x][y]


def get_board_state(board):

    return tuple(tuple(row) for row in board)

def is_future_state_visited(percept, move):
    x, y = interpret_input(percept)
    dx, dy = rules[move]
    nx = x + dx
    ny = y + dy
    percept[x][y], percept[nx][ny] = percept[nx][ny], percept[x][y]
    future_state = get_board_state(percept)
    percept[x][y], percept[nx][ny] = percept[nx][ny], percept[x][y]
    return future_state in visited_states


def rule_match(state, rules, percept):
    x, y = state
    possible_moves = []
    for move, (dx, dy) in rules.items():
        nx = x + dx
        ny = y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            if not is_future_state_visited(percept, move):
                possible_moves.append(move)
    if possible_moves:
        return random.choice(possible_moves)

    all_moves = []

    for move, (dx, dy) in rules.items():

        nx = x + dx
        ny = y + dy

        if 0 <= nx < 3 and 0 <= ny < 3:
            all_moves.append(move)

    return random.choice(all_moves)


def simple_reflex_agent(percept):
    state = interpret_input(percept)
    current_state = get_board_state(percept)
    visited_states.append(current_state)
    rule = rule_match(state, rules, percept)
    action = "MOVE " + rule
    move_blank(percept, rule)
    return action


steps = 50

for step in range(steps):
    print("Bước", step + 1)
    result = simple_reflex_agent(percept)
    for row in percept:
        print(row)
    print("Action:", result)
    print()
    if is_goal(percept):
        print("Đã xong")
        break

print("Đã max step")
