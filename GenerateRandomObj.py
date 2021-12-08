import random

def SetMonsterPos(num,map_len ,another = None):
    seg = map_len // num
    mon_pos = [random.randint(10 + seg * i,seg * (i+1)) for i in range(num)]
    if another == None:
        return mon_pos
    else:
        for i in range(len(mon_pos)):
            if mon_pos[i] == another[i]:
                #print(mon_pos[i], another[i])
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
    for block in Block_Attribute.copy():
            if len(map_data[block[1]]) == 0:
                Block_Attribute.remove(block)
            else:
                block[2] = len(map_data[block[1]]) + 4  # random.randint(4, 5)

    tmp3 = [i for i in range(0, len(Block_Attribute) - 1)]
    tmp2 = []
    for i in range(num2):
        index = random.randint(0,len(tmp3)-1)
        tmp2.append([tmp3[index],random.randint(4, 5)])
        tmp3.remove(tmp3[index])

    for i in range(len(tmp2)):
        tmp = [random.randint(0,1),Block_Attribute[tmp2[i][0]][1],Block_Attribute[tmp2[i][0]][2] + tmp2[i][1]]
        Block_Attribute.append(tmp)

    coin_pos = []
    # 블록
    for block in Block_Attribute.copy():
        if random.randint(0,2) == 0 or 1:
            coin_pos.append([block[1], block[2] + 2])
        for i in range(random.randint(3,4)):
            tmp = [random.randint(0,1),block[1] + i + 1,block[2]]
            Block_Attribute.append(tmp)

    # 코인
    for coin in coin_pos.copy():
        a = random.randint(2, 4)
        if a == 2:
            b = random.randint(0, 2)
            coin[0] += b
            for i in range(a):
                coin_pos.append([coin[0] + i,coin[1]])
        if a == 3:
            b = random.randint(0, 1)
            if b == 0:
                c = random.randint(0, 1)
                coin[0] += c
                for i in range(a):
                    coin_pos.append([coin[0] + i + 1, coin[1]])
            else:
                coin[0] = coin[0] + 2
                coin_pos.append([coin[0] + 1, coin[1] + 1])
                coin_pos.append([coin[0] + 2, coin[1] + 1])
                coin_pos.append([coin[0] + 3, coin[1]])
        if a == 4:
            b = random.randint(0, 1)
            if b == 0:
                for i in range(a):
                    coin_pos.append([coin[0] + i + 1, coin[1]])
            else:
                c = random.randint(3, 5)
                coin[0] = coin[0] + c
                coin[1] = coin[1]
                coin_pos.append([coin[0] + 1, coin[1] + 2])
                coin_pos.append([coin[0] + 2, coin[1] + 2])
                coin_pos.append([coin[0] + 3, coin[1] + 2])
                coin_pos.append([coin[0] + 4, coin[1]])

    #print(Block_Attribute)
    Block_Attribute = sorted(Block_Attribute,key = lambda x: x[1])
    #print(Block_Attribute)

    for block in Block_Attribute.copy():
        if block[1] > len(map_data) - 1:
            Block_Attribute.remove(block)

    for block in Block_Attribute.copy():
        if -2 < len(map_data[block[1]]) - block[2] < 2:
            Block_Attribute.remove(block)

    return Block_Attribute, coin_pos

def SetCoinPos(blockpos, num):
    pass
