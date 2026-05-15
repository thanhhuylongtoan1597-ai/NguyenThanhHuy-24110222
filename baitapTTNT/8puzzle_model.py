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

state = None
model = {}
action = None

visited_states = []


def interpret_input(percept):
    for i in range(3):
        for j in range(3):
            if percept[i][j] == 0:
                return (i, j)


def update_state(state, action, percept, model):

    new_state = interpret_input(percept)

    model["last_state"] = new_state
    model["last_action"] = action

    return new_state


def is_goal(percept):
    return percept == goal


def move_blank(board, move):

    x, y = interpret_input(board)

    dx, dy = rules[move]

    nx = x + dx
    ny = y + dy

    board[x][y], board[nx][ny] = board[nx][ny], board[x][y]


def get_board_state(board):

    return tuple(tuple(row) for row in board)


# xét trước 1 bước tương lai
def is_future_state_visited(percept, move):

    x, y = interpret_input(percept)

    dx, dy = rules[move]

    nx = x + dx
    ny = y + dy

    # di chuyển tạm
    percept[x][y], percept[nx][ny] = percept[nx][ny], percept[x][y]

    future_state = get_board_state(percept)

    # trả lại trạng thái cũ
    percept[x][y], percept[nx][ny] = percept[nx][ny], percept[x][y]

    return future_state in visited_states


def rule_match(state, rules, percept):

    x, y = state

    possible_moves = []

    for move, (dx, dy) in rules.items():

        nx = x + dx
        ny = y + dy

        if 0 <= nx < 3 and 0 <= ny < 3:

            # chỉ chọn trạng thái chưa từng đi
            if not is_future_state_visited(percept, move):
                possible_moves.append(move)

    if possible_moves:
        return random.choice(possible_moves)

    return None


def model_reflex_agent(percept):

    global state
    global model
    global action

    state = update_state(state, action, percept, model)

    current_state = get_board_state(percept)

    visited_states.append(current_state)

    rule = rule_match(state, rules, percept)

    if rule is None:
        print("Không còn đường đi mới!")
        return "STOP"

    action = "MOVE " + rule

    move_blank(percept, rule)

    return action


steps = 5000

for step in range(steps):

    print("Bước", step + 1)

    result = model_reflex_agent(percept)

    for row in percept:
        print(row)

    print("Action:", action)
    print()

    if is_goal(percept):
        print("Đã giải xong!")
        break

    if result == "STOP":
        break