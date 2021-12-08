import game_framework
from pico2d import *
import title_state

name = "StartState"
image = None

def enter():
    global image
    image = load_image('testmap.png')

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
    image.clip_draw(0,0,900, 900,450,450)
    update_canvas()


def update():
    pass


def pause():
    pass


def resume():
    pass






