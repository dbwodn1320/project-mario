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
FRAMES_PER_ACTION = [0, 15, 15, 1]

class Green_turtle:
    image = None
    def __init__(self, pt):
        if Green_turtle.image == None:
            Green_turtle.image = load_image('green_turtle_edit.png')
        self.size = 20, 20
        self.size_on_canvas = 60  # 가로세로 약 0.9m
        self.x = pt[0]
        self.y = pt[1]
        self.dir = -1
        self.frame = 0
        self.action = 1
        self.death = 0
        self.death_cnt = 0

    def update(self):
        if self.death == 1:
            self.action = 3
            if self.frame > 0:
                self.frame = 0
            self.death_cnt += game_framework.frame_time
        elif self.dir == -1:
            self.action = 1
        elif self.dir == 1:
            self.action = 2

        self.frame = (self.frame + FRAMES_PER_ACTION[self.action] * ACTION_PER_TIME * game_framework.frame_time) % \
                     FRAMES_PER_ACTION[self.action]

        if 610 > server.mario.x and server.mario.x > 590:
            server.green_trutle.x -= server.mario.velocity * server.mario.dash_mult * game_framework.frame_time

        if self.death == 0:
            self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time
            if collision.collide_M(server.mario, server.green_trutle, 1):
                self.death = 1
                self.frame = 0
                server.mario.jump_cnt = server.mario.jump_cnt / 2
                server.mario.add_event(server.UP)
        if self.death_cnt > 1.0:
            game_world.remove_object(server.green_trutle)

    def draw(self):
        if -100 < self.x and self.x < 1300:
            if self.death == 0:
                self.image.clip_draw(int(self.frame) * 20, 93 - 31 * self.action, 20, 31, self.x, self.y, 60, 93)
            else:
                self.image.clip_draw(int(self.frame) * 20, 93 - 31 * self.action, 20, 31, self.x, self.y, 60, 93)

            draw_rectangle(*self.get_bb())
        print('aaaaaaaaaaaaaaaaa')

    def get_bb(self):
        return self.x - 30, self.y - 46, self.x + 30, self.y + 46
