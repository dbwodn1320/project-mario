from pico2d import *
import game_framework
from pico2d import *
import game_world
import time

PIXEL_PER_METER = (100.0 / 1.5)

GRAVITY = 80 * PIXEL_PER_METER

RUN_SPEED_KMPH = 8.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.75
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = [0, 9, 9, 2]

class Goomba:
    image = None
    def __init__(self, pt):
        if Goomba.image == None:
            Goomba.image = load_image('goomba.png')
        self.size = 20, 20
        self.size_on_canvas = 60 # 가로세로 약 0.9m
        self.x = pt[0]
        self.y = pt[1]
        self.dir = -1
        self.frame = 0
        self.action_frame = [0,9,9,2]
        self.action = 1
        self.death = 0
        self.death_cnt = 0

    def update(self):
        if self.death == 1:
            self.action = 3
            if self.frame > 1:
                self.frame = 1
            self.death_cnt += game_framework.frame_time
        elif self.dir == -1:    self.action = 1
        elif self.dir == 1: self.action = 2

        self.frame = (self.frame + FRAMES_PER_ACTION[self.action] * ACTION_PER_TIME * game_framework.frame_time) % \
                      self.action_frame[self.action]
        if self.death == 0:
            self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time

    def draw(self):
        if -100 < self.x and self.x < 1300 :
            if self.death == 0:
                self.image.clip_draw(int(self.frame) * 20, 60 - 20 * self.action, 20, 20, self.x, self.y, 60, 60)
            else:
                self.image.clip_draw(int(self.frame) * 20, 60 - 20 * self.action, 20, 20, self.x, self.y, 60, 60)

            draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 30, self.y - 30, self.x + 30, self.y + 30
