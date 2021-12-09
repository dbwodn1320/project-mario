import game_framework
from pico2d import *
import server
import start_state

name = "GamesoverState"
image = None
font = None
sound = None

timer = 0

def enter():
    global image,font,sound
    image = load_image('black.png')
    font = load_font('SuperMario256.ttf',100)
    sound = load_music('smb_gameover.wav')
    sound.set_volume(32)
    sound.play()

def exit():
    global image,timer,font,sound
    del(image)
    del(font)
    del(sound)
    timer = 0

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()

def draw():
    clear_canvas()
    image.clip_draw(0,0,100,100,450,450,900,900)
    font.draw(100,450,"GAME OVER..",(255,0,0))
    update_canvas()

def update():
    global timer
    timer += game_framework.frame_time
    if timer > 1.0:
        game_framework.change_state(start_state)
        server.coin = 0
        server.life = 5
def pause():
    pass


def resume():
    pass






