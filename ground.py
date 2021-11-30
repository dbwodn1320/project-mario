from pico2d import *
import game_framework
import game_world
import server
import collision

class Ground:
    image = None
    def __init__(self, n, list):
        if Ground.image == None:
            Ground.image = load_image('ground_world1.png')
        self.size = 16
        self.size_on_canvas = 60 # 블록 당 약 1.15m
        self.map_data = list
        self.tile_num = len(self.map_data)
        self.x = self.size_on_canvas * n
        self.y = self.size_on_canvas / 2
        self.top_y = self.y + self.size_on_canvas/2 + self.size_on_canvas * (self.tile_num -1)
        self.num = n

    def update(self):
        if 610 > server.mario.x and server.mario.x > 590:
            self.x -= server.mario.velocity * server.mario.dash_mult * game_framework.frame_time

    def draw(self):
        if -100 < self.x and self.x < 1300 :
            for j in range(0, len(self.map_data)):
                self.image.clip_draw(self.size * (self.map_data[j] % 5), self.size - self.size * (self.map_data[j] // 5), self.size, self.size,
                                         self.x, self.size_on_canvas / 2 + self.size_on_canvas * j, self.size_on_canvas, self.size_on_canvas)


            draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - self.size_on_canvas/2, self.y - self.size_on_canvas/2, self.x + self.size_on_canvas/2, self.y + self.size_on_canvas/2 + self.size_on_canvas * (self.tile_num -1)
