from pico2d import *
import game_framework
import game_world
import server
from random import randint

size = 513
size_on_canvas = 900

class Background:
    def __init__(self):
        self.x1 = [-450,450,1350]
        self.x2 = [-450,450,1350]
        self.y = 450
        if server.map_kind == 1:
            self.image = load_image('bg_grassland.png')
            Background.back = randint(0,3)
            Background.front = randint(1,4)
        elif server.map_kind == 2:
            self.image = load_image('bg_castle.png')
            Background.back = 0
            Background.front = 3


    def update(self):
        pass

    def draw(self):
        # 뒷 배경
        self.image.clip_draw(size * self.back + 1, size * 2 + 1, size - 1,size - 1, self.x1[0], self.y, size_on_canvas,size_on_canvas) # 1
        self.image.clip_draw(size * self.back+ 1, size * 2 + 1, size - 1,size - 1, self.x1[1], self.y, size_on_canvas, size_on_canvas) # 2
        self.image.clip_draw(size * self.back + 1, size * 2 + 1, size - 1,size - 1, self.x1[2], self.y, size_on_canvas,size_on_canvas) # 3
        # 앞 배경
        self.image.clip_draw(size * self.front + 1, size * 3 + 1, size - 1,size - 1, self.x2[0], self.y, size_on_canvas,size_on_canvas) # 1
        self.image.clip_draw(size * self.front + 1, size * 3 + 1, size - 1,size - 1, self.x2[1], self.y, size_on_canvas, size_on_canvas) # 2
        self.image.clip_draw(size * self.front + 1, size * 3 + 1, size - 1,size - 1, self.x2[2], self.y, size_on_canvas,size_on_canvas) # 3