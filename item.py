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
FRAMES_PER_ACTION = [0, 9, 9, 2]

class Mushroom:
    image = None
    def __init__(self, x,y):
        if Mushroom.image == None:
            Mushroom.image = load_image('mush.png')
        self.size = 38, 38
        self.size_on_canvas = 60 # 가로세로 약 0.9m
        self.x = x
        self.y = y
        self.y_origin = y
        self.dy = 0
        self.dir = 0
        self.gravity_cnt = 0
        self.floor = 0
        self.falling = 0

        self.active = 0

    def update(self):
        if self.active == 0:
            self.y += 120 * game_framework.frame_time
            if self.y - self.y_origin > 60:
                self.active = 1
                if self.x > server.mario.x:
                    self.dir = 1
                elif self.x < server.mario.x:
                    self.dir = -1

        elif self.active == 1:
            if self.y < 0:
                game_world.remove_object(self)
                server.mushrooms.remove(self)

            self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time
            if collision.collide(server.mario, self):
                server.mushrooms.remove(self)
                game_world.remove_object(self)
                if server.mario.hp == 0:
                    server.mario.timestop = 1
                    server.mario.hp += 1
                    server.mario.y += 10

            for tile in server.ground_tiles:
                if tile.top_y >= self.y:
                    if self.x - 35 < tile.x < self.x + 35:
                        if collision.collide(tile, self):
                            if self.dir == 1:
                                self.dir = -1
                            elif self.dir == -1:
                                self.dir = 1
                else:
                    if collision.collide(tile, self):
                        self.falling = 0
                        self.y = tile.top_y + 31
                        self.gravity_cnt = 0

            for block in server.blocks:
                if collision.collide(block, self):
                    if block.y + 30 > self.y:
                        if self.dir == 1:
                            self.dir = -1
                        elif self.dir == -1:
                            self.dir = 1
                    else:
                        self.falling = 0
                        self.y = block.y + 31 + 30
                        self.gravity_cnt = 0

            t_cnt = 0
            for tile in server.ground_tiles:
                if not collision.collide(tile, self) and self.falling == 0:
                    t_cnt += 1
            for block in server.blocks:
                if not collision.collide(block, self) and self.falling == 0:
                    t_cnt += 1
            if t_cnt == len(server.ground_tiles) + len(server.blocks):
                self.falling = 1

            if self.falling == 1:
                self.y -= GRAVITY * self.gravity_cnt * game_framework.frame_time
                self.gravity_cnt += game_framework.frame_time


    def draw(self):
        if -100 < self.x and self.x < 1300 :
            self.image.clip_draw(0, 0, 38, 38, self.x, self.y, 60, 60)

            #draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 30, self.y - 30, self.x + 30, self.y + 30

class Coin:
    image = None
    def __init__(self, pos):
        if Coin.image == None:
            Coin.image = load_image('coin.png')
        self.size = 16
        self.size_on_canvas = 60  # 가로세로 약 0.9m
        self.x = self.size_on_canvas * pos[0]
        self.y = self.size_on_canvas / 2 + self.size_on_canvas * pos[1]
        self.gravity_cnt = 0
        self.frame = 0

    def update(self):
        self.frame = (self.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4

        if collision.collide(server.mario,self) and server.mario.cur_state_int != server.DeathState:
            server.coins.remove(self)
            game_world.remove_object(self)
            server.coin += 1
            print(server.coin)
    def draw(self):
        if -100 < self.x and self.x < 1300:
            self.image.clip_draw(self.size * int(self.frame), 0, 16, 16, self.x, self.y, 60, 60)

    def get_bb(self):
        return self.x - 35, self.y - 35, self.x + 35, self.y + 35
