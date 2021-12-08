import game_framework
from pico2d import *
import seletion_state
import os

name = "TitleState"
image = None
bgm = None

def enter():
    global image,bgm
    image = load_image('title.png')
    bgm = load_music("bgm_title.mp3")
    bgm.set_volume(32)
    bgm.repeat_play()

def exit():
    global image,bgm
    del(image)
    del(bgm)

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(seletion_state)

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






