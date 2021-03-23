# -*- coding: utf-8 -*-

import math
from tiles import Tiles
import random
from coord import Coord
import util as u

import sys
sys.path.insert(1, '../lib/perlin-noise-1.7/perlin_noise/')
from perlin_noise import PerlinNoise

start_height = 64
snow_height = 50
water_height = 64

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
#   |>
# \_|_/
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
        'name': 'pine_tree',
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
    },
    {
        'name': 'giant_pine_tree',
        'map': [
            [0, 0, 0, 9, 0, 0, 0],
            [0, 0, 9, 9, 9, 0, 0],
            [0, 0, 9, 9, 9, 0, 0],
            [0, 9, 9, 9, 9, 9, 0],
            [0, 9, 9, 9, 9, 9, 0],
            [9, 9, 9, 9, 9, 9, 9],
            [9, 9, 9, 9, 9, 9, 9],
            [0, 9, 17, 17, 17, 9, 0],
            [0, 0, 17, 17, 17, 0, 0],
            [0, 0, 17, 17, 17, 0, 0],
            [0, 0, 17, 17, 17, 0, 0],
            [0, 0, 17, 17, 17, 0, 0],
            [0, 0, 17, 17, 17, 0, 0],
            [0, 0, 17, 17, 17, 0, 0],
            [0, 0, 17, 17, 17, 0, 0],
            [0, 0, 17, 17, 17, 0, 0],
            [0, 0, 17, 17, 17, 0, 0],
            [0, 0, 17, 17, 17, 0, 0],
            [0, 0, 17, 17, 17, 0, 0],
        ],
        'origin': Coord(x=2, y=18)
    },
    {
        'name': 'begonia_flower',
        'map': [
            [13],
            [21]
        ],
        'origin': Coord(x=0,y=1)
    },
    {
        'name': 'rose_flower',
        'map': [
            [14],
            [21]
        ],
        'origin': Coord(x=0,y=1)
    },
    {
        'name': 'poppy_flower',
        'map': [
            [15],
            [21]
        ],
        'origin': Coord(x=0,y=1)
    },
    {
        'name': 'small_boat',
        'map': [
            [0, 0, 25, 47, 0],
            [44, 46, 25, 46, 45]
        ],
        'origin': Coord(x=1,y=1)
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

            if (airBlocksDelete or chunk[u.coordToIndex(pos_rel_to_start)] == 24 or (not airBlocksDelete and _map[i][j] != 0)):
                placeTile(chunk, pos_rel_to_start, _map[i][j])


def generateChunk(chunk_pos, seed):
    # region = 16 chunks or 64 tiles
    # chunk = 16 tiles

    chunk = []
    chunk = [0 for n in range(4096)]

    region = 0
    regionPos = 0
    if (chunk_pos >= 0):
        region = math.floor(chunk_pos / 16)
        regionPos = chunk_pos % 16
    else:
        region = math.ceil((chunk_pos - 16) / 16)
        regionPos = chunk_pos % 16

    noise1 = PerlinNoise(octaves=1, seed=region + seed + 10)
    noise2 = PerlinNoise(octaves=4, seed=region + seed + 10)
    noise3 = PerlinNoise(octaves=8, seed=region + seed + 10)

    start_pos = regionPos * 16

    height_map = []
    for x in range(16):
        noise_val =         noise1([(x + start_pos)/256]) * 75
        noise_val += 0.75 * noise2([(x + start_pos)/256]) * 65
        noise_val += 0.5  * noise3([(x + start_pos)/256]) * 50

        height_map.append(math.floor(noise_val) + start_height)
        #height_map = [math.floor(noise([(x + start_pos)/64, 0.5, 1]) * 30) + start_height for x in range(16)]

    occupied = False
    for x in range(len(height_map)):
        # Grass
        placeTile(chunk, Coord(x, height_map[x]), 1)

        # Snow level
        if (height_map[x] < snow_height):
            placeTile(chunk, Coord(x, height_map[x]), 22)
            if (random.randint(1, 100) == 1):
                placeTile(chunk, Coord(x, height_map[x] - 3), 51)
                placeTile(chunk, Coord(x, height_map[x] - 2), 52)
                placeTile(chunk, Coord(x, height_map[x] - 1), 52)
            else:
                placeTile(chunk, Coord(x, height_map[x] - 1), 24)

        # Water levels
        if (height_map[x] > water_height):
            placeTile(chunk, Coord(x, height_map[x]), 2)
            for y in range(water_height, height_map[x]):
                placeTile(chunk, Coord(x, y), 40)
                if (random.randint(1,20) == 1):
                    placeTile(chunk, Coord(x, y), random.randint(48,50))
            # Seaweed/kelp
            if (random.randint(1,3) == 1):
                height = water_height + random.randint(1, height_map[x] - water_height + 1)
                for i in range(height, height_map[x]):
                    if (i % 2 == 0):
                        placeTile(chunk, Coord(x, i), 42)
                    else:
                        placeTile(chunk, Coord(x, i), 43)
            if (x > 3 and x < 13 and random.randint(1,70) == 1):
                generateStructure(chunk, 8, Coord(8, water_height - 1), False)

        for y in range(height_map[x] + 1, 255):
            if (y > 240):
                placeTile(chunk, Coord(x, y), 12)
            # Bedrock layer
            if (y > 252):
                placeTile(chunk, Coord(x, y), 8)
            # Heckstone layer
            elif (y > 182 + height_map[x]):
                placeTile(chunk, Coord(x, y), 37)
            # Hecklactite/Heckslate layer
            elif (y > 160 + height_map[x]):
                cave_val = noise3([(x + start_pos)/64 / 2, y/(256 - height_map[x])])
                if (abs(cave_val) > 0.001 * y):
                    placeTile(chunk, Coord(x, y), 38)
            # Basalt layer
            elif (y > 140 + height_map[x]):
                placeTile(chunk, Coord(x, y), 7)
                if (random.randint(0,100) < 1):
                    placeTile(chunk, Coord(x, y), 19)
            # Stalactite/Granite layer
            elif (y > 110 + height_map[x]):
                placeTile(chunk, Coord(x, y), 6)
                cave_val = noise3([(x + start_pos)/64, y/(256 - height_map[x])])
                if (abs(cave_val) < 0.001 * y):
                    placeTile(chunk, Coord(x, y), 0)
            # Slate layer
            elif (y > 90 + height_map[x]):
                placeTile(chunk, Coord(x, y), 5)
                if (random.randint(0,100) < 3):
                    placeTile(chunk, Coord(x, y), 18)
            # Cave/Gneiss layer
            elif (y > 30 + height_map[x]):
                placeTile(chunk, Coord(x, y), 4)
                cave_val = noise3([(x + start_pos)/64 / 2, y/(256 - height_map[x]) * 4])
                if (abs(cave_val) < 0.001 * (y % (256 - height_map[x]))):
                    placeTile(chunk, Coord(x, y), 0)
            # Shale layer
            elif (y > 5 + height_map[x]):
                placeTile(chunk, Coord(x, y), 3)
                if (random.randint(0,100) < 35):
                    placeTile(chunk, Coord(x, y), 4)
            # Dirt
            else:
                placeTile(chunk, Coord(x, y), 2)
                if (random.randint(0,100) < 20):
                    placeTile(chunk, Coord(x, y), 20)

        # Structure generation
        if (not occupied and height_map[x] > snow_height and height_map[x] < water_height):
            if (random.randint(0, 100) < 5):
                occupied = True
                generateStructure(chunk, 4, Coord(8, height_map[8]), False)
                continue
            if ((x > 1 and x < 7) and random.randint(0, 100) < 30):
                generateStructure(chunk, random.randint(0, 1), Coord(x, height_map[x] - 1))
                continue
            if ((x > 2 and x < 6) and random.randint(0, 100) < 5):
                generateStructure(chunk, 3, Coord(x, height_map[x] - 1))
                continue
            if ((x > 1 and x < 7) and random.randint(0, 100) < 75):
                generateStructure(chunk, random.randint(5, 7), Coord(x, height_map[x] - 1))
                continue

    return chunk
