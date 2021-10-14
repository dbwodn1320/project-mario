from pico2d import *

canvas_width = 1200
canvas_height = 900

class Mario:
    def __init__(self):
        self.x, self.y = 30, 90
        self.frameX = 0
        self.frameY = 0
        self.image = load_image('mario.png')

    def update(self):
        self.frameX = (self.frameX + 1) % 63
        self.x = 0

    def draw(self):
        self.image.clip_draw(self.frameX*26, 360,26,44,self.x,self.y)

def handle_events():
    global running
    global x, y
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
         elif event.type == SDL_MOUSEMOTION:
            x, y = event.x, canvas_height - 1 - event.y
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False

mario = Mario()
open_canvas(canvas_width,canvas_height)
mario1 = load_image('mario.png')
x = 30
y = 90
frame = 0
running = True

while(running):
    clear_canvas()
    mario1.clip_draw(frame * 30, 511 - 40 * 3, 30 , 40,x + 600,y + 450)
    frame += 1
    frame = frame % 24
    print(frame)
    update_canvas()
    handle_events()
    delay(0.03)

close_canvas()



