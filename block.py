from pico2d import *
import game_framework
import game_world
import server
import collision
from math import cos,sin
from item import Mushroom

TIME_PER_ACTION = 0.35
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

class Block:
    image = None
    def __init__(self,block_pos,n):
        if Block.image == None or server.map_kind == 2:
            Block.image = load_image('block_lava.png')
        elif Block.image == None or server.map_kind == 1:
            Block.image = load_image('block.png')
        self.size = 16
        self.size_on_canvas = 60 # 블록 당 약 1.15m
        self.x = self.size_on_canvas * block_pos[1]
        self.y = self.size_on_canvas / 2 + self.size_on_canvas * block_pos[2]
        self.kind = block_pos[0]
        self.state = 0
        self.frame = 0
        self.frame4 = 0
        self.png_y = 96

        self.spin = 0
        self.state2_xy = [[self.x, self.y] for i in range(4)]
        self.state2_time = 0

        self.state1_size = 0
        self.state1_flag = 1
        self.state1_done = 0

        self.coin_y = 0

    def update(self):
        self.frame = (self.frame + 3 * ACTION_PER_TIME * game_framework.frame_time) % 7
        self.frame4 = (self.frame + 3 * ACTION_PER_TIME * game_framework.frame_time) % 4

        if collision.collide_M(server.mario,self,2) and server.mario.cur_state_int == server.JumpState and self.state != 2:
            server.mario.jump_cnt = 3
            if self.kind == 0:
                if self.state == 0:
                    server.coin += 1
                self.state = 1
            elif self.kind == 1:
                self.state = 2
            elif self.kind == 2:
                if self.state == 0:
                    server.coin += 1
                self.state = 1
            elif self.kind == 3:
                if self.state == 0:
                    server.mushrooms.append(Mushroom(self.x,self.y))
                    game_world.add_object(server.mushrooms[len(server.mushrooms) - 1],0)
                self.state = 1

        if self.state == 2:
            if self.state2_xy[2][1] < 0:
                server.blocks.remove(self)
                game_world.remove_object(self)
            self.state2_time += 30 * game_framework.frame_time
            deg = 135
            for xy in self.state2_xy:
                xy[0] = 50 * cos(3.141592 * deg / 180) * self.state2_time + self.x
                xy[1] = 50 * sin(3.141592 * deg / 180) * self.state2_time - 0.5 * 9.8 * self.state2_time**2 + self.y
                deg -= 22.5

        elif self.state == 1 and self.state1_done == 0:
            if self.state1_size > 15:
                self.state1_flag = -1
            elif self.state1_size < 0:
                self.state1_flag = 0

            if self.state1_flag == 1:
                self.state1_size += 120 * game_framework.frame_time
                self.y += 150 * game_framework.frame_time
            elif self.state1_flag == -1:
                self.state1_size -= 120 * game_framework.frame_time
                self.y -= 150 * game_framework.frame_time
            elif self.state1_flag == 0:
                self.state1_size = 0
                self.state1_done = 1

            if self.coin_y < 200:
                self.coin_y += 1000 * game_framework.frame_time

    def draw(self):
        if self.state == 0:
            if self.kind == 0 or self.kind == 1:
                self.image.clip_draw(self.size * int(self.frame), self.png_y - self.size, self.size, self.size,
                             self.x, self.y, self.size_on_canvas,
                             self.size_on_canvas)
            if self.kind == 2 or self.kind == 3:
                self.image.clip_draw(self.size * int(self.frame4), self.png_y - 5 * self.size, self.size, self.size,
                                     self.x, self.y, self.size_on_canvas,
                                     self.size_on_canvas)

        elif self.state == 1:
            if self.state1_done == 0 and self.kind != 3:
                self.image.clip_draw(self.size * int(self.frame4), self.png_y - 3 * self.size, self.size, self.size,
                                 self.x, self.y + self.coin_y, self.size_on_canvas,self.size_on_canvas) # 코인

            if self.kind == 0:
                self.image.clip_draw(0, self.png_y - self.size - self.size * self.state1_done, self.size, self.size,
                                 self.x, self.y, self.size_on_canvas + self.state1_size,
                                 self.size_on_canvas + self.state1_size)

            elif self.kind == 2:
                self.image.clip_draw(0, self.png_y - self.size * 5 + self.size * 3 * self.state1_done, self.size, self.size,
                                     self.x, self.y, self.size_on_canvas + self.state1_size,
                                     self.size_on_canvas + self.state1_size)

            elif self.kind == 3:
                self.image.clip_draw(0, self.png_y - self.size * 5 + self.size * 3 * self.state1_done, self.size, self.size,
                                     self.x, self.y, self.size_on_canvas + self.state1_size,
                                     self.size_on_canvas + self.state1_size)

        elif self.state == 2:
            self.spin += game_framework.frame_time
            for xy in self.state2_xy:
                self.image.clip_composite_draw(0, self.png_y - 4 * self.size, self.size, self.size, 3.141592 * 2 * self.spin, '',
                                  xy[0], xy[1], 50, 50)


        #draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - self.size_on_canvas/2, self.y - self.size_on_canvas/2, self.x + self.size_on_canvas/2, self.y + self.size_on_canvas/2
