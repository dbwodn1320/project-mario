from GenerateRandomObj import *

map_kind = 1
map_data = []

def ReadMapTxt(map_kind):
    data = []

    if map_kind == 1:
        f = open("map1_date.txt", 'r')
        lines = f.readlines()
        f.close()
        for line in lines:
            line = line.strip()
            tmp = []
            if line == "=":
                data.append(tmp)
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
                data.append(tmp)

    elif map_kind == 2:
        f = open("map2_date.txt", 'r')
        lines = f.readlines()
        f.close()
        for line in lines:
            line = line.strip()
            tmp = []
            if line == "=":
                data.append(tmp)
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
                data.append(tmp)

    return data,len(data)

DEBUG_KEY,RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SHIFT_DOWN, SHIFT_UP, DEATH, UP, DOWN, Landing = range(11)
DashState,IdleState,RunState,JumpState,FallingState,DeathState = range(6)

mario = None
ground_tiles = None
background = None

map_len = len(map_data)

mushrooms = []

coins_num = 15
coins = None

blocks_center = 15
blocks = None

goombas_num = 10
goombas = None

turtle_num = 10
green_trutles = None

