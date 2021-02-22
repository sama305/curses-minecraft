from perlin_noise import PerlinNoise
import math

start_height = 10

def generateChunk(offset):
    chunk = []
    noise = PerlinNoise(octaves=2)
    
    for a in range(4096):
        chunk.append(0)

    x = 16
    for i in range(x):
        foo = math.floor(noise(i / x) * 10)
        chunk[i + 16 * (foo + start_height)] = 1
        for j in range(foo + start_height + 1, 255):
            chunk[i + 16 * j] = 2
        chunk[i + 16 * 255] = 3

    return chunk