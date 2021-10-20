from pico2d import *
import random as rd

class Mario:
    def __init__(self):
        self.x, self.y = canvas_width//2, canvas_height//2 - 200
        self.frameX = 0
        self.action = 1
        self.dir = 0
        self.heading = 0
        self.jump_cnt = 0
        self.running_speed = 1.0
        self.running_cnt = 0
        self.image = load_image('mario.png')
        self.action_frame = [0,22,22,23,23,23,23,26,26]
        self.RECT = [self.x - 30, self.y - 50, self.x + 30, self.y + 50]
    def update(self,act):
        global action
        x_speed = 15
        jump_speed = 40
        gravity = jump_speed / 11

        if action == 7 or action == 8:
            self.running_cnt += 1
            if self.running_speed < 3.0:
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

        if self.dir < 0:
            self.x -= x_speed * self.running_speed
        elif self.dir > 0:
            self.x += x_speed * self.running_speed

        if action == 5 or action == 6:
            self.y += jump_speed - self.jump_cnt * gravity
            self.jump_cnt += 1
            if self.y <= canvas_height//2 - 200:
                action = 1
                self.y = canvas_height//2 - 200
                self.jump_up = True
                self.jump_cnt = 0

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

class Monster:
    def __init__(self,kind):
        self.x = rd.randint(0,1200)
        self.y = 230
        self.frame = 0
        self.heading = 0
        self.life = True
        self.sprite_num = [9,7,7,7]
        self.Kind_of_Monster = kind

        if self.Kind_of_Monster == 0:
            self.img = load_image('goomba.png')
        elif self.Kind_of_Monster == 1:
            self.img = load_image('goomba.png')
        elif self.Kind_of_Monster == 2:
            self.img = load_image('goomba.png')
        elif self.Kind_of_Monster == 3:
            self.img = load_image('goomba.png')

    def update(self):
        if self.heading == 0:
            self.x -= 5
        elif self.heading == 1:
            self.x += 5

        if mario.x > self.x:
            self.heading = 1
        else:
            self.heading = 0

        self.frame = (self.frame + 1) % self.sprite_num[self.Kind_of_Monster]
    def draw(self):
        png_h = 600
        if self.life:
            if self.Kind_of_Monster == 0:
                self.img.clip_draw(self.frame * 20, png_h - 20 * (1+self.heading), 20,20,self.x, self.y, 60, 60)
            elif self.Kind_of_Monster == 1:
                self.img.clip_draw(self.frame * 20, png_h - 20 * 1, 20,20,self.x, self.y, 60, 60)
            elif self.Kind_of_Monster == 2:
                self.img.clip_draw(self.frame * 20, png_h - 20 * 1, 20,20,self.x, self.y, 60, 60)
            elif self.Kind_of_Monster == 3:
                self.img.clip_draw(self.frame * 20, 200, 20,20,self.x, self.y)
        else:
            if self.Kind_of_Monster == 0:
                self.img.clip_draw(self.frame * 20, png_h - 20 * 1, 20,20,self.x, self.y, 60, 60)
            elif self.Kind_of_Monster == 1:
                self.img.clip_draw(self.frame * 20, png_h - 20 * 1, 20,20,self.x, self.y, 60, 60)
            elif self.Kind_of_Monster == 2:
                self.img.clip_draw(self.frame * 20, png_h - 20 * 1, 20,20,self.x, self.y, 60, 60)
            elif self.Kind_of_Monster == 3:
                self.img.clip_draw(self.frame * 20, 200, 20,20,self.x, self.y)

def InRect(Rect,pt):
    if Rect[0] < pt[0] and pt[0] < Rect[3] and Rect[1] < pt[1] and pt[1] < Rect[3]:
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

goombas = [Monster(0) for i in range(3)]
# green_turtle = Monster(1)
# red_turtle = Monster(2)
# gr_turtle = Monster(3)

running = True

while(running):
    clear_canvas()
    mario.draw(action)
    mario.update(action)
    for i in range(3):
        goombas[i].update()
        goombas[i].draw()
   #print(mario.dir, action)
    update_canvas()
    handle_events()
    delay(0.035)

close_canvas()



