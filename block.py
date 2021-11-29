from pico2d import *
import game_framework
import game_world
import server
import collision

TIME_PER_ACTION = 0.35
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

class Block:
    image = None
    def __init__(self,n):
        if Block.image == None:
            Block.image = load_image('block.png')
        self.size = 16
        self.size_on_canvas = 80 # 블록 당 약 1.15m
        self.x = self.size_on_canvas * server.map1[n][1]
        self.y = self.size_on_canvas / 2 + self.size_on_canvas * server.map1[n][2]
        self.frame = 0

    def update(self):
        self.frame = (self.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4

        if 610 > server.mario.x and server.mario.x > 590:
             self.x -= server.mario.velocity * server.mario.dash_mult * game_framework.frame_time

        if collision.collide(server.mario,self) and server.mario.cur_state_int != server.FallingState:
            server.mario.jump_cnt = 3

    def draw(self):
        self.image.clip_draw(self.size * int(self.frame), 80 - self.size, self.size, self.size,
                             self.x, self.y, self.size_on_canvas,
                             self.size_on_canvas)

        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 40, self.y - 40, self.x + 40, self.y + 40
