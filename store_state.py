import game_framework
from pico2d import *
import seletion_state
import server

name = "StoreState"
image = None
arrow = None
RM = None
BM = None

arrow_y = 0
arrow_y_flag = 0

selection_x = [300,600]
selection_index = 0
font = None

def enter():
    global image,arrow,RM,BM,font
    image = load_image('bg_store.png')
    arrow = load_image('arrow.png')
    RM = load_image('mush.png')
    BM = load_image('mush_blue.png')
    font = load_font("SuperMario256.ttf", 60)
def exit():
    global image,arrow,RM,BM,font
    del(image)
    del(arrow)
    del(RM)
    del(BM)
    del(font)

def handle_events():
    global selection_index
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.change_state(seletion_state)
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                if selection_index == 0:
                    if server.coin >= 99:
                        server.coin = server.coin - 99
                        server.life += 1
                elif selection_index == 1 and server.power == 0:
                    if server.coin >= 50:
                        server.coin = server.coin - 50
                        server.power += 1
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
                selection_index = 1 - selection_index
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
                selection_index = 1 - selection_index
def draw():
    clear_canvas()
    image.clip_draw(0,0,500,500,450,450,900,900)
    BM.clip_draw(0,0,500,500,300,450,200 + 50 * (1 - selection_index),200 + 50 * (1-selection_index))
    font.draw(240, 650, '1UP', (0, 0, 180))
    font.draw(225, 250, '99EA', (0, 0, 180))

    RM.clip_draw(0,0,500,500,600,450,200 + 50 * selection_index,200 + 50 * selection_index)
    font.draw(450, 650, 'POWERUP', (180, 0, 0))
    font.draw(525, 250, '50EA', (180, 0, 0))

    font.draw( 300, 850, 'COIN: %d' % server.coin, (0, 0, 0))

    arrow.clip_draw(0, 0, 190, 190, selection_x[selection_index], 600 + arrow_y, 80, 80)



    update_canvas()

def update():
    global arrow_y,arrow_y_flag

    if arrow_y > 20:
        arrow_y_flag = 1
    elif arrow_y < -20:
        arrow_y_flag = 0

    if arrow_y_flag == 0:
        arrow_y += 100 * game_framework.frame_time
    else:
        arrow_y -= 100 * game_framework.frame_time

def pause():
    pass

def resume():
    pass