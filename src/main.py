# -*- coding: utf-8 -*-

import curses
import math

import saveload as sl
import generation as g
import util as u
from tiles import Tiles as t
from coord import Coord as p
from chunk import Chunk

directions = {
    "w": 0,
    "e": 1,
    "d": 2,
    "c": 3,
    "s": 4,
    "z": 5,
    "a": 6,
    "q": 7
}

"""
Class that contains all the chunks as well as general world data. This includes
the name and seed.

It also includes methods for adding a new chunk, and rendering all chunks (this
method isn't actually used, as it isn't performant to render all chunks in the
chunk_list)
"""
class World:
    # Initializer
    def __init__(self, seed, name):
        self.seed = seed
        self.name = name
        self.chunk_list = []


    """
    Adds new chunk to self.chunk_list

    Pre:
    - 'new_pos' must be an integer

    Post:
    - Appends a new Chunk object to chunk_list with specified position
    """
    def newChunk(self, new_pos):
        self.chunk_list.append(Chunk(new_pos))


    """
    Renders all chunks within chunk_list

    Pre:
    - 'cam' must be Camera object, not be null or undefined
    - 'stdscr' must not be null or undefined

    Post:
    - Renders all chunks in the chunk_list, in the order they appear
    """
    def render(self, cam, stdscr):
        for c in self.chunk_list:
            c.render(cam.pos, stdscr)

# Create World
# TODO: load data from save file
w = World(0, 'new_world')


"""
Simple class that holds the position for the Camera object
"""
class Camera:
    def __init__(self):
        self.pos = p()


"""
Class that holds all data relating to the player character, including useful
positional values that make it easy to locate the player along the world and
individual chunks.

Along with this is input methods that allow the player to perform set actions.
"""
class Character:
    # Intializer
    def __init__(self):
        # Position of the player (y=50 is above the water)
        self.pos = p(y=50)
        # Current chunk the player is within
        self.current_chunk = 0
        # Chunk index of the chunk the player is within
        self.current_chunk_index = 0
        # Chunk index to the left of current_chunk
        self.left_chunk_index = 0
        # Chunk index to the right of the current_chunk
        self.right_chunk_index = 0
        # Current position along the curent chunk (y can be ignored)
        self.current_chunk_pos = p(
            x=math.floor(self.pos.x % 16), y=self.pos.y)
        # List of all chunks (used instead of world.chunk_list)
        self.chunk_list = []
        # Tile ID of tile to place when using the placeTile method
        self.equipped_tile = 0


    """
    Simply attempts to render the player character relative to the world origin
    and a set offset (often the camera position)

    Pre:
    - Offset must have a pos attribute
    - stdscr must not be null or undefined

    Post:
    - The player will either get rendered somewhere on the screen or simply
    won't (this won't happen as the Camera is centered on the player)
    """
    def render(self, offset, stdscr):
        try:
            stdscr.addstr(self.pos.y + offset.y, self.pos.x + offset.x, '☺')
        except:
            pass


    """
    Get's chunk index relative to a chunk + offset

    Pre:
    - chunk_id must be an int
    - offset must be an int

    Post:
    - Returns index of chunk who's position is chunk.pos + offset
    """
    def getAdjacentChunk(self, chunk_id, offset):
        return self.getIndexOfChunk(chunk_id + offset)


    """
    Check for specific tile at a position within a chunk

    Pre:
    - tile_index must be a positive number that isn't greater than the length of
      the tile_list in tiles.py
    - chunk_index must be an int
    - pos must be a Coord object

    Post:
    - Return True if the tile exists at the position, return False otherwise
    """
    def checkForTileInChunk(self, tile_index, chunk_index, pos):
        if (self.chunk_list[chunk_index].data[u.coordToIndex(p(y=pos.y, x=pos.x))] == tile_index):
            return True
        return False


    """
    Get the isSolid attribute of a tile at a position within a chunk

    Pre:
    - chunk_index must be int
    - pos must be a Coord object

    Post:
    - Return the isSolid attribute of the tile at the position
    """
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
                        self.pos.addX(-1); self.pos.addY(-1)
                # Anywhere in between
                else:
                    if (not self.collisionCheck(self.current_chunk_index, p(x=self.current_chunk_pos.x-1, y=self.pos.y))):
                        self.pos.addX(-1)
                    elif (not self.collisionCheck(self.current_chunk_index, p(x=self.current_chunk_pos.x-1, y=self.pos.y-1))):
                        self.pos.addX(-1); self.pos.addY(-1)
            elif (_dir == 1):
                # On right edge of chunk
                if (self.current_chunk_pos.x == 15):
                    if (not self.collisionCheck(self.right_chunk_index, p(y=self.pos.y, x=0))):
                        self.pos.addX(1)
                    elif (not self.collisionCheck(self.right_chunk_index, p(y=self.pos.y-1, x=0))):
                        self.pos.addX(1); self.pos.addY(-1)
                # Anywhere in between
                else:
                    if (not self.collisionCheck(self.current_chunk_index, p(x=self.current_chunk_pos.x+1, y=self.pos.y))):
                        self.pos.addX(1)
                    elif (not self.collisionCheck(self.current_chunk_index, p(x=self.current_chunk_pos.x+1, y=self.pos.y-1))):
                        self.pos.addX(1); self.pos.addY(-1)
        # If tile below player is air, just make player fall
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
chunk_render_distance = 2

# Pregenerating chunk
for i in range(-abs(chunk_gen_distance + 5), abs(chunk_gen_distance + 5)):
    w.newChunk(i)


def curses_main(stdscr):
    stdscr.clear()
    curses.noecho()
    rows, cols = stdscr.getmaxyx()

    # Intializing all the colors for curses
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

        # Generating chunk
        '''
        if (plr.pos.x % 15 == 0):
            new_chunk = math.floor((plr.pos.x) / 15)

            if (plr.getIndexOfChunk(new_chunk+chunk_gen_distance) == -1):
                w.newChunk(new_chunk+chunk_gen_distance)
            if (plr.getIndexOfChunk(new_chunk - chunk_gen_distance - 1) == -1):
                w.newChunk(new_chunk - chunk_gen_distance - 1)
        '''

        stdscr.clear()
        #w.render(cam, stdscr)

        # Chunk rendering
        for i in range(-abs(chunk_render_distance), abs(chunk_render_distance + 1)):
            w.chunk_list[plr.getAdjacentChunk(
                plr.current_chunk, i)].render(cam.pos, stdscr)

        plr.render(cam.pos, stdscr)

        stdscr.refresh()

        stdscr.addstr(0, 0, 'X:' + str(plr.pos.x))
        stdscr.addstr(1, 0, 'Y:' + str(plr.pos.y))
        stdscr.addstr(2, 0, 'CHUNK:' + str(plr.current_chunk) +
                      " - " + str(plr.current_chunk_pos.x) + "/15")

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

        # Iterates over all possible directions to check for placing
        # NOTE: Heavily reduces boilerplate
        for key in directions:
            if (k == ord(key)):
                plr.plrPlaceTile(directions[key])

        cam.pos.x = -plr.pos.x + int(cols / 2)
        cam.pos.y = -plr.pos.y + int(rows / 2)
    stdscr.refresh()


curses.wrapper(curses_main)

print(len(w.chunk_list))

sl.saveWorld(w, w.name)
