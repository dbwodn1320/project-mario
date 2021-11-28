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

mario = None
ground_tiles = None
goomba = None
green_trutle = None

DEBUG_KEY,RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SHIFT_DOWN, SHIFT_UP, SPACE, UP, DOWN, Landing = range(11)
DashState,IdleState,RunState,JumpState,FallingState,LandingState = range(6)