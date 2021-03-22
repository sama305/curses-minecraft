# -*- coding: utf-8 -*-

from perlin_noise import PerlinNoise
import math
from tiles import Tiles
import random
from coord import Coord

start_height = 64

# Structures:
#
#  ░░░
# ░░░░░
#   ║
#   ║
#
#   ░
#  ░░░
# ░░║░░
#   ║
#

structure_maps = [
    {
        'name': 'oak_tree',
        'map': [
            [0, 9, 9, 9, 0],
            [9, 9, 9, 9, 9],
            [0, 0, 10, 0, 0],
            [0, 0, 10, 0, 0]
        ],
        'origin': Coord(x=2, y=3)
    },
    {
        'name': 'oak_tree',
        'map': [
            [0, 0, 9, 0, 0],
            [0, 9, 9, 9, 0],
            [9, 9, 10, 9, 9],
            [0, 0, 10, 0, 0],
            [0, 0, 10, 0, 0]
        ],
        'origin': Coord(x=2, y=4)
    },
    {
        'name': 'hut',
        'map': [
            [0, 16, 16, 16, 16, 16, 0],
            [0, 16, 10, 10, 10, 16, 0],
            [0, 16, 10, 10, 10, 16, 0],
            [0, 10, 10, 10, 10, 10, 0],
            [1, 16, 16, 16, 16, 16, 1],
            [2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2],
        ],
        'origin': Coord(x=2, y=4)
    },
    {
        'name': 'rock',
        'map': [
            [0, 4, 4],
            [4, 4, 4],
        ],
        'origin': Coord(1, 1)
    }
]

def placeTile(chunk, pos, tile):
    chunk[pos.x + 16 * pos.y] = tile

def getTile(chunk, pos):
    return chunk[pos.x + 16 * pos.y]

def generateStructure(chunk, structure_index, start_point, airBlocksDelete=False):
    # TODO
    # Make generated structures go into chunks
    # actually make things going across chunks more natural and easy to do
    _map = structure_maps[structure_index]['map']
    origin = structure_maps[structure_index]['origin']

    for i in range(len(_map)):
        for j in range(len(_map[0])):
            pos_rel_to_origin = Coord(origin.x - j, origin.y - i)
            pos_rel_to_start = Coord(start_point.x - pos_rel_to_origin.x, start_point.y - pos_rel_to_origin.y)

            if (airBlocksDelete or (not airBlocksDelete and _map[i][j] != 0)):
                placeTile(chunk, pos_rel_to_start, _map[i][j])


def generateChunk(offset):
    chunk = []
    noise = PerlinNoise(octaves=1)

    chunk = [0 if n<1072 else (4 if n<4080 else 8) for n in range(4096)]

    x = 16
    occupied = False
    for i in range(x):
        noise_offset = math.floor(noise(i / x) * 10)
        col_height = noise_offset + start_height

        placeTile(chunk, Coord(i + (math.floor(noise(col_height / x) * 10)), col_height), 1)

        current_layer = 2
        for j in range(col_height + 1, 255):
            #normal = j - (col_height)
            if (j / (40.0 + noise_offset) % 1 == 0):
                current_layer += 1

            if (current_layer == 7):
                current_layer = 0

            placeTile(chunk, Coord(i + math.floor(noise(j / x) * 10), j), current_layer)
        placeTile(chunk, Coord(i, 255), 8)
        for l in range(3):
            placeTile(chunk, Coord(i, 254 - l), 12)

        # Structure generation
        if (not occupied):
            if (random.randint(0, 100) < 1):
                occupied = True
                generateStructure(chunk, 2, Coord(8, col_height - 1), True)
                continue
            if ((i > 1 and i < 7) and random.randint(0, 100) < 30):
                generateStructure(chunk, random.randint(0, 1), Coord(i, col_height - 1))
                continue
            if ((i > 2 and i < 6) and random.randint(0, 100) < 5):
                generateStructure(chunk, 3, Coord(i, col_height - 1))
                continue
            if ((i > 1 and i < 7) and random.randint(0, 100) < 20):
                placeTile(chunk, Coord(i, col_height - 1), random.randint(13,15))
                continue

    return chunk

generateChunk(0)
