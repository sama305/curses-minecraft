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
#
#
#
#
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
    noise = PerlinNoise(octaves=2)
    
    for a in range(4096):
        chunk.append(0)

    x = 16
    for i in range(x):
        noise_offset = math.floor(noise(i / x) * 10)
        col_height = noise_offset + start_height

        placeTile(chunk, Coord(i, col_height), 1)

        current_layer = 2
        for j in range(col_height + 1, 255):
            normal = j - (col_height)
            if (j / (40.0 + noise_offset) % 1 == 0):
                current_layer += 1
            
            if (current_layer == 7):
                current_layer = 0
            
            placeTile(chunk, Coord(i, j), current_layer)
        placeTile(chunk, Coord(i, 255), 8)
        for l in range(3):
            placeTile(chunk, Coord(i, 254 - l), 12)

        if (i == 8 and random.randint(0, 100) < 40):
            generateStructure(chunk, 0, Coord(i, col_height - 1))

    return chunk

generateChunk(0)