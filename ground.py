from pico2d import *

class Grass:
    image = None
    def __init__(self):
        if image == None:
        self.image = load_image('ground_world1.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(400, 30)
        self.image.draw(1200, 30)
