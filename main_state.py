import random
import json
import os

from pico2d import *
import game_framework
import game_world
import seletion_state
import gameover_state

from mario import Mario
from ground import Ground
from goomba import Goomba
from green_turtle import Green_turtle
from block import Block
from background import Background
from item import Coin
import server
from GenerateRandomObj import *

name = "MainState"

def enter():
    server.powerup = load_wav('smb_powerup.wav')
    server.powerup.set_volume(32)

    server.coin_sound = load_wav('smb_coin.wav')
    server.coin_sound.set_volume(32)

    goomba_pos = SetMonsterPos(server.goombas_num*(seletion_state.level_index + 1), server.map_len)
    turtle_pos = SetMonsterPos(server.turtle_num*(seletion_state.level_index + 1), server.map_len, goomba_pos)
    #print(len(goomba_pos),len(turtle_pos))
    blocks_attribute,coin_pos = SetBlockAttribute(server.blocks_center, server.map_data, server.blocks_center // 3)

    server.background = Background()
    server.mario = Mario()
    server.ground_tiles = [Ground(n,server.map_data[n]) for n in range(len(server.map_data))]
    server.goombas = [Goomba(goomba_pos[i]) for i in range(server.goombas_num)]
    server.green_trutles = [Green_turtle(turtle_pos[i]) for i in range(server.turtle_num)]
    server.blocks = [ Block(blocks_attribute[i],i) for i in range(len(blocks_attribute))]
    server.coins = [Coin(coin_pos[i]) for i in range(len(coin_pos))]

    game_world.add_object(server.background,0)
    game_world.add_objects(server.goombas, 1)
    game_world.add_objects(server.green_trutles, 1)
    game_world.add_objects(server.coins, 0)
    game_world.add_objects(server.ground_tiles, 1)
    game_world.add_object(server.mario, 1)
    game_world.add_objects(server.blocks, 1)

def exit():
    game_world.clear()
    server.background.bgm.stop()

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
            game_framework.change_state(seletion_state)
        else:
            server.mario.handle_event(event)

def update():
    global time_cnt,a,clear_sound
    if server.mario.timestop == 0:
        for game_object in game_world.all_objects():
            game_object.update()
        time_cnt = 0
        a = 0
    elif server.mario.timestop == 1:
        time_cnt += game_framework.frame_time
        if time_cnt % 0.2 > 0.18:
            a = 1 - a
        server.mario.image.opacify(int(a))
        server.mario.image_small.opacify(int(a))
        if time_cnt > 0.7:
            server.mario.timestop = 0
            server.mario.image.opacify(1)
            server.mario.image_small.opacify(1)
            if server.mario.hp == 0:
                server.mario.ghost = 1
    elif server.mario.timestop == 2:
        if time_cnt == 0:
            server.time_ranking[server.map_kind - 1].append(int(server.background.time))
            server.time_ranking[server.map_kind - 1].sort()
            with open('ranking.json', 'w') as f:
                f.write(json.dumps(server.time_ranking))

            #print(server.time_ranking[seletion_state.level_index])
            clear_sound = load_wav("sbm_mapcomplete.wav")
            clear_sound.set_volume(32)
            server.background.bgm.stop()
            clear_sound.play()

        time_cnt += game_framework.frame_time
        if time_cnt > 4.0:
            game_framework.change_state(seletion_state)

    if server.mario.death == 1:
        server.mario.death_sound.play()
        game_world.clear()
        if server.life < 0:
            game_framework.change_state(gameover_state)
            seletion_state.selected = [[1, 0], [0, 0]]
            seletion_state.garo_index = 0
            seletion_state.sero_index = 0
            seletion_state.level_index = 0
        else:
            game_framework.change_state(seletion_state)


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()




