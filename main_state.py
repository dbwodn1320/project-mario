import random
import json
import os

from pico2d import *
import game_framework
import game_world
import title_state

from mario import Mario
from ground import Ground
from goomba import Goomba
from green_turtle import Green_turtle
from block import Block
import server
import random

name = "MainState"

def enter():
    server.mario = Mario()
    server.ground_tiles = [Ground(n,server.map_data[n]) for n in range(len(server.map_data))]
    map_len = len(server.ground_tiles)
    server.goombas = [Goomba(random.randint(10 + 20 * i,20 * (i + 1))) for i in range(10)]
    server.green_trutles = [Green_turtle(random.randint(10 + 20 * i, 20 * (i + 1))) for i in range(10)]
    server.blocks = [ Block(j) for j in range(5)]

    game_world.add_object(server.mario, 1)
    game_world.add_objects(server.goombas, 1)
    game_world.add_objects(server.green_trutles, 1)
    game_world.add_objects(server.ground_tiles, 1)
    game_world.add_objects(server.blocks, 1)

def exit():
    game_world.clear()

def pause():
    pass

def resume():
    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.change_state(title_state)
                game_world.clear()
        else:
            server.mario.handle_event(event)

def update():
    for game_object in game_world.all_objects():
        game_object.update()

def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()




