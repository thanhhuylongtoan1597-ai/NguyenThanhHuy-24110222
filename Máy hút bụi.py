import random
room = [
    [1, 0, 1],
    [0, 1, 0],
    [1, 0, 1]
]
x = random.randint(0, 2)
y = random.randint(0, 2)
def print_room():

    for i in range(3):
        for j in range(3):
            print(room[i][j], end=" ")
        print()
    print()
print("TRẠNG THÁI BAN ĐẦU")
print_room()
step = 1
while step <= 10:
    print("Bước", step)
    print("Vị trí Robot:", x, y)
    if room[x][y] == 1:
        print("Action: SUCK")
        room[x][y] = 0
    else:
        moves = []
        if x > 0:
            moves.append("U")
        if x < 2:
            moves.append("D")
        if y > 0:
            moves.append("L")
        if y < 2:
            moves.append("R")
        action = random.choice(moves)
        print("Action:", action)
        if action == "U":
            x -= 1
        elif action == "D":
            x += 1
        elif action == "L":
            y -= 1
        elif action == "R":
            y += 1
    print_room()
    dirty = False
    for i in range(3):
        for j in range(3):

            if room[i][j] == 1:
                dirty = True
    if dirty == False:
        print("TẤT CẢ ĐÃ SẠCH!")
        break
    step += 1