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
w = World(0, 'foo')


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
                              str(t.tile_list[self.data[i]].texture),
                              curses.color_pair(Tiles.tile_list[self.data[i]].color_pair))
            except:
                pass


class Camera:
    def __init__(self):
        self.pos = Coord()


class Character:
    def __init__(self):
        self.pos = Coord(y=50)
        self.current_chunk = 0
        self.current_chunk_index = 0
        self.current_chunk_pos = Coord(
            x=math.floor(self.pos.x % 16), y=self.pos.y)

    def render(self, offset, stdscr):
        try:
            stdscr.addstr(self.pos.y + offset.y, self.pos.x + offset.x, '☺')
        except:
            pass
    
    # TODO
    # Consider rethinking how these chunk functions are organized
    def getAdjacentChunk(self, chunk_list, chunk_id, offset):
        return self.getIndexOfChunk(chunk_list, chunk_id + offset)

    def checkForTileInChunk(self, chunk_list, tile_index, index, pos):
        if (chunk_list[index].data[u.coordToIndex(Coord(y=pos.y, x=pos.x))] == tile_index):
            return True

    def simpleTileDirCheck(self, chunk_list, offset):
        return self.checkForTileInChunk(chunk_list, 0, self.current_chunk_index, Coord(x=self.current_chunk_pos.x+offset.x, y=self.current_chunk_pos.y+offset.y))

    def getIndexOfChunk(self, chunk_list, _id):
        for i in range(len(w.chunk_list)):
            if (chunk_list[i].chunk_pos == _id):
                return i

    def update(self, chunk_list):
        self.current_chunk = math.floor(self.pos.x / 16)
        self.current_chunk_pos = Coord(
            x=math.floor(self.pos.x % 16), y=self.pos.y)

        self.current_chunk_index = self.getIndexOfChunk(chunk_list, self.current_chunk)

    def movePlr(self, chunk_list, _dir):
        # TODO
        #

        if (not self.checkForTileInChunk(chunk_list, 0, self.current_chunk_index, Coord(x=self.current_chunk_pos.x, y=self.pos.y + 1))):
            if  (_dir == 0):
                # On left edge of chunk
                if (self.current_chunk_pos.x == 0):
                    if (self.checkForTileInChunk(chunk_list, 0, self.getAdjacentChunk(chunk_list, self.current_chunk, -1), Coord(y=self.pos.y, x=15))):
                        self.pos.addX(-1)
                    elif (self.checkForTileInChunk(chunk_list, 0, self.getAdjacentChunk(chunk_list, self.current_chunk, -1), Coord(y=self.pos.y-1, x=15))):
                        self.pos.addX(-1)
                        self.pos.addY(-1)
                # Anywhere in between
                else:
                    if (self.simpleTileDirCheck(chunk_list, Coord(x=-1, y=0))):
                        self.pos.addX(-1)
                    elif (self.simpleTileDirCheck(chunk_list, Coord(x=-1, y=-1))):
                        self.pos.addX(-1)
                        self.pos.addY(-1)
            elif (_dir == 1):
                # On left edge of chunk
                if (self.current_chunk_pos.x == 15):
                    if (self.checkForTileInChunk(chunk_list, 0, self.getAdjacentChunk(chunk_list, self.current_chunk, 1), Coord(y=self.pos.y, x=0))):
                        self.pos.addX(1)
                    elif (self.checkForTileInChunk(chunk_list, 0, self.getAdjacentChunk(chunk_list, self.current_chunk, 1), Coord(y=self.pos.y-1, x=0))):
                        self.pos.addX(1)
                        self.pos.addY(-1)
                # Anywhere in between
                else:
                    if (self.simpleTileDirCheck(chunk_list, Coord(x=1, y=0))):
                        self.pos.addX(1)
                    elif (self.simpleTileDirCheck(chunk_list, Coord(x=1, y=-1))):
                        self.pos.addX(1)
                        self.pos.addY(-1)

        else:
            self.pos.y += 1
        
    def digInDir(self, chunk_list, _dir):
        # N
        if (_dir == 0):
            g.placeTile(chunk_list[self.current_chunk_index].data, Coord(x=self.current_chunk_pos.x, y=self.current_chunk_pos.y - 1), 0)
        # NE
        elif (_dir == 1):
            if (self.current_chunk_pos.x == 15):
                g.placeTile(chunk_list[self.getAdjacentChunk(chunk_list, self.current_chunk, 1)].data, Coord(x=0, y=self.current_chunk_pos.y - 1), 0)
            else:
                g.placeTile(chunk_list[self.current_chunk_index].data, Coord(x=self.current_chunk_pos.x + 1, y=self.current_chunk_pos.y - 1), 0)         
        # E
        elif (_dir == 2):
            if (self.current_chunk_pos.x == 15):
                g.placeTile(chunk_list[self.getAdjacentChunk(chunk_list, self.current_chunk, 1)].data, Coord(x=0, y=self.current_chunk_pos.y), 0)
            else:
                g.placeTile(chunk_list[self.current_chunk_index].data, Coord(x=self.current_chunk_pos.x + 1, y=self.current_chunk_pos.y), 0)         
        # SE
        elif (_dir == 3):
            if (self.current_chunk_pos.x == 15):
                g.placeTile(chunk_list[self.getAdjacentChunk(chunk_list, self.current_chunk, 1)].data, Coord(x=0, y=self.current_chunk_pos.y + 1), 0)
            else:
                g.placeTile(chunk_list[self.current_chunk_index].data, Coord(x=self.current_chunk_pos.x + 1, y=self.current_chunk_pos.y + 1), 0)
        # S
        elif (_dir == 4):
            g.placeTile(chunk_list[self.current_chunk_index].data, Coord(x=self.current_chunk_pos.x, y=self.current_chunk_pos.y + 1), 0)
            self.pos.addY(1)
        # SW 
        elif (_dir == 5):
            if (self.current_chunk_pos.x == 0):
                g.placeTile(chunk_list[self.getAdjacentChunk(chunk_list, self.current_chunk, -1)].data, Coord(x=15, y=self.current_chunk_pos.y + 1), 0)
            else:
                g.placeTile(chunk_list[self.current_chunk_index].data, Coord(x=self.current_chunk_pos.x - 1, y=self.current_chunk_pos.y + 1), 0)
        # W
        elif (_dir == 6):
            if (self.current_chunk_pos.x == 0):
                g.placeTile(chunk_list[self.getAdjacentChunk(chunk_list, self.current_chunk, -1)].data, Coord(x=15, y=self.current_chunk_pos.y), 0)
            else:
                g.placeTile(chunk_list[self.current_chunk_index].data, Coord(x=self.current_chunk_pos.x - 1, y=self.current_chunk_pos.y), 0)
        # NW 
        elif (_dir == 7):
            if (self.current_chunk_pos.x == 0):
                g.placeTile(chunk_list[self.getAdjacentChunk(chunk_list, self.current_chunk, -1)].data, Coord(x=15, y=self.current_chunk_pos.y - 1), 0)
            else:
                g.placeTile(chunk_list[self.current_chunk_index].data, Coord(x=self.current_chunk_pos.x - 1, y=self.current_chunk_pos.y - 1), 0)

        
        
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

    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)


    while (True):

        stdscr.clear()
        w.render(cam, stdscr)
        plr.update(w.chunk_list)
        plr.render(cam.pos, stdscr)

        stdscr.addstr(0, 0, str(plr.current_chunk_pos.x))
        stdscr.refresh()

        k = stdscr.getch()
        if (k == ord('q')):
            break

        if (k == curses.KEY_LEFT):
            plr.movePlr(w.chunk_list, 0)

        if (k == curses.KEY_RIGHT):
            plr.movePlr(w.chunk_list, 1)

        if (k == ord('w')):
            plr.digInDir(w.chunk_list, 0)
        if (k == ord('e')):
            plr.digInDir(w.chunk_list, 1)
        if (k == ord('d')):
            plr.digInDir(w.chunk_list, 2)
        if (k == ord('c')):
            plr.digInDir(w.chunk_list, 3)
        if (k == ord('s')):
            plr.digInDir(w.chunk_list, 4)
        if (k == ord('z')):
            plr.digInDir(w.chunk_list, 5)
        if (k == ord('a')):
            plr.digInDir(w.chunk_list, 6)
        if (k == ord('q')):
            plr.digInDir(w.chunk_list, 7)

        cam.pos.x = -plr.pos.x + int(cols / 2)
        cam.pos.y = -plr.pos.y + int(rows / 2)
    stdscr.refresh()


curses.wrapper(curses_main)

sl.saveWorld(w, w.name)
