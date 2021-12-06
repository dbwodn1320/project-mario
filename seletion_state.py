import game_framework
from pico2d import *
import main_state
import title_state
import server

name = "SelectionState"
image1 = None
image2 = None
arrow = None
bg = None

arrow_y = 0
arrow_y_flag = 0

def enter():
    global image1,image2,arrow,bg
    image1 = load_image('map1.png')
    image2 = load_image('map2.png')
    arrow = load_image('arrow.png')
    #bg = load_image('lobby.png')

def exit():
    global image1,image2,arrow,bg
    del(image1)
    del(image2)
    del(arrow)
    #del(bg)

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.change_state(title_state)
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                server.map_data,server.map_len = server.ReadMapTxt(server.map_kind)
                game_framework.change_state(main_state)
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
                if server.map_kind == 1:
                    server.map_kind = 2
                elif server.map_kind == 2:
                    server.map_kind = 1
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
                if server.map_kind == 1:
                    server.map_kind = 2
                elif server.map_kind == 2:
                    server.map_kind = 1
def draw():
    clear_canvas()
    image1.clip_draw(0,0,450, 450,225,600,300 + server.map_kind % 2 * 50,300 + server.map_kind % 2 * 50)
    image2.clip_draw(0,0,500, 500,675,600,300 + + server.map_kind // 2 * 50,300 + server.map_kind // 2 * 50)
    if server.map_kind == 1:
        arrow.clip_draw(0, 0, 190, 190, 225, 830 + arrow_y, 80, 80)
    elif server.map_kind == 2:
        arrow.clip_draw(0, 0, 190, 190, 675, 830 + arrow_y, 80, 80)

    update_canvas()


def update():
    global arrow_y,arrow_y_flag

    if arrow_y > 40:
        arrow_y_flag = 1
    elif arrow_y < -40:
        arrow_y_flag = 0

    if arrow_y_flag == 0:
        arrow_y += 200 * game_framework.frame_time
    else:
        arrow_y -= 200 * game_framework.frame_time


def pause():
    pass


def resume():
    pass






