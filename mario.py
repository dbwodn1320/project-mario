import game_framework
from pico2d import *
import game_world
import time
import collision
import server

frame_time = 0.0

PIXEL_PER_METER = (100.0 / 1.5)

MARIO_JUMP = 30 * PIXEL_PER_METER
GRAVITY = 80 * PIXEL_PER_METER

RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.75
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = [0, 22, 22, 23, 23, 23, 23, 26, 26]

DEBUG_KEY,RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SHIFT_DOWN, SHIFT_UP, SPACE, UP, DOWN, Landing = range(11)

event_name = ['DEBUG_KEY','RIGHT_DOWN', 'LEFT_DOWN', 'RIGHT_UP', 'LEFT_UP', 'SLEEP_TIMER',\
'SHIFT_DOWN','SHIFT_UP','SPACE','UP','DOWN','Landing']

key_event_table = {
    (SDL_KEYDOWN, SDLK_SPACE): SPACE,
    (SDL_KEYDOWN, SDLK_d): DEBUG_KEY,
    (SDL_KEYDOWN, SDLK_RSHIFT): SHIFT_DOWN,
    (SDL_KEYDOWN, SDLK_LSHIFT): SHIFT_DOWN,
    (SDL_KEYUP, SDLK_RSHIFT): SHIFT_UP,
    (SDL_KEYUP, SDLK_LSHIFT): SHIFT_UP,

    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_UP): UP
}

class IdleState:
    def enter(mario, event):
        mario.jump_cnt = 0
        mario.cur_state_int = 1
        if event == RIGHT_DOWN:
            mario.dir += 1
            mario.heading = 1
        elif event == LEFT_DOWN:
            mario.dir -= 1
            mario.heading = -1
        elif event == RIGHT_UP:
            mario.dir -= 1
        elif event == LEFT_UP:
            mario.dir += 1
        elif event == DEBUG_KEY:
            mario.god = 1 - mario.god

    def exit(mario, event):
        pass

    def do(mario):
        if mario.heading == 1:
            mario.action = 1
        else:
            mario.action = 2
        mario.frame = (mario.frame + FRAMES_PER_ACTION[mario.action] * ACTION_PER_TIME * game_framework.frame_time) % mario.action_frame[mario.action]

    def draw(mario):
        if mario.heading == 1:
            mario.image.clip_draw(int(mario.frame) * 20, 656 - 40 * mario.action, 20, 40, mario.x, mario.y,60,120)
        elif mario.heading == -1:
            mario.image.clip_draw(int(mario.frame) * 20, 656 - 40 * mario.action, 20, 40, mario.x, mario.y,60,120)

class RunState:
    def enter(mario, event):
        mario.cur_state_int = 2
        mario.jump_cnt = 0
        if event == RIGHT_DOWN:
            mario.dir += 1
            mario.heading = 1
        elif event == LEFT_DOWN:
            mario.dir -= 1
            mario.heading = -1
        elif event == RIGHT_UP:
            mario.dir -= 1
        elif event == LEFT_UP:
            mario.dir += 1

    def exit(mario, event):
        pass

    def do(mario):
        if mario.heading == 1:
            mario.action = 3
            mario.frame = (mario.frame + FRAMES_PER_ACTION[mario.action]  * ACTION_PER_TIME * game_framework.frame_time) % \
                          mario.action_frame[mario.action]
        else:
            mario.action = 4
            mario.frame = abs((mario.frame - FRAMES_PER_ACTION[mario.action]  * ACTION_PER_TIME * game_framework.frame_time) % \
                          mario.action_frame[mario.action])

        mario.x += mario.velocity * mario.dash_mult * game_framework.frame_time

        mario.dash_mult += mario.dir * 4.0 * game_framework.frame_time
        if mario.dash_mult < -1.0:
            mario.dash_mult = -1.0
        elif mario.dash_mult > 1.0:
            mario.dash_mult = 1.0

    def draw(mario):
        if mario.heading == 1:
            mario.image.clip_draw(int(mario.frame) * 30, 656 - 40 * mario.action, 30, 40, mario.x, mario.y,90,120)
        else:
            mario.image.clip_draw(int(mario.frame) * 30, 656 - 40 * mario.action, 30, 40, mario.x, mario.y,90,120)

class DashState:
    def enter(mario, event):
        mario.cur_state_int = 0
        if event == RIGHT_DOWN:
            mario.dir += 1
            mario.heading = 1
        elif event == LEFT_DOWN:
            mario.dir -= 1
            mario.heading = -1
        elif event == RIGHT_UP:
            mario.dir -= 1
        elif event == LEFT_UP:
            mario.dir += 1
        mario.dash_timer = 0

    def exit(mario, event):
        mario.dash_timer = 0

    def do(mario):
        if mario.heading == 1:
            mario.action = 7
            if mario.dash_timer > 17:
                mario.frame = (mario.frame + FRAMES_PER_ACTION[
                    mario.action] * ACTION_PER_TIME * game_framework.frame_time) % 8 + 18
            else:
                mario.frame = (mario.frame + FRAMES_PER_ACTION[
                    mario.action] * ACTION_PER_TIME * game_framework.frame_time) % \
                              mario.action_frame[mario.action]
        else:
            mario.action = 8
            if mario.dash_timer > 17:
                mario.frame = abs(
                    (mario.frame - FRAMES_PER_ACTION[mario.action] * ACTION_PER_TIME * game_framework.frame_time) % 8)
            else:
                mario.frame = abs(
                    (mario.frame - FRAMES_PER_ACTION[mario.action] * ACTION_PER_TIME * game_framework.frame_time) % \
                    mario.action_frame[mario.action])


        mario.dash_timer +=  FRAMES_PER_ACTION[mario.action] * ACTION_PER_TIME * game_framework.frame_time
        mario.x += mario.velocity * mario.dash_mult * game_framework.frame_time
        mario.dash_mult += 5.0 * mario.dir * game_framework.frame_time
        if mario.dash_mult < -3.0:
            mario.dash_mult = -3.0
        elif mario.dash_mult > 3.0:
            mario.dash_mult = 3.0

    def draw(mario):
            if mario.heading == 1:
                mario.image.clip_draw(int(mario.frame) * 30, 656 - 40 * mario.action, 30, 40, mario.x, mario.y,90,120)
            else:
                mario.image.clip_draw(int(mario.frame) * 30, 656 - 40 * mario.action, 30, 40, mario.x, mario.y,90,120)

class JumpState:
    def enter(mario, event):
        mario.frame = 0
        mario.cur_state_int = 3
        if event == RIGHT_DOWN:
            mario.dir += 1
            mario.heading = 1
        elif event == LEFT_DOWN:
            mario.dir -= 1
            mario.heading = -1
        elif event == RIGHT_UP:
            mario.dir -= 1
        elif event == LEFT_UP:
            mario.dir += 1

    def exit(mario, event):
        pass

    def do(mario):
        if mario.heading == 1:
            mario.action = 5
            mario.frame = (mario.frame + FRAMES_PER_ACTION[mario.action] * ACTION_PER_TIME * game_framework.frame_time) % \
                          mario.action_frame[mario.action]
        else:
            mario.action = 6
            mario.frame = (mario.frame + FRAMES_PER_ACTION[mario.action] * ACTION_PER_TIME * game_framework.frame_time) % \
                          mario.action_frame[mario.action]

        mario.x += mario.velocity * mario.dash_mult * game_framework.frame_time
        mario.dash_mult += mario.dir * 4.0 * game_framework.frame_time
        if mario.dash_mult < -1.0:
            mario.dash_mult = -1.0
        elif mario.dash_mult > 1.0:
            mario.dash_mult = 1.0
        if  610 > mario.x and mario.x > 590:
            mario.x = 600
        mario.y += (MARIO_JUMP - mario.jump_cnt * GRAVITY) * game_framework.frame_time
        mario.jump_cnt += game_framework.frame_time
        if MARIO_JUMP - mario.jump_cnt * GRAVITY < 0:
            mario.add_event(DOWN)
            mario.jump_cnt = 0

    def draw(mario):
        if mario.heading == 1:
            mario.image.clip_draw(int(mario.frame) * 30, 656 - 40 * mario.action, 30, 40, mario.x, mario.y,90,120)
        else:
            mario.image.clip_draw(int(mario.frame) * 30, 656 - 40 * mario.action, 30, 40, mario.x, mario.y,90,120)

class FallingState:
    def enter(mario, event):
        mario.cur_state_int = 4
        if event == RIGHT_DOWN:
            mario.dir += 1
            mario.heading = 1
        elif event == LEFT_DOWN:
            mario.dir -= 1
            mario.heading = -1
        elif event == RIGHT_UP:
            mario.dir -= 1
        elif event == LEFT_UP:
            mario.dir += 1

    def exit(mario, event):
        pass

    def do(mario):
        if mario.heading == 1:
            mario.action = 5
            mario.frame = (mario.frame + FRAMES_PER_ACTION[mario.action] * ACTION_PER_TIME * game_framework.frame_time) % \
                          mario.action_frame[mario.action]
        else:
            mario.action = 6
            mario.frame = (mario.frame + FRAMES_PER_ACTION[mario.action] * ACTION_PER_TIME * game_framework.frame_time) % \
                          mario.action_frame[mario.action]

        mario.x += mario.velocity * mario.dash_mult * game_framework.frame_time
        mario.dash_mult += mario.dir * 4.0 * game_framework.frame_time
        if mario.dash_mult < -1.0:
            mario.dash_mult = -1.0
        elif mario.dash_mult > 1.0:
            mario.dash_mult = 1.0
        if  610 > mario.x and mario.x > 590:
            mario.x = 600
        mario.y += -mario.jump_cnt * GRAVITY * game_framework.frame_time
        mario.jump_cnt += game_framework.frame_time

    def draw(mario):
        if mario.heading == 1:
            mario.image.clip_draw(int(mario.frame) * 30, 656 - 40 * mario.action, 30, 40, mario.x, mario.y,90,120)
        else:
            mario.image.clip_draw(int(mario.frame) * 30, 656 - 40 * mario.action, 30, 40, mario.x, mario.y,90,120)

class LandingState:
    def enter(mario, event):
        mario.cur_state_int = 5

    def exit(mario, event):
        pass

    def do(mario):
        pass

    def draw(mario):
        pass

next_state_table = {
    DashState: {SHIFT_UP:RunState,SHIFT_DOWN:RunState,LEFT_UP:RunState,LEFT_DOWN:RunState,RIGHT_UP:RunState,RIGHT_DOWN:RunState, SPACE: DashState,UP: DashState,DOWN: FallingState},

    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState,
                SHIFT_UP: IdleState,SHIFT_DOWN:IdleState,SPACE: IdleState,UP:JumpState, DOWN:FallingState},

    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
               SHIFT_DOWN:DashState,SHIFT_UP:RunState,SPACE: RunState, UP:JumpState, DOWN:FallingState, Landing:RunState},

    JumpState: {RIGHT_UP: JumpState, LEFT_UP: JumpState, LEFT_DOWN: JumpState, RIGHT_DOWN: JumpState,
               SHIFT_DOWN:JumpState,SHIFT_UP:JumpState,SPACE: JumpState,UP:JumpState,DOWN:FallingState,Landing: LandingState},

    FallingState: { RIGHT_UP: FallingState, LEFT_UP: FallingState, LEFT_DOWN: FallingState, RIGHT_DOWN: FallingState,
               SHIFT_DOWN:FallingState,SHIFT_UP:FallingState,SPACE: FallingState, UP:JumpState,Landing: RunState},

    LandingState: { RIGHT_UP: RunState, LEFT_UP: RunState, LEFT_DOWN: RunState, RIGHT_DOWN: RunState,
       SHIFT_DOWN: RunState, SHIFT_UP: RunState, SPACE: RunState, UP: RunState}
}

class Mario:
    def __init__(self):
        self.action = 1
        self.action_frame = [0, 22, 22, 23, 23, 23, 23, 26, 26]
        self.x, self.y = 100, 125
        # mario is only once created, so instance image loading is fine
        self.image = load_image('mario.png')
        self.font = load_font('ENCR10B.TTF',16)
        self.dir = 0
        self.velocity = RUN_SPEED_PPS
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        self.jump_cnt = 0
        self.dash_mult = 0.0
        self.heading = 1
        self.cur_state_int = 1

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            try:
                print('cur state:', self.cur_state.__name__, 'event: ', event_name[event])
                print(self.dir)
                self.cur_state = next_state_table[self.cur_state][event]
            except:
                print('cur state:' , self.cur_state.__name__,'event: ',event_name[event])
                exit(-1)
            self.cur_state.enter(self, event)
        if 610 > self.x and self.x > 590:
            self.x = 600

        for tile in server.ground_tiles:
            if 610 > self.x and self.x > 590:
                tile.x -= self.velocity * self.dash_mult * game_framework.frame_time
                if collision.collide_M(server.mario, tile, 0):
                    for tile1 in server.ground_tiles:
                        tile1.x += self.velocity * self.dash_mult * game_framework.frame_time

        for tile in server.ground_tiles.copy():
            if self.x - 100 < tile.x and tile.x < self.x + 100:
                if collision.collide_M(server.mario, tile, 1):
                    if self.cur_state_int == server.FallingState:
                        self.add_event(Landing)
                        self.y = tile.y + 40 + 50 + (tile.tile_num - 1) * 80 - 1
                if self.x - 25 < tile.x and tile.x < self.x + 25:
                    if self.cur_state_int != server.FallingState and self.cur_state_int != server.JumpState:
                        if collision.collide_M(server.mario, tile, 1) == False:
                            self.add_event(DOWN)

    def draw(self):
        self.cur_state.draw(self)
        self.font.draw(self.x - 60, self.y + 50, '(Time: %3.2f)'% get_time(),(255,255,0))
        draw_rectangle(*self.get_bb_body())
        draw_rectangle(*self.get_bb_foot())

        if self.dash_mult != 0 and self.cur_state == IdleState:
            if self.dash_mult > 0:
                self.dash_mult -= 4.0 * game_framework.frame_time
            elif self.dash_mult < 0:
                self.dash_mult += 4.0 * game_framework.frame_time

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def get_bb_body(self):
        return self.x - 27, self.y - 30, self.x + 27, self.y + 50

    def get_bb_foot(self):
        return self.x - 20, self.y - 50, self.x + 20, self.y - 30