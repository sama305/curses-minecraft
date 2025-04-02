import json
import interpreter
from chunk import Chunk
import os

save_root = './save_data/'

def saveChunk(c):
    c_data = interpreter.arrToData(c)

    return [c.chunk_pos, c_data]

def loadChunk(d):
    c_data = interpreter.dataToArr(d)

    return c_data

def saveWorld(w, p):
    file_name = save_root + w.name + '.json'

    saved_chunks = []
    for c in w.chunk_list:
        saved_chunks.append(saveChunk(c))

    data = {
        'seed': w.seed,
        'name': w.name,
        'chunk_data': saved_chunks,
        'player_pos': [p.pos.x, p.pos.y],
        'player_equipped_tile': p.equipped_tile
    }

    # make save_data dir if necessary
    os.makedirs('./save_data')
    with open(file_name, 'w+') as _file:
        _file.write(json.dumps(data, sort_keys=True, indent=4))

    _file.close()

def loadWorld(data):
    chunk_list = []

    for d in data['chunk_data']:
        c = Chunk(int(d[0]), int(data['seed']))
        c.data = loadChunk(d[1])
        chunk_list.append(c)

    return chunk_list
