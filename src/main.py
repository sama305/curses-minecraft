import curses
import math

import saveload as sl
import generation as g
import util as u
from tiles import Tiles as t
from coord import Coord as p
from chunk import Chunk


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


class Camera:
    def __init__(self):
        self.pos = p()


class Character:
    def __init__(self):
        self.pos = p(y=50)
        self.current_chunk = 0
        self.current_chunk_index = 0
        self.left_chunk_index = 0
        self.right_chunk_index = 0
        self.current_chunk_pos = p(
            x=math.floor(self.pos.x % 16), y=self.pos.y)
        self.chunk_list = []
        self.equipped_tile = 0

    def render(self, offset, stdscr):
        try:
            stdscr.addstr(self.pos.y + offset.y, self.pos.x + offset.x, '☺')
        except:
            pass

    # TODO
    # Consider rethinking how these chunk functions are organized
    def getAdjacentChunk(self, chunk_id, offset):
        return self.getIndexOfChunk(chunk_id + offset)

    def checkForTileInChunk(self, tile_index, chunk_index, pos):
        if (self.chunk_list[chunk_index].data[u.coordToIndex(p(y=pos.y, x=pos.x))] == tile_index):
            return True

    def collisionCheck(self, chunk_index, pos):
        return t.tile_list[self.chunk_list[chunk_index].data[u.coordToIndex(p(y=pos.y, x=pos.x))]].isSolid

    def getIndexOfChunk(self, _id):
        for i in range(len(w.chunk_list)):
            if (self.chunk_list[i].chunk_pos == _id):
                return i
        return -1

    def update(self, chunk_list):
        self.current_chunk = math.floor(self.pos.x / 16)
        self.current_chunk_pos = p(
            x=math.floor(self.pos.x % 16), y=self.pos.y)
        self.chunk_list = chunk_list

        self.current_chunk_index = self.getIndexOfChunk(
            self.current_chunk)
        self.left_chunk_index = self.getAdjacentChunk(
            self.current_chunk, -1)
        self.right_chunk_index = self.getAdjacentChunk(
            self.current_chunk, 1)

    def movePlr(self, _dir):
        # TODO
        #

        if (self.collisionCheck(self.current_chunk_index, p(x=self.current_chunk_pos.x, y=self.pos.y + 1))):
            if (_dir == 0):
                # On left edge of chunk
                if (self.current_chunk_pos.x == 0):
                    if (not self.collisionCheck(self.left_chunk_index, p(y=self.pos.y, x=15))):
                        self.pos.addX(-1)
                    elif (not self.collisionCheck(self.left_chunk_index, p(y=self.pos.y-1, x=15))):
                        self.pos.addX(-1)
                        self.pos.addY(-1)
                # Anywhere in between
                else:
                    if (not self.collisionCheck(self.current_chunk_index, p(x=self.current_chunk_pos.x-1, y=self.pos.y))):
                        self.pos.addX(-1)
                    elif (not self.collisionCheck(self.current_chunk_index, p(x=self.current_chunk_pos.x-1, y=self.pos.y-1))):
                        self.pos.addX(-1)
                        self.pos.addY(-1)
            elif (_dir == 1):
                # On right edge of chunk
                if (self.current_chunk_pos.x == 15):
                    if (not self.collisionCheck(self.right_chunk_index, p(y=self.pos.y, x=0))):
                        self.pos.addX(1)
                    elif (not self.collisionCheck(self.right_chunk_index, p(y=self.pos.y-1, x=0))):
                        self.pos.addX(1)
                        self.pos.addY(-1)
                # Anywhere in between
                else:
                    if (not self.collisionCheck(self.current_chunk_index, p(x=self.current_chunk_pos.x+1, y=self.pos.y))):
                        self.pos.addX(1)
                    elif (not self.collisionCheck(self.current_chunk_index, p(x=self.current_chunk_pos.x+1, y=self.pos.y-1))):
                        self.pos.addX(1)
                        self.pos.addY(-1)

        else:
            self.pos.y += 1

    def plrPlaceTile(self, _dir):
        # N
        if (_dir == 0):
            g.placeTile(self.chunk_list[self.current_chunk_index].data, p(
                x=self.current_chunk_pos.x, y=self.current_chunk_pos.y - 1), self.equipped_tile)
        # NE
        elif (_dir == 1):
            if (self.current_chunk_pos.x == 15):
                g.placeTile(self.chunk_list[self.right_chunk_index].data, p(
                    x=0, y=self.current_chunk_pos.y - 1), self.equipped_tile)
            else:
                g.placeTile(self.chunk_list[self.current_chunk_index].data, p(
                    x=self.current_chunk_pos.x + 1, y=self.current_chunk_pos.y - 1), self.equipped_tile)
        # E
        elif (_dir == 2):
            if (self.current_chunk_pos.x == 15):
                g.placeTile(self.chunk_list[self.right_chunk_index].data, p(
                    x=0, y=self.current_chunk_pos.y), self.equipped_tile)
            else:
                g.placeTile(self.chunk_list[self.current_chunk_index].data, p(
                    x=self.current_chunk_pos.x + 1, y=self.current_chunk_pos.y), self.equipped_tile)
        # SE
        elif (_dir == 3):
            if (self.current_chunk_pos.x == 15):
                g.placeTile(self.chunk_list[self.right_chunk_index].data, p(
                    x=0, y=self.current_chunk_pos.y + 1), self.equipped_tile)
            else:
                g.placeTile(self.chunk_list[self.current_chunk_index].data, p(
                    x=self.current_chunk_pos.x + 1, y=self.current_chunk_pos.y + 1), self.equipped_tile)
        # S
        elif (_dir == 4):
            if (t.tile_list[self.equipped_tile].isSolid):
                self.pos.addY(-1)
            
            g.placeTile(self.chunk_list[self.current_chunk_index].data, p(
                x=self.current_chunk_pos.x, y=self.pos.y + 1), self.equipped_tile)
            
            if (not t.tile_list[self.equipped_tile].isSolid):
                self.pos.addY(1)
        # SW
        elif (_dir == 5):
            if (self.current_chunk_pos.x == 0):
                g.placeTile(self.chunk_list[self.left_chunk_index].data, p(
                    x=15, y=self.current_chunk_pos.y + 1), self.equipped_tile)
            else:
                g.placeTile(self.chunk_list[self.current_chunk_index].data, p(
                    x=self.current_chunk_pos.x - 1, y=self.current_chunk_pos.y + 1), self.equipped_tile)
        # W
        elif (_dir == 6):
            if (self.current_chunk_pos.x == 0):
                g.placeTile(self.chunk_list[self.left_chunk_index].data, p(
                    x=15, y=self.current_chunk_pos.y), self.equipped_tile)
            else:
                g.placeTile(self.chunk_list[self.current_chunk_index].data, p(
                    x=self.current_chunk_pos.x - 1, y=self.current_chunk_pos.y), self.equipped_tile)
        # NW
        elif (_dir == 7):
            if (self.current_chunk_pos.x == 0):
                g.placeTile(self.chunk_list[self.left_chunk_index].data, p(
                    x=15, y=self.current_chunk_pos.y - 1), self.equipped_tile)
            else:
                g.placeTile(self.chunk_list[self.current_chunk_index].data, p(
                    x=self.current_chunk_pos.x - 1, y=self.current_chunk_pos.y - 1), self.equipped_tile)


# +------------------------------------------------------+
# |                      MAIN LOOP!                      |
# +------------------------------------------------------+
cam = Camera()

plr = Character()

chunk_gen_distance = 3

for i in range(-abs(chunk_gen_distance - 1), abs(chunk_gen_distance - 1)):
    w.newChunk(i)

def curses_main(stdscr):
    stdscr.clear()
    curses.noecho()
    rows, cols = stdscr.getmaxyx()

    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_YELLOW)

    while (True):
        plr.update(w.chunk_list)

        if (plr.pos.x % 15 == 0):
            new_chunk = math.floor((plr.pos.x) / 15)

            if (plr.getIndexOfChunk(new_chunk+1) == -1):
                w.newChunk(new_chunk+1)
            if (plr.getIndexOfChunk(new_chunk) == -1):
                w.newChunk(new_chunk)
            if (plr.getIndexOfChunk(new_chunk - 1) == -1):
                w.newChunk(new_chunk - 1)
            if (plr.getIndexOfChunk(new_chunk - 2) == -1):
                w.newChunk(new_chunk - 2)

        stdscr.clear()
        #w.render(cam, stdscr)
        w.chunk_list[plr.current_chunk_index].render(cam.pos, stdscr)
        w.chunk_list[plr.left_chunk_index].render(cam.pos, stdscr)
        w.chunk_list[plr.right_chunk_index].render(cam.pos, stdscr)
        plr.render(cam.pos, stdscr)

        stdscr.refresh()

        stdscr.addstr(0,0, 'X:' + str(plr.pos.x))
        stdscr.addstr(1,0, 'Y:' + str(plr.pos.y))
        stdscr.addstr(2,0, 'CHUNK:' + str(plr.current_chunk) + " - " + str(plr.current_chunk_pos.x) + "/15")

        k = stdscr.getch()
        if (k == ord('Q')):
            break

        if (k == curses.KEY_LEFT):
            plr.movePlr(0)

        if (k == curses.KEY_RIGHT):
            plr.movePlr(1)

        if (k == ord('1')):
            plr.equipped_tile = 0
        if (k == ord('2')):
            plr.equipped_tile = 5

        if (k == ord('w')):
            plr.plrPlaceTile(0)
        if (k == ord('e')):
            plr.plrPlaceTile(1)
        if (k == ord('d')):
            plr.plrPlaceTile(2)
        if (k == ord('c')):
            plr.plrPlaceTile(3)
        if (k == ord('s')):
            plr.plrPlaceTile(4)
        if (k == ord('z')):
            plr.plrPlaceTile(5)
        if (k == ord('a')):
            plr.plrPlaceTile(6)
        if (k == ord('q')):
            plr.plrPlaceTile(7)

        cam.pos.x = -plr.pos.x + int(cols / 2)
        cam.pos.y = -plr.pos.y + int(rows / 2)
    stdscr.refresh()


curses.wrapper(curses_main)

sl.saveWorld(w, w.name)
