import game_framework
from pico2d import *
import main_state
import server
import seletion_state

name = "LeaderboardState"
image = None
font = None

timer = 0

def enter():
    global image,font
    image = load_image('bg_store.png')
    font = load_font('SuperMario256.ttf',50)

def exit():
    global image,timer,font
    del(image)
    del(font)
    timer = 0

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.change_state(seletion_state)
def draw():
    clear_canvas()
    image.clip_draw(0,0,500,500,450,450,900,900)

    font.draw(260, 860, "TIME RANKING", (0, 0, 0))
    font.draw(150, 800, "GRASSLAND", (0, 0, 0))
    font.draw(550, 800, "CASTLE" , (0, 0, 0))
    font.draw(50, 750, "1st", (0, 0, 0))
    font.draw(50, 650, "2nd", (0, 0, 0))
    font.draw(50, 550, "3rd", (0, 0, 0))
    font.draw(50, 450, "4th", (0, 0, 0))
    font.draw(50, 350, "5th", (0, 0, 0))

    for j in range(2):
        for i in range(5):
            if len(server.time_ranking[j]) != 0 and len(server.time_ranking[j]) - 1 >= i:
                font.draw(250 + j * 400, 750 - i * 100, "%d" % server.time_ranking[j][i], (255, 255, 255))
            else:
                font.draw(250 + j * 400, 750 - i * 100, "0", (255, 255, 255))

    update_canvas()


def update():
    pass

def pause():
    pass


def resume():
    pass