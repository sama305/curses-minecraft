import json
import interpreter

save_root = '../save_data/'

def saveChunk(c):
    c_data = interpreter.convertChunk(c)

    return [c.chunk_pos, c_data]

def saveWorld(w, n):
    file_name = save_root + n + '.json'

    saved_chunks = []
    for c in w.chunk_list:
        saved_chunks.append(saveChunk(c))
    
    data = {
        'seed': w.seed,
        'name': n,
        'chunk_data': saved_chunks
    }

    with open(file_name, 'w') as _file:
        _file.write(json.dumps(data, sort_keys=True, indent=4))

    _file.close()

