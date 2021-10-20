from pico2d import *
import random as rd

class Mario:  # 죽는 모션//달리기 방향 전환//점프 하강 착지 조건 변경
    def __init__(self):
        self.x, self.y = canvas_width//2, canvas_height//2 - 280
        self.frameX = 0
        self.action = 1
        self.dir = 0
        self.heading = 0
        self.jump_cnt = 13
        self.running_speed = 1.0
        self.running_cnt = 0
        self.down = False
        self.down_motion_flag = False
        self.image = load_image('mario.png')
        self.action_frame = [0,22,22,23,23,23,23,26,26]
        self.rect = [self.x - 25, self.y - 40, self.x + 25, self.y + 40]

    def update(self,act):
        global action
        x_speed = 15
        jump_speed = 40
        gravity = jump_speed / 11

        if action == 7 or action == 8:
            self.running_cnt += 1
            if self.running_speed < 2.1:
                self.running_speed += 0.03
        else:
            if self.running_speed > 1:
                self.running_speed -= 0.1

        if action == 4 or action == 8:
            if self.running_cnt > 17:
                self.frameX = abs((self.frameX - 1) % 8)
            else:
                self.frameX = abs((self.frameX - 1) % self.action_frame[action])
        else:
            if self.running_cnt > 17:
                self.frameX = (self.frameX + 1) % 8 + 18
            else:
                self.frameX = (self.frameX + 1) % self.action_frame[action]

        if self.down_motion_flag:
            self.frameX = 18

        if self.dir < 0:
            self.x -= x_speed * self.running_speed
        elif self.dir > 0:
            self.x += x_speed * self.running_speed

        if self.down:
            self.y += jump_speed - self.jump_cnt * gravity
            if self.jump_cnt < 26:
                self.jump_cnt += 1
            if self.frameX == 18:
                self.down_motion_flag = True
            if self.y <= canvas_height//2 - 280:
                action = 1
                self.down = False
                self.y = canvas_height//2 - 280
                self.jump_cnt = 13
                self.down_motion_flag = False

        if (action == 5 or action == 6) and self.down == False:
            self.y += jump_speed - self.jump_cnt * gravity
            self.jump_cnt += 1
            if jump_speed - self.jump_cnt * gravity < 0:
                self.down = True

        if action == 5 or action == 6:
            if self.dir == -1:
                action = 6
            elif self.dir == 1:
                action = 5
        elif action == 7 or action == 8:
            if self.dir == -1:
                action = 8
            elif self.dir == 1:
                action = 7
        elif self.dir == 0:
            if self.heading == -1:
                action = 2
            elif self.heading == 1:
                action = 1
        elif action != 5 and action != 6 and action != 7 and action != 8:
            if self.dir == -1:
                action = 4
            elif self.dir == 1:
                action = 3

        self.rect = [self.x - 20, self.y - 40, self.x + 20, self.y + 40]

    def draw(self, act):
        png_height = 656
        if act == 1 or act == 2:
            self.image.clip_draw(self.frameX * 20, png_height - 40 * act, 20,38,self.x, self.y,60,120)
        elif act == 3:
            self.image.clip_draw(self.frameX * 30, png_height - 40 * act, 30, 38, self.x, self.y,90,120)
        elif 3 < act or act < 9:
            self.image.clip_draw(self.frameX * 30, png_height - 40 * act, 30, 38, self.x, self.y,90,120)

class Map:
    pass

class Object:
    pass

class Monster:  #굼바 방향전환 모션, 다른 몬스터들
    def __init__(self,kind):
        self.x = rd.randint(0,1200)
        self.y = 155
        self.frame = 0
        self.heading = -1
        self.life = True
        self.action = 1
        self.Kind = kind
        self.sprite_num = [[9,9,2,2,2],[7,7,7,7]] # 0 = Goomba // 1 =
        self.size = [[30,30]]
        self.rect = [self.x - self.size[self.Kind][0],self.y - self.size[self.Kind][1],
                     self.x + self.size[self.Kind][0],self.y + self.size[self.Kind][1]]
        self.testcnt = 0

        if self.Kind == 0:
            self.img = load_image('goomba.png')
        elif self.Kind == 1:
            self.img = load_image('goomba.png')
        elif self.Kind == 2:
            self.img = load_image('goomba.png')
        elif self.Kind == 3:
            self.img = load_image('goomba.png')

    def update(self):
        if self.action == 4:
            if self.frame % 2 == 0:
                self.action = 1
                #self.heading = -1

        elif self.action == 3:
            if self.frame % 2 == 0:
                self.action = 2
                #self.heading = 1

        if self.action == 1:
            self.x -= 5
        elif self.action == 2:
            self.x += 5

        if 1190 < self.x:
            self.frame = 0
            self.action = 4
            self.x = 1188
        elif 10 > self.x:
            self.frame = 0
            self.action = 3
            self.x = 11

        if self.life == False:
            self.testcnt += 1
            if self.testcnt % 70 == 69:
                self.testcnt = 0
                self.action = rd.randint(1,2)
                # if self.action == 1:
                #     self.heading = -1
                # else:
                #     self.heading = 1
                self.life = True
                self.x = rd.randint(0,1200)

        self.frame = (self.frame + 1) % self.sprite_num[self.Kind][self.action - 1]
        self.rect = [self.x - self.size[self.Kind][0],self.y - self.size[self.Kind][1],
                     self.x + self.size[self.Kind][0],self.y + self.size[self.Kind][1]]

    def draw(self):
        png_h = 600
        if self.life:
            if self.Kind == 0:
                self.img.clip_draw(self.frame * 20, png_h - 20 * self.action, 20,20,self.x, self.y, 60, 60)
            elif self.Kind == 1:
                self.img.clip_draw(self.frame * 20, png_h - 20 * 1, 20,20,self.x, self.y, 60, 60)
            elif self.Kind == 2:
                self.img.clip_draw(self.frame * 20, png_h - 20 * 1, 20,20,self.x, self.y, 60, 60)
            elif self.Kind == 3:
                self.img.clip_draw(self.frame * 20, 200, 20,20,self.x, self.y)
        else:
            if self.Kind == 0 and self.testcnt < 15:
                self.frame = self.testcnt - 1
                if self.testcnt > 2:
                    self.frame = 1
                self.img.clip_draw(self.frame * 25, png_h - 20 * self.action, 25, 20, self.x, self.y, 60, 60)

def InRect(Rect,pt):
    if Rect[0] < pt[0] and pt[0] < Rect[2] and Rect[1] < pt[1] and pt[1] < Rect[3]:
        return True
    else:
        return False

def handle_events():
    global running
    global action
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        # elif event.type == SDL_MOUSEMOTION:
        #     x, y = event.x, canvas_height - 1 - event.y
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_UP:
                if action != 5 and action != 6:
                    mario.frameX = 0
                    mario.jump_cnt = 0
                    mario.running_cnt = 0
                    if mario.dir == 1 or mario.heading == 1:
                        action = 5
                    elif mario.dir == -1 or mario.heading == -1:
                        action = 6
            if event.key == SDLK_LEFT:
                mario.dir -= 1
                mario.heading = -1
            if event.key == SDLK_DOWN:
                pass
            if event.key == SDLK_RIGHT:
                mario.dir += 1
                mario.heading = 1
            if event.key == SDLK_LSHIFT:
                mario.frameX = 0
                if action == 3 or action == 4 and action != 5 and action != 6:
                    if mario.heading == 1:
                        action = 7
                    elif mario.heading == -1:
                        action = 8
            if event.key == SDLK_SPACE:
                mario.frameX = 0
                mario.jump_cnt = 0
                mario.running_cnt = 0
                if mario.dir == 1 or mario.heading == 1:
                    action = 5
                elif mario.dir == -1 or mario.heading == -1:
                    action = 6
            if event.key == SDLK_ESCAPE:
                running = False
        elif event.type == SDL_KEYUP:
            # if event.key == SDLK_UP:
            #     action
            if event.key == SDLK_LEFT:
                mario.dir += 1
            if event.key == SDLK_DOWN:
                pass
            if event.key == SDLK_RIGHT:
                mario.dir -= 1
            if event.key == SDLK_LSHIFT:
                mario.running_cnt = 0
                if action == 7 or action == 8:
                    if mario.dir == -1:
                        action = 4
                    elif mario.dir == 1:
                        action = 3
                    elif mario.dir == 0:
                        if mario.heading == -1:
                            action = 2
                        elif mario.heading == 1:
                            action = 1

                elif action == 5 or action == 6:
                    if mario.dir == -1:
                        action = 6
                    elif mario.dir == 1:
                        action = 5

canvas_width = 1200
canvas_height = 900
action = 1
open_canvas(canvas_width,canvas_height)
mario = Mario()

testmap = load_image('testmap.png')

goombas = [Monster(0) for i in range(5)]
# green_turtle = Monster(1)
# red_turtle = Monster(2)
# gr_turtle = Monster(3)

running = True

while(running):
    clear_canvas()
    testmap.draw(600, 450)
    mario.draw(action)
    mario.update(action)

    for i in range(5):
        goombas[i].update()
        goombas[i].draw()

    for i in range(5):  # 충돌체크
        if InRect(goombas[i].rect, [mario.x, mario.y]) and mario.down == False:
            if goombas[i].life:
                mario.y = 800
                mario.down = True
                mario.jump_cnt = 13
                if mario.heading == 1:
                    action = 5
                elif mario.heading == -1:
                    action = 6
        elif InRect(goombas[i].rect, [mario.x, mario.y - 40]) and mario.down:
            if goombas[i].life:
                goombas[i].action = 5
                goombas[i].frame = 0
                goombas[i].life = False
                if mario.heading == -1:
                    action = 6
                elif mario.heading == 1:
                    action = 5
                mario.frameX = 0
                mario.down = False
                mario.down_motion_flag = False
                mario.jump_cnt = 3
                print(goombas[i].frame, goombas[i].action)


    update_canvas()
    handle_events()
    delay(0.035)

close_canvas()