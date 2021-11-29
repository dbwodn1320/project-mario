from pico2d import *
import game_framework
import game_world
import server
import collision

map1 = [[0,0],[0,0]]
map2 = [[0,0],[0,0]]

class Block:
    image = None
    def __init__(self,n):
        if Block.image == None:
            Block.image = load_image('ground_world1.png')
        self.size = 16
        self.size_on_canvas = 80 # 블록 당 약 1.15m
        self.map_data = list
        self.tile_num = len(self.map_data)
        self.x = self.size_on_canvas * map1[n][0]
        self.y = self.size_on_canvas / 2 + self.size_on_canvas * map1[n][1]

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(self.size, self.size, self.size, self.size,
                             self.x, self.y, self.size_on_canvas,
                             self.size_on_canvas)

        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 40, self.y - 40, self.x + 40, self.y + 40
