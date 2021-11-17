from pico2d import *

class Ground:
    image = None
    def __init__(self, n, list):
        if Ground.image == None:
            Ground.image = load_image('ground_world1.png')
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
            for j in range(0, len(self.map_data)):
                if self.map_data[j] == 0:
                    self.image.clip_draw(self.size * self.map_data[j], self.size, self.size, self.size,
                                         self.x, self.size_on_canvas / 2 + self.size_on_canvas * j, self.size_on_canvas, self.size_on_canvas)
                elif self.map_data[j] == 1:
                    self.image.clip_draw(self.size * self.map_data[j], self.size, self.size, self.size,
                                         self.x, self.size_on_canvas / 2 + self.size_on_canvas * j, self.size_on_canvas, self.size_on_canvas)
                elif self.map_data[j] == 2:
                    self.image.clip_draw(self.size * self.map_data[j], self.size, self.size, self.size,
                                         self.x, self.size_on_canvas / 2 + self.size_on_canvas * j, self.size_on_canvas, self.size_on_canvas)
                elif self.map_data[j] == 3:
                    self.image.clip_draw(self.size * self.map_data[j], self.size, self.size, self.size,
                                         self.x, self.size_on_canvas / 2 + self.size_on_canvas * j, self.size_on_canvas, self.size_on_canvas)
                elif self.map_data[j] == 4:
                    self.image.clip_draw(self.size * self.map_data[j], self.size, self.size, self.size,
                                         self.x, self.size_on_canvas / 2 + self.size_on_canvas * j, self.size_on_canvas, self.size_on_canvas)
                elif self.map_data[j] == 5:
                    self.image.clip_draw(self.size * (self.map_data[j] % 5), 0, self.size, self.size,
                                         self.x, self.size_on_canvas / 2 + self.size_on_canvas * j, self.size_on_canvas, self.size_on_canvas)
                elif self.map_data[j] == 6:
                    self.image.clip_draw(self.size * (self.map_data[j] % 5), 0, self.size, self.size,
                                         self.x, self.size_on_canvas / 2 + self.size_on_canvas * j, self.size_on_canvas, self.size_on_canvas)
                elif self.map_data[j] == 7:
                    self.image.clip_draw(self.size * (self.map_data[j] % 5), 0, self.size, self.size,
                                         self.x, self.size_on_canvas / 2 + self.size_on_canvas * j, self.size_on_canvas, self.size_on_canvas)
                elif self.map_data[j] == 8:
                    self.image.clip_draw(self.size * (self.map_data[j] % 5), 0, self.size, self.size,
                                         self.x, self.size_on_canvas / 2 + self.size_on_canvas * j, self.size_on_canvas, self.size_on_canvas)
                elif self.map_data[j] == 9:
                    self.image.clip_draw(self.size * (self.map_data[j] % 5), 0, self.size, self.size,
                                         self.x, self.size_on_canvas / 2 + self.size_on_canvas * j, self.size_on_canvas, self.size_on_canvas)

            draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 40, self.y - 40, self.x + 40, self.y + 40 + 80 * (self.tile_num -1)
