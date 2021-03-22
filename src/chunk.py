import generation as g
from tiles import Tiles as t

import math
import curses

class Chunk:
    def __init__(self, chunk_pos):
        self.chunk_pos = chunk_pos
        self.data = []
        self.generate(chunk_pos)

    def generate(self, t_id):
        self.data = g.generateChunk(t_id)

    def render(self, offset, stdscr):
        # go through data and place blocks by array index
        # every 16 go down a row
        # everything should also be move by adding (pos * 16)
        #
        # IMPORTANT NOTE!!!!!
        # Everything HAS to be relative to the position of the camera
        # So the formula for placing each tile should be:
        #
        # REMEMBER THAT CURSES USES (y, x) ;-;
        # place tile at pos (floor(i / 16) + cameraOffset.y, i % 16 + pos * 16 + cameraOffset.x)
        #
        for i in range(len(self.data)):
            try:
                stdscr.addstr(int(math.floor(i / 16)) + offset.y,
                              int(i % 16 + self.chunk_pos * 16) + offset.x,
                              str(t.tile_list[self.data[i]].texture),
                              curses.color_pair(t.tile_list[self.data[i]].color_pair))
            except:
                pass
