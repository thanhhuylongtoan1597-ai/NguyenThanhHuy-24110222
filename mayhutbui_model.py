import random

room = [
    [0,1,1],
    [1,0,1],
    [1,1,0]
]

step = 1

x = random.randint(0,2)
y = random.randint(0,2)

state = None
action = None

model = {
    "visited": []
}


def print_room():
    for i in range(3):
        for j in range(3):
            print(room[i][j], end=" ")
        print()


def update_state(state, action, room, model):

    new_state = (x, y)

    model["last_state"] = new_state
    model["last_action"] = action

    return new_state


def rule_match(state):

    x, y = state

    possible_moves = []

    if x > 0 and (x-1, y) not in model["visited"]:
        possible_moves.append("Up")

    if x < 2 and (x+1, y) not in model["visited"]:
        possible_moves.append("Down")

    if y > 0 and (x, y-1) not in model["visited"]:
        possible_moves.append("Left")

    if y < 2 and (x, y+1) not in model["visited"]:
        possible_moves.append("Right")

    # nếu hết ô mới thì cho random ô cũ
    if len(possible_moves) == 0:

        if x > 0:
            possible_moves.append("Up")

        if x < 2:
            possible_moves.append("Down")

        if y > 0:
            possible_moves.append("Left")

        if y < 2:
            possible_moves.append("Right")

    return random.choice(possible_moves)


def model_reflex_agent(room):

    global state
    global action
    global x
    global y

    state = update_state(state, action, room, model)

    model["visited"].append(state)

    # nếu bẩn thì hút
    if room[x][y] == 1:

        action = "Suck"

        room[x][y] = 0

    else:

        action = rule_match(state)

        if action == "Up":
            x = x - 1

        elif action == "Down":
            x = x + 1

        elif action == "Left":
            y = y - 1

        elif action == "Right":
            y = y + 1

    return action


print("Phòng ban đầu")
print_room()

while step <= 1000:

    print("Bước", step)

    print("Vị trí RB:", x, y)

    result = model_reflex_agent(room)

    print("Action:", result)

    print_room()

    dirty = False

    for i in range(3):
        for j in range(3):

            if room[i][j] == 1:
                dirty = True

    if dirty == False:
        print("Sàn nhà đã được lau sạch")
        break

    step = step + 1