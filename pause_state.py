import game_framework
from pico2d import *
import title_state

os.chdir("d:/2DGP/project mario/resource")

name = "StartState"
image = None
timer = 0

def enter():
    global image
    image = load_image('kpu_credit.png')

def exit():
    global image
    del(image)

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(title_state)

def draw():
    clear_canvas()
    image.draw(450,450)
    update_canvas()


def update():
    global timer
    timer += game_framework.frame_time
    if timer > 2.0:
        game_framework.change_state(title_state)

def pause():
    pass


def resume():
    pass






