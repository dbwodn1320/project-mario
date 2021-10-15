from pico2d import *

class Mario:
    def __init__(self):
        self.x, self.y = 600, 450
        self.frameX = 0
        self.action = 1
        self.dir = 0
        self.heading = 0
        self.jump_height_check = 0
        self.jump_up = True

        self.image = load_image('mario.png')
        self.action_frame = [0,23,23,24,24,24,26]
        #self.action_delay = [0,0.035,0.035,0.035,0.035]
    def update(self,act):
        global action
        x_speed = 5
        jump_speed = 8
        self.frameX = (self.frameX + 1) % self.action_frame[action]
        if self.dir < 0:
            self.x -= x_speed
        elif self.dir > 0:
            self.x += x_speed

        if action == 5 or action == 6:
            if self.jump_up:
                self.y += jump_speed
                self.jump_height_check += jump_speed
            else:
                self.y -= jump_speed
                self.jump_height_check -= jump_speed
                if self.jump_height_check <= 0:
                    self.jump_height_check = 0
                    action = 1
                    self.jump_up = True

            if self.jump_height_check > jump_speed * 10:
                self.jump_up = False

    def draw(self, act):
        if act == 1 or act == 2:
            self.image.clip_draw(self.frameX * 20, 511 - 40 * act, 20, 38, self.x, self.y)
        if act == 3 or act == 4 or act == 5 or act == 6:
            self.image.clip_draw(self.frameX * 30, 511 - 40 * act, 30, 38, self.x, self.y)

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
                    if mario.dir == 1:
                        action = 5
                    elif mario.dir == -1:
                        action = 6
            if event.key == SDLK_LEFT:
                mario.dir -= 1
                mario.heading = -1
            if event.key == SDLK_DOWN:
                pass
            if event.key == SDLK_RIGHT:
                mario.dir += 1
                mario.heading = 1
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

canvas_width = 1200
canvas_height = 900
action = 1
open_canvas(canvas_width,canvas_height)
mario = Mario()

running = True

while(running):
    clear_canvas()
    mario.draw(action)
    mario.update(action)
    print(mario.dir, mario.heading)

    if action == 5 or action == 6:
        if mario.dir == -1:
            action = 6
        elif mario.dir == 1:
            action = 5
    elif mario.dir == 0:
        if mario.heading == 1:
            action = 1
        elif mario.heading == -1:
            action = 2
    elif action != 5 and action != 6:
        if mario.dir == -1:
            action = 4
        elif mario.dir == 1:
            action = 3



    update_canvas()
    handle_events()
    delay(0.035)

close_canvas()



