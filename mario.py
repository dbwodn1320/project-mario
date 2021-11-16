import game_framework
from pico2d import *
import game_world
import time
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
        if event == RIGHT_DOWN:
            mario.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            mario.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            mario.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            mario.velocity += RUN_SPEED_PPS

    def exit(mario, event):
        print('idle')

    def do(mario):
        if mario.dir == 1:
            mario.action = 1
        else:
            mario.action = 2
        mario.frame = (mario.frame + FRAMES_PER_ACTION[mario.action] * ACTION_PER_TIME * game_framework.frame_time) % mario.action_frame[mario.action]

    def draw(mario):
        if mario.dir == 1:
            mario.image.clip_draw(int(mario.frame) * 20, 656 - 40 * mario.action, 20, 40, mario.x, mario.y,60,120)
        else:
            mario.image.clip_draw(int(mario.frame) * 20, 656 - 40 * mario.action, 20, 40, mario.x, mario.y,60,120)

class RunState:
    def enter(mario, event):
        if event == RIGHT_DOWN:
            mario.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            mario.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            mario.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            mario.velocity += RUN_SPEED_PPS

        mario.dir = clamp(-1,mario.velocity, 1)

    def exit(mario, event):
        print('run')

    def do(mario):
        if mario.dir == 1:
            mario.action = 3
            mario.frame = (mario.frame + FRAMES_PER_ACTION[mario.action]  * ACTION_PER_TIME * game_framework.frame_time) % \
                          mario.action_frame[mario.action]
        else:
            mario.action = 4
            mario.frame = abs((mario.frame - FRAMES_PER_ACTION[mario.action]  * ACTION_PER_TIME * game_framework.frame_time) % \
                          mario.action_frame[mario.action])

        mario.x += mario.velocity * game_framework.frame_time

    def draw(mario):
        if mario.dir == 1:
            mario.image.clip_draw(int(mario.frame) * 30, 656 - 40 * mario.action, 30, 40, mario.x, mario.y,90,120)
        else:
            mario.image.clip_draw(int(mario.frame) * 30, 656 - 40 * mario.action, 30, 40, mario.x, mario.y,90,120)

class DashState:
    def enter(mario, event):
        if event == RIGHT_DOWN:
            mario.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            mario.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            mario.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            mario.velocity += RUN_SPEED_PPS

    def exit(mario, event):
        print('XXXXdash')

    def do(mario):
        if mario.dir == 1:
            mario.action = 7
            mario.frame = (mario.frame + FRAMES_PER_ACTION[mario.action]  * ACTION_PER_TIME * game_framework.frame_time) % \
                          mario.action_frame[mario.action]
        else:
            mario.action = 8
            mario.frame = (mario.frame + FRAMES_PER_ACTION[mario.action]  * ACTION_PER_TIME * game_framework.frame_time) % \
                          mario.action_frame[mario.action]

        mario.x += mario.velocity * 3 * game_framework.frame_time

    def draw(mario):
        if mario.dir == 1:
            mario.image.clip_draw(int(mario.frame) * 30, 656 - 40 * mario.action, 30, 40, mario.x, mario.y,90,120)
        else:
            mario.image.clip_draw(int(mario.frame) * 30, 656 - 40 * mario.action, 30, 40, mario.x, mario.y,90,120)

class JumpState:
    def enter(mario, event):
        if event == RIGHT_DOWN:
            mario.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            mario.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            mario.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            mario.velocity += RUN_SPEED_PPS

        mario.dir = clamp(-1, mario.velocity, 1)

    def exit(mario, event):
        print('falling')

    def do(mario):
        if mario.dir == 1:
            mario.action = 5
            mario.frame = (mario.frame + FRAMES_PER_ACTION[mario.action] * ACTION_PER_TIME * game_framework.frame_time) % \
                          mario.action_frame[mario.action]
        else:
            mario.action = 6
            mario.frame = (mario.frame + FRAMES_PER_ACTION[mario.action] * ACTION_PER_TIME * game_framework.frame_time) % \
                          mario.action_frame[mario.action]

        if mario.jump_cnt == 0:  mario.frame = 0
        mario.x += mario.velocity * game_framework.frame_time
        mario.y += (MARIO_JUMP - mario.jump_cnt * GRAVITY) * game_framework.frame_time
        mario.jump_cnt += game_framework.frame_time
        if MARIO_JUMP - mario.jump_cnt * GRAVITY < 0:
            mario.add_event(DOWN)

    def draw(mario):
        if mario.dir == 1:
            mario.image.clip_draw(int(mario.frame) * 30, 656 - 40 * mario.action, 30, 40, mario.x, mario.y,90,120)
        else:
            mario.image.clip_draw(int(mario.frame) * 30, 656 - 40 * mario.action, 30, 40, mario.x, mario.y,90,120)

class FallingState:
    def enter(mario, event):
        if event == RIGHT_DOWN:
            mario.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            mario.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            mario.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            mario.velocity += RUN_SPEED_PPS

        mario.dir = clamp(-1, mario.velocity, 1)

    def exit(mario, event):
        print('falling')

    def do(mario):
        if mario.dir == 1:
            mario.action = 5
            mario.frame = (mario.frame + FRAMES_PER_ACTION[mario.action] * ACTION_PER_TIME * game_framework.frame_time) % \
                          mario.action_frame[mario.action]
        else:
            mario.action = 6
            mario.frame = (mario.frame + FRAMES_PER_ACTION[mario.action] * ACTION_PER_TIME * game_framework.frame_time) % \
                          mario.action_frame[mario.action]

        if mario.jump_cnt == 0:  mario.frame = 0
        mario.x += mario.velocity * game_framework.frame_time
        mario.y += (MARIO_JUMP - mario.jump_cnt * GRAVITY) * game_framework.frame_time
        mario.jump_cnt += game_framework.frame_time
        if mario.y < 90:
            mario.add_event(Landing)
            mario.y = 90

    def draw(mario):
        if mario.dir == 1:
            mario.image.clip_draw(int(mario.frame) * 30, 656 - 40 * mario.action, 30, 40, mario.x, mario.y,90,120)
        else:
            mario.image.clip_draw(int(mario.frame) * 30, 656 - 40 * mario.action, 30, 40, mario.x, mario.y,90,120)

    class DashState:
        def enter(mario, event):
            pass

        def exit(mario, event):
            print('XXXXdash')

        def do(mario):
            if mario.dir == 1:
                mario.action = 7
                mario.frame = (mario.frame + FRAMES_PER_ACTION[
                    mario.action] * ACTION_PER_TIME * game_framework.frame_time) % \
                              mario.action_frame[mario.action]
            else:
                mario.action = 8
                mario.frame = (mario.frame + FRAMES_PER_ACTION[
                    mario.action] * ACTION_PER_TIME * game_framework.frame_time) % \
                              mario.action_frame[mario.action]

            mario.x += mario.velocity * 3 * game_framework.frame_time

        def draw(mario):
            if mario.dir == 1:
                mario.image.clip_draw(int(mario.frame) * 30, 656 - 40 * mario.action, 30, 40, mario.x, mario.y, 90, 120)
            else:
                mario.image.clip_draw(int(mario.frame) * 30, 656 - 40 * mario.action, 30, 40, mario.x, mario.y, 90, 120)

class LandingState:
    def enter(mario, event):
        pass

    def exit(mario, event):
        pass

    def do(mario):
        pass
    
    def draw(mario):
        if mario.dir == 1:
            mario.image.clip_draw(int(mario.frame) * 30, 656 - 40 * mario.action, 30, 40, mario.x, mario.y,90,120)
        else:
            mario.image.clip_draw(int(mario.frame) * 30, 656 - 40 * mario.action, 30, 40, mario.x, mario.y,90,120)

next_state_table = {
    DashState: {SHIFT_UP:RunState,LEFT_UP:IdleState,LEFT_DOWN:IdleState,RIGHT_UP:IdleState,RIGHT_DOWN:IdleState, SPACE:DashState, UP:JumpState},

    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState,
                SHIFT_UP: IdleState,SHIFT_DOWN:IdleState,SPACE: IdleState,UP:JumpState, DOWN:IdleState},

    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
               SHIFT_DOWN:DashState,SHIFT_UP:RunState,SPACE: RunState, UP:JumpState, DOWN:RunState},

    JumpState: {RIGHT_UP: JumpState, LEFT_UP: JumpState, LEFT_DOWN: JumpState, RIGHT_DOWN: JumpState,
               SHIFT_DOWN:JumpState,SHIFT_UP:JumpState,SPACE: JumpState,UP:JumpState,DOWN:FallingState,Landing: IdleState},

    FallingState: { RIGHT_UP: FallingState, LEFT_UP: FallingState, LEFT_DOWN: FallingState, RIGHT_DOWN: FallingState,
               SHIFT_DOWN:FallingState,SHIFT_UP:FallingState,SPACE: FallingState, UP:FallingState,Landing: IdleState}
}

class Mario:
    def __init__(self):
        self.acrion = 1
        self.action_frame = [0, 22, 22, 23, 23, 23, 23, 26, 26]
        self.x, self.y = 1600 // 2, 90
        # mario is only once created, so instance image loading is fine
        self.image = load_image('mario.png')
        self.font = load_font('ENCR10B.TTF',16)
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        self.jump_cnt = 0

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            try:
                self.cur_state = next_state_table[self.cur_state][event]
                print('cur state:', self.cur_state.__name__, 'event: ', event_name[event])
            except:
                print('cur state:' , self.cur_state.__name__,'event: ',event_name[event])
                exit(-1)
            self.cur_state.enter(self, event)
    def draw(self):
        self.cur_state.draw(self)
        self.font.draw(self.x - 60, self.y +50, '(Time: %3.2f)'% get_time(),(255,255,0))

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)