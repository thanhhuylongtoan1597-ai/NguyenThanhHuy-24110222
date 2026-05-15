start = [
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


def print_board(board):

    for row in board:
        print(row)

    print()


def get_zero(board):

    for i in range(3):
        for j in range(3):

            if board[i][j] == 0:
                return (i, j)


def get_state(board):

    return tuple(tuple(row) for row in board)


def child_node(board, action):

    x, y = get_zero(board)

    dx, dy = rules[action]

    nx = x + dx
    ny = y + dy

    if 0 <= nx < 3 and 0 <= ny < 3:

        new_board = [row[:] for row in board]

        new_board[x][y], new_board[nx][ny] = \
        new_board[nx][ny], new_board[x][y]

        return new_board

    return None


def bfs(start, goal):

    queue = []

    queue.append((start, []))

    visited = []

    while len(queue) > 0:

        current_board, path = queue.pop(0)

        print("Trạng thái hiện tại:")
        print_board(current_board)

        if current_board == goal:

            print("Đã giải xong!")
            return path

        current_state = get_state(current_board)

        visited.append(current_state)

        for action in rules:

            child = child_node(current_board, action)

            if child is not None:

                child_state = get_state(child)

                if child_state not in visited:

                    queue.append(
                        (child, path + [action])
                    )

    return None


result = bfs(start, goal)

print("Đường đi:")

for step in result:
    print(step)