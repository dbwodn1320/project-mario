import game_framework
import pico2d

import main_state
import title_state

pico2d.open_canvas(1200, 900)
game_framework.run(title_state)
pico2d.close_canvas()