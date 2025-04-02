# -*- coding: utf-8 -*-

import curses
import math
import saveload as sl
import generation as g
import util as u
import random as r
from tiles import Tiles as t
from coord import Coord as p
from chunk import Chunk
from character import Character
import os
import json


interact_directions = {
    "w": (-1, 0),
    "e": (-1, 1),
    "d": (0, 1),
    "c": (1, 1),
    "x": (1, 0),
    "z": (1, -1),
    "a": (0, -1),
    "q": (-1, -1),
    "s": (0, 0)
}

move_directions = {
    curses.KEY_LEFT: (0, -1),
    curses.KEY_RIGHT: (0, 1),
    curses.KEY_UP: (-1, 0),
    curses.KEY_DOWN: (1, 0)
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
        self.chunk_list.append(Chunk(new_pos, self.seed))


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




cam = Camera()

plr = Character()

chunk_gen_distance = 3
chunk_render_distance = 2

# Pregenerating chunk
#for i in range(-abs(chunk_gen_distance + 5), abs(chunk_gen_distance + 5)):


menu_options = ["Start new game"]
def initialize_menu():
	file_list = os.listdir("./save_data/")
	for f in file_list:
		menu_options.append(f)


def curses_main(stdscr):
    stdscr.clear()
    stdscr.timeout(1)
    curses.noecho()
    curses.curs_set(0)
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
    curses.init_pair(8, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(9, curses.COLOR_YELLOW, curses.COLOR_RED)
    curses.init_pair(10, curses.COLOR_GREEN, curses.COLOR_BLUE)
    curses.init_pair(11, curses.COLOR_BLACK, curses.COLOR_WHITE)

    author = "Samuel Anderson"
    game_title = "Curses-craft (working title)"
    selected = 0

    initialize_menu()

    # +------------------------------------------------------+
    # |                      MENU LOOP!                      |
    # +------------------------------------------------------+
    while (True):
        stdscr.refresh()
        stdscr.addstr(1, math.floor(cols / 2) - math.floor(len(game_title) / 2), game_title)
        stdscr.addstr(rows - 2, math.floor(cols / 2) - math.floor(len("By " + author) / 2), "By " + author)

        for i in range(len(menu_options)):
            current_option = menu_options[i]
            if i != 0:
                current_option = "Load: " + current_option

            if i == selected:
                stdscr.addstr(math.floor(rows / 2) + i - math.floor(len(menu_options) / 2), math.floor(cols / 2) - math.floor(len(current_option) / 2), current_option, curses.color_pair(11))
            else:
                stdscr.addstr(math.floor(rows / 2) + i - math.floor(len(menu_options) / 2), math.floor(cols / 2) - math.floor(len(current_option) / 2), current_option)


        k = stdscr.getch()
        if k == ord("q"):
            crash = True
        elif k == curses.KEY_UP:
            selected = selected - 1
            if selected < 0:
                selected = len(menu_options) - 1
        elif k == curses.KEY_DOWN:
            selected = selected + 1
            if selected > len(menu_options) - 1:
                selected = 0
        # Select
        elif k == 10:

            if selected != 0:
                stdscr.addstr(math.floor(rows / 2) + i - math.floor(len(menu_options) / 2 - 2), math.floor(cols / 2) - math.floor(len("Loading...") / 2), "Loading...")
                stdscr.refresh()

                with open("./save_data/" + menu_options[selected]) as f:
                    data = json.load(f)

                w.name = data['name']
                w.seed = data['seed']
                plr.pos.x = data['player_pos'][0]
                plr.pos.y = data['player_pos'][1]
                plr.equipped_tile = data['player_equipped_tile']

                w.chunk_list = sl.loadWorld(data)
            # New Game
            else:
                stdscr.addstr(math.floor(rows / 2) + i - math.floor(len(menu_options) / 2 - 2), math.floor(cols / 2) - math.floor(len("Creating world...") / 2), "Creating world...")
                stdscr.refresh()

                w.name = "world_" + str(len(os.listdir("./save_data/")) + 1)
                w.seed = r.randint(0, 999)
                [w.newChunk(i) for i in range(-4, 4)]
            break


# +------------------------------------------------------+
# |                      MAIN LOOP!                      |
# +------------------------------------------------------+
    show_hud = True
    while (True):
        plr.update(w.chunk_list)

        # Generating chunk
        if (plr.pos.x % 15 == 0):
            new_chunk = math.floor((plr.pos.x) / 15)

            if (plr.getIndexOfChunk(new_chunk+chunk_gen_distance) == -1):
                w.newChunk(new_chunk+chunk_gen_distance)
            if (plr.getIndexOfChunk(new_chunk - chunk_gen_distance - 1) == -1):
                w.newChunk(new_chunk - chunk_gen_distance - 1)

        stdscr.clear()
        #w.render(cam, stdscr)

        # Chunk rendering
        for i in range(-abs(chunk_render_distance), abs(chunk_render_distance + 1)):
            w.chunk_list[plr.getAdjacentChunk(
                plr.current_chunk, i)].render(cam.pos, stdscr)

        plr.render(cam.pos, stdscr)

        stdscr.refresh()

        if (show_hud):
            stdscr.addstr(0, 0, 'X:' + str(plr.pos.x))
            stdscr.addstr(1, 0, 'Y:' + str(plr.pos.y))
            stdscr.addstr(2, 0, 'CHUNK:' + str(plr.current_chunk) +
                          " - " + str(plr.current_chunk_pos + 1) + "/16")
            stdscr.addstr(3, 0, 'SELECTED TILE: [' + str(plr.equipped_tile) + ']')
            stdscr.addstr(3, 18 + len(str(plr.equipped_tile)), t.tile_list[plr.equipped_tile].texture,
                                 curses.color_pair(t.tile_list[plr.equipped_tile].color_pair))
            stdscr.addstr(3, 20 + len(str(plr.equipped_tile)), t.tile_list[plr.equipped_tile].name)

        k = stdscr.getch()

        if (k == ord('Q')):
            break

        if (k == ord('S')):
            sl.saveWorld(w, plr)
            stdscr.addstr(0, math.floor(cols / 2), "Saving...")
            stdscr.refresh()
        # Updates the screen
        plr.movePlr((2, 2))

        if (k == ord('1')):
            plr.equipped_tile -= 1
            if (plr.equipped_tile < 0):
                plr.equipped_tile = len(t.tile_list) - 1
        if (k == ord('2')):
            plr.equipped_tile += 1
            if (plr.equipped_tile > len(t.tile_list) - 1):
                plr.equipped_tile = 0
        if (k == ord('3')):
            plr.equipped_tile = 0

        if (k == ord('h')):
            show_hud = not show_hud
            stdscr.refresh()

        # Iterates over all possible directions to check for placing and moving
        # NOTE: Heavily reduces boilerplate
        for key in interact_directions:
            if (k == ord(key)):
                plr.plrPlaceTile(interact_directions[key])

        for key in move_directions:
            if (k == key):
                plr.movePlr(move_directions[key])

        cam.pos.x = -plr.pos.x + int(cols / 2)
        cam.pos.y = -plr.pos.y + int(rows / 2)
    stdscr.refresh()


curses.wrapper(curses_main)

sl.saveWorld(w, plr)
