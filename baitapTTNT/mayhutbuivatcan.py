import random
room=[[0,1,2],
      [1,0,1],
      [1,2,0]]

step=1

x=random.randint(0,2)
y=random.randint(0,2)

while(room[x][y]==2):
    x=random.randint(0,2)
    y=random.randint(0,2)

def print_room():
    for i in range(3):
            for j in range(3):
                print(room[i][j], end=" ")
            print()

print("Phòng ban đầu")
print_room()

while step<=1000:
    print("Bước",step)
    print('Vị trí RB:',x,y)
    if(room[x][y]==1):
        print('action: Suck')
        room[x][y]=0
    else:
        move=[]
        if(x>0 and room[x-1][y]!=2):
            move.append("Up")
        if(x<2 and room[x+1][y]!=2):
            move.append("Down")
        if(y>0 and room[x][y-1]!=2):
            move.append('Left')
        if(y<2 and room[x][y+1]!=2):
            move.append('Right')
        action=random.choice(move)
        print('action:',action)
        if(action=="Up"):
            x=x-1
        if(action=="Down"):
            x=x+1
        if(action=="Left"):
            y=y-1
        if(action=="Right"):
            y=y+1
    print_room()
    dirty=False
    for i in range (3):
        for j in range (3):
            if(room[i][j]==1):
                dirty=True
    if(dirty==False):
        print("Sàn nhà đã được lau sạch")
        break
    step=step+1