import curses
import math

import saveload as sl
import generation as g
import util as u
from tiles import Tiles
from coord import Coord

t = Tiles()

class World:
    def __init__(self, seed, name):
        self.seed = seed
        self.name = name
        self.chunk_list = []

    def newChunk(self, new_pos):
        self.chunk_list.append(Chunk(new_pos))

    def render(self, cam, stdscr):
        # figure out how to only generate chunks near camera
        for c in self.chunk_list:
            c.render(cam.pos, stdscr)
w = World(0, 'new_world')


class Chunk:
    def __init__(self, chunk_pos):
        self.chunk_pos = chunk_pos
        self.data = []
        self.generate(1)

    def generate(self, t_id):
        self.data = g.generateChunk(0)

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
                              str(t.tile_list[self.data[i]].texture))
            except:
                pass


class Camera:
    def __init__(self):
        self.pos = Coord()


class Character:
    def __init__(self):
        self.pos = Coord()
        self.current_chunk = 0
        self.current_chunk_index = 0
        self.current_chunk_pos = Coord(
            x=math.floor(self.pos.x % 16), y=self.pos.y)

    def render(self, offset, stdscr):
        try:
            stdscr.addstr(self.pos.y + offset.y, self.pos.x + offset.x, '☺')
        except:
            pass

    def getAdjacentChunk(self, chunk_id, offset):
        return self.getIndexOfChunk(chunk_id + offset)

    def checkForTileInChunk(self, tile_index, index, pos):
        if (w.chunk_list[index].data[u.coordToIndex(Coord(y=pos.y, x=pos.x))] == tile_index):
            return True

    def getIndexOfChunk(self, id):
        for i in range(len(w.chunk_list)):
            if (w.chunk_list[i].chunk_pos == self.current_chunk):
                return i

    def update(self):
        self.current_chunk = math.floor(self.pos.x / 16)
        self.current_chunk_pos = Coord(
            x=math.floor(self.pos.x % 16), y=self.pos.y)

        self.current_chunk_index = self.getIndexOfChunk(self.current_chunk)

    def moveCheck(self, _dir):
        #
        # REDO MOVEMENT!!!!!!!
        #
        
        #if (not self.checkForTileInChunk(0, self.current_chunk_index, Coord(x=self.current_chunk_pos.x, y=self.pos.y + 1))):
        
        if (_dir == 0):
            self.pos.addX(-1)
        elif (_dir == 1):
            self.pos.addX(1)
        
        #else:
        #   self.pos.y += 1


# +------------------------------------------------------+
# |                      MAIN LOOP!                      |
# +------------------------------------------------------+

cam = Camera()

plr = Character()

for i in range(0, 10):
    w.newChunk(i)


def curses_main(stdscr):
    stdscr.clear()
    rows, cols = stdscr.getmaxyx()

    while (True):

        stdscr.clear()
        w.render(cam, stdscr)
        plr.update()
        plr.render(cam.pos, stdscr)

        stdscr.addstr(0, 0, str(plr.pos.y))
        stdscr.refresh()

        k = stdscr.getch()
        if (k == ord('q')):
            break

        if (k == curses.KEY_LEFT):
            plr.moveCheck(0)

        if (k == curses.KEY_RIGHT):
            plr.moveCheck(1)

        cam.pos.x = -plr.pos.x + int(cols / 2)
        cam.pos.y = -plr.pos.y + int(rows / 2)
    stdscr.refresh()


curses.wrapper(curses_main)

sl.saveWorld(w, w.name)
