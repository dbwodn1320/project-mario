import random

def SetMonsterPos(num,map_len ,another = None):
    seg = map_len // num
    mon_pos = [random.randint(10 + seg * i,seg * (i+1)) for i in range(num)]
    if another == None:
        return mon_pos
    else:
        for i in range(len(mon_pos)):
            if mon_pos[i] == another[i]:
                print(mon_pos[i], another[i])
                while 1:
                    mon_pos[i] = random.randint(10 + seg * i,seg * (i+1))
                    #print(mon_pos[i],another[i])
                    if mon_pos[i] != another[i]:
                        break
        return mon_pos

def SetBlockAttribute(num,map_data,num2 = 0):
    map_len = len(map_data)
    seg = map_len // num

    Block_Attribute = [[random.randint(0,3),random.randint(10 + seg * i,seg * (i + 1)),0] for i in range(num)]
    for block in Block_Attribute:
            block[2] = len(map_data[block[1]]) + random.randint(3, 4)

    tmp3 = [i for i in range(0, len(Block_Attribute) - 1)]
    tmp2 = []
    for i in range(num2):
        index = random.randint(0,len(tmp3)-1)
        tmp2.append([tmp3[index],random.randint(4, 6)])
        tmp3.remove(tmp3[index])

    for i in range(len(tmp2)):
        tmp = [random.randint(0,1),Block_Attribute[tmp2[i][0]][1],Block_Attribute[tmp2[i][0]][2] + tmp2[i][1]]
        Block_Attribute.append(tmp)

    for block in Block_Attribute.copy():
        for i in range(random.randint(3,4)):
            tmp = [random.randint(0,1),block[1] + i + 1,block[2]]
            Block_Attribute.append(tmp)

    #print(Block_Attribute)
    Block_Attribute = sorted(Block_Attribute,key = lambda x: x[1])
    #print(Block_Attribute)

    for block in Block_Attribute.copy():
        if -2 < len(map_data[block[1]]) - block[2] < 2:
            Block_Attribute.remove(block)

    return Block_Attribute

def SetCoinPos(blockpos, num):
    pass
