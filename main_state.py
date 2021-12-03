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
from background import Background
import server
from GenerateRandomObj import *

name = "MainState"

def enter():
    goomba_pos = SetMonsterPos(server.goombas_num, server.map_len)
    turtle_pos = SetMonsterPos(server.turtle_num, server.map_len, goomba_pos)
    blocks_attribute = SetBlockAttribute(server.blocks_center, server.map_data, server.blocks_center // 3)

    server.background = Background()
    server.mario = Mario()
    server.ground_tiles = [Ground(n,server.map_data[n]) for n in range(len(server.map_data))]
    server.goombas = [Goomba(goomba_pos[i]) for i in range(server.goombas_num)]
    server.green_trutles = [Green_turtle(turtle_pos[i]) for i in range(server.turtle_num)]
    server.blocks = [ Block(blocks_attribute[i],i) for i in range(len(blocks_attribute))]

    game_world.add_object(server.background,0)
    game_world.add_object(server.mario, 1)
    game_world.add_objects(server.goombas, 1)
    game_world.add_objects(server.green_trutles, 1)
    game_world.add_objects(server.blocks, 1)
    game_world.add_objects(server.ground_tiles, 1)

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
            game_world.clear()
            game_framework.change_state(title_state)
        else:
            server.mario.handle_event(event)

def update():
    for game_object in game_world.all_objects():
        game_object.update()

    if server.mario.death == 1:
        game_world.clear()
        game_framework.change_state(title_state)

def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()




