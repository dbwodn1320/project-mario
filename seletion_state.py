import game_framework
from pico2d import *
import gamestart_state
import store_state
import title_state
import server

name = "SelectionState"
image1 = None
image2 = None
shop = None
arrow = None
bg = None
font = None
font_level = None

arrow_y = 0
arrow_y_flag = 0
selected = [[1,0],[0,0]]
garo_index = 0
sero_index = 0

level = {0: 'EASY',1: 'NORMAL', 2: 'HARD'}
level_color = [(0,180,180),(180,180,180),(255,100,100)]
level_index = 0

def enter():
    global image1,image2,arrow,bg,font,shop,font_level
    font = load_font('SuperMario256.ttf',60)
    font_level = load_font('SuperMario256.ttf',100)
    image1 = load_image('map1.png')
    image2 = load_image('map2.png')
    arrow = load_image('arrow.png')
    bg = load_image('bg_selection.png')
    shop = load_image('mush.png')

def exit():
    global image1,image2,arrow,bg,shop,font,font_level
    #global garo_index,sero_index,level_index

    del(image1)
    del(image2)
    del(arrow)
    del(shop)
    del(bg)
    del(font)
    del(font_level)

def handle_events():
    global seleted,garo_index,sero_index,level_index
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.change_state(title_state)
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                if sero_index == 0 and garo_index == 0:
                    server.map_kind = 1
                    server.map_data,server.map_len = server.ReadMapTxt(server.map_kind)
                    game_framework.change_state(gamestart_state)
                elif sero_index == 0 and garo_index == 1:
                    server.map_kind = 2
                    server.map_data, server.map_len = server.ReadMapTxt(server.map_kind)
                    game_framework.change_state(gamestart_state)
                elif sero_index == 1 and garo_index == 0:
                    game_framework.change_state(store_state)
                elif sero_index == 1 and garo_index == 1:
                    level_index += 1
                    server.coin = 0
                    if level_index > 2:
                        level_index = 0
                    server.life = 5 - level_index * 2
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
                selected[sero_index][garo_index] = 0
                garo_index -= 1
                if garo_index < 0:
                    garo_index = abs(garo_index)
                selected[sero_index][garo_index] = 1
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
                selected[sero_index][garo_index] = 0
                garo_index += 1
                if garo_index > 1:
                    garo_index = 0
                selected[sero_index][garo_index] = 1
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
                selected[sero_index][garo_index] = 0
                sero_index -= 1
                if sero_index < 0:
                    sero_index = 1
                selected[sero_index][garo_index] = 1
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
                selected[sero_index][garo_index] = 0
                sero_index += 1
                if sero_index > 1:
                    sero_index = 0
                selected[sero_index][garo_index] = 1
def draw():
    clear_canvas()
    bg.clip_draw(0, 0, 526, 526, 450, 450, 900,900)

    image1.clip_draw(0,0,450, 450,225,600,300 + selected[0][0] * 50,300 + + selected[0][0] * 50)
    font.draw(225-180, 600 - 220, 'GRASSLAND', (0, 0, 0))

    image2.clip_draw(0,0,500, 500,675,600,300 + selected[0][1] * 50,300 ++ selected[0][1] * 50)
    font.draw(675-120, 600 - 220, 'CASTLE', (0, 0, 0))

    shop.clip_draw(0,0,38, 38,225,200,200 + selected[1][0] * 50,200 + selected[1][0] * 50)
    font.draw(225-90, 200 - 160, 'SHOP', (0, 0, 0))

    font_level.draw(625 - 70 - 110 * (level_index % 2), 200 - 50, level[level_index], level_color[level_index])

    if sero_index == 0 and garo_index == 0:
        arrow.clip_draw(0, 0, 190, 190, 225, 830 + arrow_y, 80, 80)
    elif sero_index == 0 and garo_index == 1:
        arrow.clip_draw(0, 0, 190, 190, 675, 830 + arrow_y, 80, 80)
    elif sero_index == 1 and garo_index == 0:
        arrow.clip_draw(0, 0, 190, 190, 225, 350 + arrow_y, 80, 80)
    elif sero_index == 1 and garo_index == 1:
        arrow.clip_draw(0, 0, 190, 190, 675, 300 + arrow_y, 80, 80)

    update_canvas()


def update():
    global arrow_y,arrow_y_flag

    if sero_index == 0 and garo_index == 0:
        pass
    elif sero_index == 0 and garo_index == 1:
        pass
    elif sero_index == 1 and garo_index == 0:
        pass
    elif sero_index == 1 and garo_index == 1:
        pass

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






