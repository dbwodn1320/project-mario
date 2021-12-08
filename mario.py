import game_framework
from pico2d import *
import game_world
import time
import collision
import server

frame_time = 0.0

PIXEL_PER_METER = (100.0 / 1.5)
MARIO_JUMP = 25 * PIXEL_PER_METER
GRAVITY = 70 * PIXEL_PER_METER

RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.75
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = [0, 22, 22, 23, 23, 23, 25, 26, 26]
FRAMES_PER_ACTION_SMALL = [0,20,23,21,10,9]


DEBUG_KEY,RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SHIFT_DOWN, SHIFT_UP, DEATH, UP, DOWN, Landing = range(11)

event_name = ['DEBUG_KEY','RIGHT_DOWN', 'LEFT_DOWN', 'RIGHT_UP', 'LEFT_UP',\
'SHIFT_DOWN','SHIFT_UP','SPACE','UP','DOWN','Landing']

key_event_table = {
    #(SDL_KEYDOWN, SDLK_SPACE): SPACE,
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
        elif event == LEFT_DOWN:
            mario.dir -= 1
        elif event == RIGHT_UP:
            mario.dir -= 1
        elif event == LEFT_UP:
            mario.dir += 1
        elif event == DEBUG_KEY:
            mario.god = 1 - mario.god

        mario.dir = clamp(-1,mario.dir,1)

    def exit(mario, event):
        pass

    def do(mario):
        if mario.hp == 1:
            mario.frame = (mario.frame + FRAMES_PER_ACTION[1] * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION[1]
        elif mario.hp == 0:
            mario.frame = (mario.frame + FRAMES_PER_ACTION_SMALL[1] * ACTION_PER_TIME * game_framework.frame_time) % \
                          FRAMES_PER_ACTION_SMALL[1]
    def draw(mario):
        if mario.hp == 1:
            if mario.heading == 1:
                mario.image.clip_draw(int(mario.frame) * 20, 360 - 40 * 1, 20, 40, mario.x, mario.y, 60,120)
            else:
                mario.image.clip_draw(int(mario.frame) * 20, 360 - 40 * 2, 20, 40, mario.x, mario.y, 60,120)
        elif mario.hp == 0:
            if mario.heading == 1:
                mario.image_small.clip_draw(int(mario.frame) * 20, 125 - 25 * 1, 20, 25, mario.x, mario.y, 60,75)
            else:
                mario.image_small.clip_composite_draw(int(mario.frame) * 20, 125 - 25 * 1, 20, 25, 0,'h',mario.x, mario.y, 60,75)
class RunState:
    def enter(mario, event):
        mario.cur_state_int = 2
        mario.jump_cnt = 0
        mario.frame = 0
        if event == RIGHT_DOWN:
            mario.dir += 1
        elif event == LEFT_DOWN:
            mario.dir -= 1
        elif event == RIGHT_UP:
            mario.dir -= 1
        elif event == LEFT_UP:
            mario.dir += 1

        mario.dir = clamp(-1,mario.dir,1)

    def exit(mario, event):
        pass

    def do(mario):
        if mario.hp == 1:
            if mario.heading == 1:
                mario.action = 3
                mario.frame = (mario.frame + FRAMES_PER_ACTION[mario.action] * ACTION_PER_TIME * game_framework.frame_time) % \
                              FRAMES_PER_ACTION[mario.action]
            else:
                mario.action = 4
                mario.frame = abs((mario.frame - FRAMES_PER_ACTION[mario.action] * ACTION_PER_TIME * game_framework.frame_time) % \
                              FRAMES_PER_ACTION[mario.action])
        elif mario.hp == 0:
            mario.frame = (mario.frame + FRAMES_PER_ACTION_SMALL[2] * ACTION_PER_TIME * game_framework.frame_time) % \
                          FRAMES_PER_ACTION_SMALL[2]

        mario.x += mario.velocity * mario.dash_mult * game_framework.frame_time

        mario.dash_mult += mario.dir * 4.0 * game_framework.frame_time
        if -1.1 < mario.dash_mult < -1.0:
            mario.dash_mult = -1.0
        elif 1.1 > mario.dash_mult > 1.0:
            mario.dash_mult = 1.0

    def draw(mario):
        if mario.hp == 1:
            if mario.heading == 1:
                mario.image.clip_draw(int(mario.frame) * 30, 360 - 40 * 3, 30, 40, mario.x, mario.y, 90,120)
            else:
                mario.image.clip_draw(int(mario.frame) * 30, 360 - 40 * 4, 30, 40, mario.x, mario.y, 90,120)
        elif mario.hp <= 0:
            if mario.heading == 1:
                mario.image_small.clip_draw(int(mario.frame) * 20, 125 - 25 * 2, 20, 25, mario.x, mario.y, 60,75)
            else:
                mario.image_small.clip_composite_draw(int(mario.frame) * 20, 125 - 25 * 2, 20, 25, 0,'h',mario.x, mario.y, 60,75)


class DashState:
    def enter(mario, event):
        mario.cur_state_int = 0
        if event == RIGHT_DOWN:
            mario.dir += 1
        elif event == LEFT_DOWN:
            mario.dir -= 1
        elif event == RIGHT_UP:
            mario.dir -= 1
        elif event == LEFT_UP:
            mario.dir += 1
        mario.jump_cnt = 0
        mario.dash_timer = 0
        mario.dir = clamp(-1,mario.dir,1)

    def exit(mario, event):
        mario.dash_timer = 0

    def do(mario):
        if mario.hp == 1:
            if mario.heading == 1:
                mario.action = 7
                if mario.dash_timer > 17:
                    mario.frame = (mario.frame - 18 + FRAMES_PER_ACTION[mario.action] * ACTION_PER_TIME * game_framework.frame_time) % 8 + 18
                else:
                    mario.frame = (mario.frame + FRAMES_PER_ACTION[mario.action] * ACTION_PER_TIME * game_framework.frame_time) % \
                                  FRAMES_PER_ACTION[mario.action]
            else:
                mario.action = 8
                if mario.dash_timer > 17:
                    mario.frame = abs(
                        (mario.frame - FRAMES_PER_ACTION[mario.action] * ACTION_PER_TIME * game_framework.frame_time) % 8)
                else:
                    mario.frame = abs(
                        (mario.frame - FRAMES_PER_ACTION[mario.action] * ACTION_PER_TIME * game_framework.frame_time) % \
                        FRAMES_PER_ACTION[mario.action])
        elif mario.hp == 0:
            mario.frame = (mario.frame + 18 * ACTION_PER_TIME * game_framework.frame_time) % \
                          FRAMES_PER_ACTION_SMALL[4]


        mario.dash_timer += FRAMES_PER_ACTION[mario.action] * ACTION_PER_TIME * game_framework.frame_time
        mario.x += mario.velocity * mario.dash_mult * game_framework.frame_time
        mario.dash_mult += 6.0 * mario.dir * game_framework.frame_time

    def draw(mario):
        if mario.hp == 1:
            if mario.heading == 1:
                mario.image.clip_draw(int(mario.frame) * 30, 360 - 40 * 7, 30, 40, mario.x, mario.y, 90, 120)
            else:
                mario.image.clip_draw(int(mario.frame) * 30, 360 - 40 * 8, 30, 40, mario.x, mario.y, 90, 120)
        elif mario.hp <= 0:
            if mario.heading == 1:
                mario.image_small.clip_draw(int(mario.frame) * 20, 125 - 25 * 4, 20, 25, mario.x, mario.y, 60, 75)
            else:
                mario.image_small.clip_composite_draw(int(mario.frame) * 20, 125 - 25 * 4, 20, 25, 0, 'h', mario.x,
                                                      mario.y, 60, 75)

class JumpState:
    def enter(mario, event):
        mario.frame = 0
        mario.cur_state_int = 3
        if event == RIGHT_DOWN:
            mario.dir += 1
        elif event == LEFT_DOWN:
            mario.dir -= 1
        elif event == RIGHT_UP:
            mario.dir -= 1
        elif event == LEFT_UP:
            mario.dir += 1

        mario.dir = clamp(-1,mario.dir,1)

    def exit(mario, event):
        pass

    def do(mario):
        if mario.hp == 1:
            if mario.heading == 1:
                mario.action = 5
            else:
                mario.action = 6
            mario.frame = (mario.frame + 18 * ACTION_PER_TIME * game_framework.frame_time) % \
                          FRAMES_PER_ACTION[mario.action]
        elif mario.hp <= 0:
            mario.frame = (mario.frame + FRAMES_PER_ACTION_SMALL[3] * ACTION_PER_TIME * game_framework.frame_time) % \
                          FRAMES_PER_ACTION_SMALL[3]

        mario.x += mario.velocity * mario.dash_mult * game_framework.frame_time
        mario.dash_mult += mario.dir * 4.0 * game_framework.frame_time
        if -1.1 < mario.dash_mult < -1.0:
            mario.dash_mult = -1.0
        elif 1.1 > mario.dash_mult > 1.0:
            mario.dash_mult = 1.0

        mario.y += (MARIO_JUMP - mario.jump_cnt * GRAVITY) * game_framework.frame_time
        mario.jump_cnt += game_framework.frame_time
        if MARIO_JUMP - mario.jump_cnt * GRAVITY < 0:
            mario.add_event(DOWN)
            mario.jump_cnt = 0

    def draw(mario):
        if mario.hp == 1:
            if mario.heading == 1:
                mario.image.clip_draw(int(mario.frame) * 30, 360 - 40 * 5, 30, 40, mario.x, mario.y, 90, 120)
            else:
                mario.image.clip_draw(int(mario.frame) * 30, 360 - 40 * 6, 30, 40, mario.x, mario.y, 90, 120)
        elif mario.hp <= 0:
            if mario.heading == 1:
                mario.image_small.clip_draw(int(mario.frame) * 20, 125 - 25 * 3, 20, 25, mario.x, mario.y, 60, 75)
            else:
                mario.image_small.clip_composite_draw(int(mario.frame) * 20, 125 - 25 * 3, 20, 25, 0, 'h', mario.x,
                                                      mario.y, 60, 75)

class FallingState:
    def enter(mario, event):
        mario.cur_state_int = 4
        if event == RIGHT_DOWN:
            mario.dir += 1
        elif event == LEFT_DOWN:
            mario.dir -= 1
        elif event == RIGHT_UP:
            mario.dir -= 1
        elif event == LEFT_UP:
            mario.dir += 1

        mario.dir = clamp(-1,mario.dir,1)

    def exit(mario, event):
        pass

    def do(mario):
        if mario.hp == 1:
            if mario.heading == 1:
                mario.action = 5
            else:
                mario.action = 6
            mario.frame = (mario.frame + 15 * ACTION_PER_TIME * game_framework.frame_time) % \
                          FRAMES_PER_ACTION[mario.action]

        elif mario.hp < 0:
            mario.frame = (mario.frame + FRAMES_PER_ACTION_SMALL[3] * ACTION_PER_TIME * game_framework.frame_time) % \
                          FRAMES_PER_ACTION_SMALL[3]

        mario.x += mario.velocity * mario.dash_mult * game_framework.frame_time
        mario.dash_mult += mario.dir * 4.0 * game_framework.frame_time
        if -1.1 < mario.dash_mult < -1.0:
            mario.dash_mult = -1.0
        elif 1.1 > mario.dash_mult > 1.0:
            mario.dash_mult = 1.0

        mario.y += -mario.jump_cnt * GRAVITY * game_framework.frame_time
        mario.jump_cnt += game_framework.frame_time

    def draw(mario):
        if mario.hp == 1:
            if mario.heading == 1:
                mario.image.clip_draw(int(mario.frame) * 30, 360 - 40 * 5, 30, 40, mario.x, mario.y, 90, 120)
            else:
                mario.image.clip_draw(int(mario.frame) * 30, 360 - 40 * 6, 30, 40, mario.x, mario.y, 90, 120)
        elif mario.hp <= 0:
            if mario.heading == 1:
                mario.image_small.clip_draw(int(mario.frame) * 20, 125 - 25 * 3, 20, 25, mario.x, mario.y, 60, 75)
            else:
                mario.image_small.clip_composite_draw(int(mario.frame) * 20, 125 - 25 * 3, 20, 25, 0, 'h', mario.x,
                                                      mario.y, 60, 75)

class DeathState:
    def enter(mario, event):
        mario.cur_state_int = 5
        server.mario.image.opacify(1)
        server.mario.image_small.opacify(1)

    def exit(mario, event):
        pass

    def do(mario):
        if mario.hp == 1:
            mario.frame = (mario.frame + 20 * ACTION_PER_TIME * game_framework.frame_time) % 13
        elif mario.hp <= 0:
            mario.frame = (mario.frame + 9 * ACTION_PER_TIME * game_framework.frame_time) % 9

        #print(mario.frame)
        mario.y += (MARIO_JUMP - mario.jump_cnt * GRAVITY) * game_framework.frame_time
        mario.jump_cnt += game_framework.frame_time
        if mario.y < -50:
            mario.death = 1

    def draw(mario):
        if mario.hp == 1:
            mario.image.clip_draw(int(mario.frame) * 40, 360 - 40 * 9, 40, 40, mario.x, mario.y, 120, 120)
        elif mario.hp <= 0:
            mario.image_small.clip_draw(int(mario.frame) * 20, 125 - 25 * 5, 20, 25, mario.x, mario.y, 60, 75)

next_state_table = {
    DashState: {SHIFT_UP:RunState,SHIFT_DOWN:DashState,LEFT_UP:IdleState,LEFT_DOWN:IdleState,
                RIGHT_UP:IdleState,RIGHT_DOWN:IdleState, DEATH: DeathState,UP: JumpState,DOWN: FallingState},

    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState,
                SHIFT_UP: IdleState,SHIFT_DOWN:IdleState,DEATH: DeathState,UP:JumpState, DOWN:FallingState,Landing:IdleState},

    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
               SHIFT_DOWN:DashState,SHIFT_UP:RunState,DEATH: DeathState, UP:JumpState, DOWN:FallingState, Landing:RunState},

    JumpState: {RIGHT_UP: JumpState, LEFT_UP: JumpState, LEFT_DOWN: JumpState, RIGHT_DOWN: JumpState,
               SHIFT_DOWN:JumpState,SHIFT_UP:JumpState,DEATH: DeathState,UP:JumpState,DOWN:FallingState,Landing: JumpState},

    FallingState: { RIGHT_UP: FallingState, LEFT_UP: FallingState, LEFT_DOWN: FallingState, RIGHT_DOWN: FallingState,
               SHIFT_DOWN:FallingState,SHIFT_UP:FallingState,DEATH: DeathState, UP:JumpState,Landing: RunState},

    DeathState: { RIGHT_UP: DeathState, LEFT_UP: DeathState, LEFT_DOWN: DeathState, RIGHT_DOWN: DeathState,
       SHIFT_DOWN: DeathState, SHIFT_UP: DeathState, DEATH: DeathState, UP: DeathState, DOWN:DeathState}
}

class Mario:
    def __init__(self):
        self.action = 1
        self.action_frame = [0, 22, 22, 23, 23, 23, 23, 26, 26]
        self.x, self.y = 100, 120
        # mario is only once created, so instance image loading is fine
        self.image = load_image('mario.png')
        self.image_small = load_image('mario_small.png')
        self.font = load_font('SuperMario256.ttf',50)
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
        self.run = 0

        self.timestop = 0
        self.hp = 0
        self.death = 0
        self.ghost = 0
        self.ghost_cnt = 0

        self.first_cmd = 0
        self.keydown_shift = 0

        if server.map_kind == 2:
            self.y += 60

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            try:
                print('cur state:', self.cur_state.__name__, 'event: ', event_name[event])
                print(MARIO_JUMP - self.jump_cnt * GRAVITY)
                if self.cur_state == DeathState:
                    self.cur_state = DeathState
                elif self.cur_state == FallingState and event == Landing:
                    if self.keydown_shift == 1:
                        self.cur_state = DashState
                    elif abs(self.dir) > 0:
                        self.cur_state = RunState
                    elif self.dir == 0:
                        self.cur_state = IdleState
                elif self.keydown_shift == 1 and (event != UP and event !=DOWN) and self.cur_state != FallingState and self.cur_state != JumpState:
                    self.cur_state = DashState
                else:
                    self.cur_state = next_state_table[self.cur_state][event]
                #print('cur state:', self.cur_state.__name__, 'event: ', event_name[event])
            except:
                print('cur state:' , self.cur_state.__name__,'event: ',event_name[event])
                exit(-1)
            self.cur_state.enter(self, event)

        # 마리오 죽음
        if self.cur_state != DeathState:
            if self.y < - 50:
                self.add_event(DEATH)
                self.jump_cnt = 0
                self.timestop = 1
            if self.hp < 0:
                self.add_event(DEATH)
                self.jump_cnt = 0
                self.timestop = 1

        # 마리오 바라보는 방향 설정
        if self.dir > 0:
            self.heading = 1
        elif self.dir < 0:
            self.heading = -1

        self.x = clamp(0,self.x,900)
        # 스크롤링 및 충돌체크
        if 450 + 20 > self.x > 450 - 20 and not server.ground_tiles[0].x < self.x < server.ground_tiles[0 + 7].x \
                and not server.ground_tiles[server.map_len - 8].x < self.x < server.ground_tiles[server.map_len - 1].x:
            self.x = 450
            for i in range(len(server.background.x1)):
                server.background.x1[i] -= 0.25 *self.velocity * self.dash_mult * game_framework.frame_time
                if server.background.x1[i] < -1350:
                    for j in range(len(server.background.x1)):
                        if 430 < server.background.x1[j] < 450:
                            server.background.x1[i] = server.background.x1[j] + 900
                            break
                elif server.background.x1[i] > 2150:
                    for j in range(len(server.background.x1)):
                        if 430 < server.background.x1[j] < 450:
                            server.background.x1[i] = server.background.x1[j] - 900
                            break
            for i in range(len(server.background.x2)):
                server.background.x2[i] -= 0.5 * self.velocity * self.dash_mult * game_framework.frame_time
                if server.background.x2[i] < -1350:
                    for j in range(len(server.background.x2)):
                        if 430 < server.background.x2[j] < 450:
                            server.background.x2[i] = server.background.x2[j] + 900
                            break
                elif server.background.x2[i] > 2150:
                    for j in range(len(server.background.x2)):
                        if 430 < server.background.x2[j] < 450:
                            server.background.x2[i] = server.background.x2[j] - 900
                            break
            for coin in server.coins:
                coin.x -= self.velocity * self.dash_mult * game_framework.frame_time
            for block in server.blocks:
                block.x -= self.velocity * self.dash_mult * game_framework.frame_time
            for tile in server.ground_tiles:
                tile.x -= self.velocity * self.dash_mult * game_framework.frame_time
            for turtle in server.green_trutles:
                turtle.x -= self.velocity * self.dash_mult * game_framework.frame_time
            for goomba in server.goombas:
                goomba.x -= self.velocity * self.dash_mult * game_framework.frame_time
            if len(server.mushrooms) > 0:
                for mush in server.mushrooms:
                    mush.x -= self.velocity * self.dash_mult * game_framework.frame_time
            for tile in server.ground_tiles:
                if collision.collide(server.mario, tile):
                    for tile1 in server.ground_tiles:
                        tile1.x += self.velocity * self.dash_mult * game_framework.frame_time
                    for coin in server.coins:
                        coin.x += self.velocity * self.dash_mult * game_framework.frame_time
                    for turtle in server.green_trutles:
                        turtle.x += self.velocity * self.dash_mult * game_framework.frame_time
                    for goomba in server.goombas:
                        goomba.x += self.velocity * self.dash_mult * game_framework.frame_time
                    for block in server.blocks:
                        block.x += self.velocity * self.dash_mult * game_framework.frame_time
                    for i in range(len(server.background.x1)):
                        server.background.x1[i] += 0.25 * self.velocity * self.dash_mult * game_framework.frame_time
                        server.background.x2[i] += 0.5 * self.velocity * self.dash_mult * game_framework.frame_time
                    if len(server.mushrooms) > 0:
                        for mush in server.mushrooms:
                            mush.x += self.velocity * self.dash_mult * game_framework.frame_time
                    break
            for block in server.blocks:
                if collision.collide(server.mario, block):
                    for tile in server.ground_tiles:
                        tile.x += self.velocity * self.dash_mult * game_framework.frame_time
                    for coin in server.coins:
                        coin.x += self.velocity * self.dash_mult * game_framework.frame_time
                    for turtle in server.green_trutles:
                        turtle.x += self.velocity * self.dash_mult * game_framework.frame_time
                    for goomba in server.goombas:
                        goomba.x += self.velocity * self.dash_mult * game_framework.frame_time
                    for block1 in server.blocks:
                        block1.x += self.velocity * self.dash_mult * game_framework.frame_time
                    for i in range(len(server.background.x1)):
                        server.background.x1[i] += 0.25 * self.velocity * self.dash_mult * game_framework.frame_time
                        server.background.x2[i] += 0.5 * self.velocity * self.dash_mult * game_framework.frame_time
                    if len(server.mushrooms) > 0:
                        for mush in server.mushrooms:
                            mush.x += self.velocity * self.dash_mult * game_framework.frame_time
                    break

        # 몬스터 충돌체크
        #print(self.ghost)
        for turtle in server.green_trutles:
            if collision.collide_M(self,turtle,0):
                if (turtle.death == 0 or (turtle.shell == 1 and turtle.shell1_cnt > 0.2)) and not self.ghost == 1:
                    if self.hp == 1:
                        self.timestop = 1
                        self.y -= 10
                    self.hp -= 1
                break
        for goomba in server.goombas:
            if collision.collide_M(self, goomba, 0) and not self.ghost == 1:
                if goomba.death == 0:
                    if self.hp == 1:
                        self.timestop = 1
                        self.y -= 10
                    self.hp -= 1
                break

        if self.ghost == 1 and self.cur_state != DeathState:
            self.ghost_cnt += game_framework.frame_time
            self.image.opacify(self.ghost_cnt)
            self.image_small.opacify(self.ghost_cnt)
            if self.ghost_cnt > 1.0:
                self.ghost_cnt = 0
                self.ghost = 0
                self.image.opacify(1)
                self.image_small.opacify(1)

        # 마리오 착지
        if self.cur_state_int == server.FallingState:
            for block in server.blocks:
                if self.x - 100 < block.x and block.x < self.x + 100:
                    if collision.collide_M(server.mario, block, 1) and block.y + 30 < self.y - 30:
                        self.add_event(Landing)
                        if self.hp == 0:
                            self.y = block.y + 30 + 40
                            pass
                        elif self.hp == 1:
                            self.y = block.y + 30 + 49.9
                        break
            for tile in server.ground_tiles:
                if self.x - 100 < tile.x and tile.x < self.x + 100:
                    if collision.collide_M(server.mario, tile, 1) and tile.tile_num != 0:
                        self.add_event(Landing)
                        if self.hp == 0:
                            self.y = tile.top_y + 40
                            pass
                        elif self.hp == 1:
                            self.y = tile.top_y + 49.9
                        break
        # 마리오 낙하
        elif self.cur_state_int != server.JumpState and self.cur_state_int != server.FallingState:
            a = 0
            for block in server.blocks:
                if not collision.collide_M(server.mario, block, 1):
                    a += 1
            for tile in server.ground_tiles:
                if not collision.collide_M(server.mario, tile, 1):
                    a += 1
            if a == len(server.ground_tiles) + len(server.blocks):
                server.mario.add_event(DOWN)

        # 감속
        if self.dash_mult != 0:
            if self.cur_state == IdleState:
                if -1.0 <= self.dash_mult <= 1:
                    if self.dash_mult > 0:
                        self.dash_mult -= 4.0 * game_framework.frame_time
                    elif self.dash_mult < 0:
                        self.dash_mult += 4.0 * game_framework.frame_time
                elif abs(self.dash_mult) > 1:
                    if self.dash_mult > 0:
                        self.dash_mult -= 12.0 * game_framework.frame_time
                    elif self.dash_mult < 0:
                        self.dash_mult += 12.0 * game_framework.frame_time
            elif (self.cur_state == JumpState or self.cur_state == FallingState) and abs(self.dash_mult) > 1.09 and self.keydown_shift == 1:
                if self.dash_mult > 0:
                    self.dash_mult -= 3.0 * game_framework.frame_time
                elif self.dash_mult < 0:
                    self.dash_mult += 3.0 * game_framework.frame_time
            elif self.cur_state != DashState and abs(self.dash_mult) > 1.09:
                if self.dash_mult > 0:
                    self.dash_mult -= 9.0 * game_framework.frame_time
                elif self.dash_mult < 0:
                    self.dash_mult += 9.0 * game_framework.frame_time

        if self.dash_mult < -2.5:
            self.dash_mult = -2.5
        elif self.dash_mult > 2.5:
            self.dash_mult = 2.5

        if -0.05 < self.dash_mult < -0.05:
            self.dash_mult = 0

    def draw(self):
        self.cur_state.draw(self)
        #self.font.draw(self.x - 60, self.y + 80, '(HP: %d)' % self.hp,(255,255,255))
        #draw_rectangle(*self.get_bb_body())
        #draw_rectangle(*self.get_bb_foot())
        #draw_rectangle(*self.get_bb_head())
        #draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            if not self.cur_state == FallingState or not event.key == SDLK_UP:
                if not(self.first_cmd == 0 and event.type == SDL_KEYUP and (event.key == SDLK_LEFT or event.key == SDLK_RIGHT)):
                    key_event = key_event_table[(event.type, event.key)]
                    self.add_event(key_event)
                    if event.type == SDL_KEYUP and (event.key == SDLK_LSHIFT or event.key == SDLK_RSHIFT):
                        self.keydown_shift = 0
                    elif event.type == SDL_KEYDOWN and (event.key == SDLK_LSHIFT or event.key == SDLK_RSHIFT):
                        self.keydown_shift = 1

            #print(self.keydown_shift)
            self.first_cmd += 1

    def get_bb(self):
        if self.hp == 1:
            return self.x - 27, self.y - 30, self.x + 27, self.y + 50
        elif self.hp <= 0:
            return self.x - 21, self.y - 20, self.x + 25, self.y + 15

    def get_bb_body(self):
        if self.hp == 1:
            return self.x - 20, self.y - 30, self.x + 20, self.y + 30
        elif self.hp <= 0:
            #return self.x - 15, self.y - 20, self.x + 15, self.y + 20
            return self.x - 15, self.y + 9999, self.x + 15, self.y + 99999
    def get_bb_foot(self):
        if self.hp == 1:
            return self.x - 27, self.y - 50, self.x + 27, self.y - 30
        elif self.hp <= 0:
            return self.x - 21, self.y - 40, self.x + 25, self.y - 20
    def get_bb_head(self):
        if self.hp == 1:
            return self.x - 20, self.y + 30, self.x + 20, self.y + 50
        elif self.hp <= 0:
            return self.x - 15, self.y + 20, self.x + 15, self.y + 37