from pico2d import *
import game_framework
import game_world
import server
from random import randint

size = 513
size_on_canvas = 900

class Background:
    image = None
    def __init__(self):
        if Background.image == None and server.map_kind == 1:
            Background.image = load_image('26058.png')
        elif Background.image == None and server.map_kind == 2:
            Background.image = load_image('26058.png')
        self.x1 = [-450,450,1350]
        self.x2 = [-450,450,1350]
        self.y = 450
        self.back_rand = randint(0,3)
        self.foward_rand = randint(,4)

    def update(self):
        pass

    def draw(self):
        # 뒷 배경
        self.image.clip_draw(size * self.back_rand + 1, size * 2 + 1, size - 1,size - 1, self.x1[0], self.y, size_on_canvas,size_on_canvas) # 1
        self.image.clip_draw(size * self.back_rand + 1, size * 2 + 1, size - 1,size - 1, self.x1[1], self.y, size_on_canvas, size_on_canvas) # 2
        self.image.clip_draw(size * self.back_rand + 1, size * 2 + 1, size - 1,size - 1, self.x1[2], self.y, size_on_canvas,size_on_canvas) # 3
        # 앞 배경
        self.image.clip_draw(size * self.foward_rand + 1, size * 3 + 1, size - 1,size - 1, self.x2[0], self.y, size_on_canvas,size_on_canvas) # 1
        self.image.clip_draw(size * self.foward_rand + 1, size * 3 + 1, size - 1,size - 1, self.x2[1], self.y, size_on_canvas, size_on_canvas) # 2
        self.image.clip_draw(size * self.foward_rand + 1, size * 3 + 1, size - 1,size - 1, self.x2[2], self.y, size_on_canvas,size_on_canvas) # 3