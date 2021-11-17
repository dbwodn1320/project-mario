import random
import json
import os

from pico2d import *
import game_framework
import game_world

from mario import Mario
from ground import Ground

name = "MainState"
DEBUG_KEY,RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SHIFT_DOWN, SHIFT_UP, SPACE, UP, DOWN, Landing = range(11)
DashState,IdleState,RunState,JumpState,FallingState,LandingState = range(6)

f = open("map_date.txt", 'r')
lines = f.readlines()
f.close()
map_data = []
for line in lines:
    line = line.strip()
    tmp = []
    if line == "=":
        map_data.append(tmp)
    else:
        line = int(line)
        while 1:
            tmp.append(line % 10)
            line = line // 10
            if line == 0: break

        tmp.reverse()
        map_data.append(tmp)

#print(map_data)

mario = None
ground_tiles = None

def enter():
    global mario,ground_tiles
    mario = Mario()
    ground_tiles = [Ground(n,map_data[n]) for n in range(len(map_data))]
    game_world.add_object(mario, 1)
    game_world.add_objects(ground_tiles, 0)

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
                game_framework.quit()
        else:
            mario.handle_event(event)

def update():
    #print(mario.cur_state)
    for game_object in game_world.all_objects():
        game_object.update()
    for tile in ground_tiles:
        if  610 > mario.x and mario.x > 590:
            tile.x -= mario.velocity * mario.dash_mult * game_framework.frame_time

        if mario.x - 100 < tile.x and tile.x < mario.x + 100:
            if collide(mario, tile, 0):
                mario.x -= mario.velocity * mario.dash_mult * game_framework.frame_time

        if tile.x - 50 < mario.x and mario.x < tile.x + 50:
            if collide(mario, tile, 1):
                 if mario.action == 5 or mario.action == 6:
                    mario.add_event(Landing)
                    mario.y = tile.y + 40 + 50 + (tile.tile_num - 1) * 80 - 1

                # else:
                #     if collide(mario, tile, 1) == False:
                #         mario.add_event(DOWN)



def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()

def collide(a, b, n):
    if n == 1:
        left_a, bottom_a, right_a, top_a = a.get_bb_foot()
    elif n == 0:
        left_a, bottom_a, right_a, top_a = a.get_bb_body()

    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True




