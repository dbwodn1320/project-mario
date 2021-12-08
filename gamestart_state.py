import game_framework
from pico2d import *
import main_state
import server

name = "GamestartState"
image = None
mario_face = None
font = None

timer = 0

def enter():
    global image,mario_face,font
    image = load_image('black.png')
    mario_face = load_image('mario_life.png')
    font = load_font('SuperMario256.ttf',50)

def exit():
    global image,mario_face,timer,font
    del(image)
    del(mario_face)
    del(font)
    timer = 0

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        # else:
        #     if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
        #         game_framework.quit()
        #     elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
        #         game_framework.change_state(seletion_state)

def draw():
    clear_canvas()
    image.clip_draw(0,0,100,100,450,450,900,900)
    mario_face.clip_draw(0,0,434,489
                         ,370,450,70,70)
    font.draw(470,450,"X %d"% server.life,(255,255,255))
    if server.map_kind == 1:
        font.draw(350,550,"GRASSLAND",(255,255,255))
    else:
        font.draw(300, 550, "KOOPA CASTLE", (255,255,255))
    update_canvas()


def update():
    global timer
    timer += game_framework.frame_time
    if timer > 1.0:
        game_framework.change_state(main_state)
def pause():
    pass


def resume():
    pass






