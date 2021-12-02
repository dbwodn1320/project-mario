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

class Goomba:
    image = None
    def __init__(self, n):
        if Goomba.image == None:
            Goomba.image = load_image('goomba.png')
        self.size = 20, 20
        self.size_on_canvas = 60 # 가로세로 약 0.9m
        self.x = server.ground_tiles[n].x
        self.y = server.ground_tiles[n].top_y + 31
        self.dir = -1
        self.frame = 0
        self.action = 1
        self.death = 0
        self.death_cnt = 0
        self.gravity_cnt = 0
        self.active = 0
        self.floor = 0

        self.spin = 0

    def update(self):
        if self.y < 0:
            game_world.remove_object(self)
            server.goombas.remove(self)
        # 화면에 들어올 시 활성화 및 방향, 액션 설정
        if self.active == 0:
            if 0 < self.x and self.x < 1200:
                self.active = 1
        elif self.active == 1:
            if self.death == 1:
                self.action = 3
                if self.frame > 1:
                    self.frame = 1
                self.death_cnt += game_framework.frame_time
            elif self.dir == -1: self.action = 1
            elif self.dir == 1: self.action = 2

            self.frame = (self.frame + FRAMES_PER_ACTION[self.action] * ACTION_PER_TIME * game_framework.frame_time) % \
                          FRAMES_PER_ACTION[self.action]

            # 살아있을 때
            if self.death == 0:
                self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time
                if server.mario.cur_state_int == server.FallingState:
                    if collision.collide_M(server.mario, self, 1):
                        self.death = 1
                        self.frame = 0
                        server.mario.jump_cnt = 0.1
                        server.mario.add_event(server.UP)

                for turtle in server.green_trutles:
                    if turtle.shell == 1:
                        if collision.collide_M(turtle, self, 1):
                            self.death = 2

            if self.death_cnt > 1.0:
                server.goombas.remove(self)
                game_world.remove_object(self)

            for tile in server.ground_tiles:
                if tile.top_y >= self.y:
                    if self.x - 35 < tile.x and tile.x < self.x + 35:
                        if collision.collide(tile, self):
                            if self.dir == 1:
                                self.dir = -1
                            elif self.dir == -1:
                                self.dir = 1
                if tile.x - 30 < self.x and self.x < tile.x + 30:
                    self.floor = tile.top_y
                    if self.floor == 0:
                        self.floor = -100
            if self.death == 2:
                self.y += 1000 * game_framework.frame_time
            self.y -= GRAVITY * self.gravity_cnt * game_framework.frame_time
            self.gravity_cnt += game_framework.frame_time

            if self.death < 2:
                if self.y < self.floor + 31:
                    self.y = self.floor + 31
                    self.gravity_cnt = 0

    def draw(self):
        if -100 < self.x and self.x < 1300 :
            if self.death == 0 or self.death == 1:
                self.image.clip_draw(int(self.frame) * 20, 60 - 20 * self.action, 20, 20, self.x, self.y, 60, 60)
            elif self.death == 2:
                self.spin += game_framework.frame_time
                self.image.clip_composite_draw(0, 60 - 20,20, 20,3.141592 * 2 * self.spin,'', self.x, self.y, 60, 60)

            draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 30, self.y - 30, self.x + 30, self.y + 30
