import game_framework
from pico2d import *
import game_world
import server
import collision

PIXEL_PER_METER = (100.0 / 1.5)

GRAVITY = 80 * PIXEL_PER_METER

RUN_SPEED_KMPH = 8.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.75
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = [0, 15, 15, 3]

class Green_turtle:
    image = None
    def __init__(self, n):
        if Green_turtle.image == None:
            Green_turtle.image = load_image('green_turtle.png')
        self.size = 20, 20
        self.size_on_canvas = 60  # 가로세로 약 0.9m
        self.x = server.ground_tiles[n].x
        self.y = server.ground_tiles[n].top_y + 45
        self.dir = -1
        self.frame = 0
        self.action = 1
        self.death = 0
        self.shell = 0
        self.death_cnt = 0
        self.floor = 0
        self.active = 0
        self.gravity_cnt = 0
        self.font = load_font('ENCR10B.TTF',16)

    def update(self):
        if 610 > server.mario.x and server.mario.x > 590:
            self.x -= server.mario.velocity * server.mario.dash_mult * game_framework.frame_time

        if self.y < 0:
            game_world.remove_object(self)

        if self.active == 0:
            if  0 < self.x and self.x < 1200:
                self.active = 1

        elif self.active == 1:
            if self.death == 1:
                self.action = 3
                if self.shell != 1:
                    if self.frame > 0:
                        self.frame = 0
            elif self.dir == -1 and self.death == 0:
                self.action = 1
            elif self.dir == 1 and self.death == 0:
                self.action = 2

            self.frame = (self.frame + (FRAMES_PER_ACTION[self.action] + self.shell * 10) * ACTION_PER_TIME * game_framework.frame_time) % \
                         FRAMES_PER_ACTION[self.action]

            if self.shell == 1:
                self.x += self.dir * 5 * RUN_SPEED_PPS * game_framework.frame_time

            if self.death == 0:
                self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time
                if server.mario.cur_state_int == server.FallingState:
                    if collision.collide_M(server.mario, self, 1):
                        self.death = 1
                        self.frame = 0
                        server.mario.jump_cnt = server.mario.jump_cnt / 2
                        server.mario.add_event(server.UP)
                else:
                    pass

            elif self.death == 1 and self.shell == 0:
                if collision.collide_M(server.mario, self, 1):
                    self.shell = 1
                    if server.mario.x > self.x:
                        self.dir = -1
                    else:
                        self.dir = 1

            for tile in server.ground_tiles:
                if tile.top_y >= self.y:
                    if self.x - 25 < tile.x and tile.x < self.x + 25:
                        if collision.collide(tile, self):
                            if self.dir == 1:
                                self.dir = -1
                            elif self.dir == -1:
                                self.dir = 1

                if tile.x - 20 < self.x and self.x < tile.x + 20:
                    self.floor = tile.top_y
                    if self.floor == 0:
                        self.floor = -100

            self.y -= GRAVITY * self.gravity_cnt * game_framework.frame_time
            self.gravity_cnt += game_framework.frame_time
            if self.y < self.floor + 45:
                self.y = self.floor + 45
                self.gravity_cnt = 0

    def draw(self):
        if -100 < self.x and self.x < 1300:
            self.image.clip_draw(int(self.frame) * 20, 93 - 31 * self.action, 20, 31, self.x, self.y, 60, 93)
            self.font.draw(self.x - 60, self.y + 50, '(DIR: %d , Action: %d)' % (self.dir,self.action) , (255, 255, 0))
            draw_rectangle(*self.get_bb())

    def get_bb_body(self):
        if self.death == 0:
            return self.x - 30, self.y - 46, self.x + 30, self.y + 46
        elif self.death == 1 or self.shell == 1:
            return self.x - 30, self.y - 46, self.x + 30, self.y

    def get_bb_foot(self):
        return self.x - 20, self.y - 50, self.x + 20, self.y - 30

    def get_bb(self):
        if self.death == 0:
            return self.x - 30, self.y - 46, self.x + 30, self.y + 46
        elif self.death < 0 or self.shell == 1:
            return self.x - 30, self.y - 46, self.x + 30, self.y