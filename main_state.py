import random
import json
import os

from pico2d import *
import game_framework
import game_world

from mario import Mario
from ground import Ground
from goomba import Goomba
from green_turtle import Green_turtle
import server

name = "MainState"
DEBUG_KEY,RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SHIFT_DOWN, SHIFT_UP, SPACE, UP, DOWN, Landing = range(11)
DashState,IdleState,RunState,JumpState,FallingState,LandingState = range(6)

def enter():
    server.mario = Mario()
    server.goomba = Goomba([600,111])
    server.green_trutle = Green_turtle([700,111])
    server.ground_tiles = [Ground(n,server.map_data[n]) for n in range(len(server.map_data))]
    game_world.add_object(server.mario, 1)
    game_world.add_object(server.goomba, 1)
    game_world.add_object(server.green_trutle, 1)
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
                game_framework.quit()
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




