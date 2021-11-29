f = open("map_date.txt", 'r')
lines = f.readlines()
f.close()
map_data = []

for line in lines:
    line = line.strip()
    tmp = []
    if line == "=":
        map_data.append(tmp)
    else:
        t = line
        line = int(line)
        while 1:
            tmp.append(line % 10)
            line = line // 10
            if line == 0: break
        if len(t) > 1:
            if t[0] == '0':
                tmp.append(0)
        tmp.reverse()
        map_data.append(tmp)

DEBUG_KEY,RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SHIFT_DOWN, SHIFT_UP, SPACE, UP, DOWN, Landing = range(11)
DashState,IdleState,RunState,JumpState,FallingState,LandingState = range(6)

map1 = [[0,3,3],[0,4,3],[0,5,3],[0,6,3],[0,7,3]] #(kind,x,y)
map2 = [[0,0,0],[0,0,0]]

blocks = None
mario = None
ground_tiles = None
goombas = None
green_trutles = None

