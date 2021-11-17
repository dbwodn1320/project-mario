from pico2d import *

class Monster:
    image = None
    def __init__(self, n):
        if Monster.image == None:
            if n == 0:
                Monster.image = load_image('goomba.png')
            if n == 1:
                Monster.image = load_image('green_turtle.png')

        self.size = 16
        self.size_on_canvas = 80 # 블록 당 약 1.15m
        self.map_data = list
        self.tile_num = len(self.map_data)
        self.x = self.size_on_canvas * n
        self.y = self.size_on_canvas / 2

    def update(self):
        pass

    def draw(self):
        if -100 < self.x and self.x < 1300 :
            draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 40, self.y - 40, self.x + 40, self.y + 40 + 80 * (self.tile_num -1)
