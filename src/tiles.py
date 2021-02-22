class Tiles:
    class Tile:
        def __init__(self, name, texture, color_pair=1):
            self.name = name
            self.texture = texture
            self.color_pair = color_pair

    tile_list = [
        Tile('air', ' '),       # 0
        Tile('grass','#', 2),      # 1
        Tile('dirt','~', 3),       # 2
        Tile('shale', '░'),     # 3
        Tile('gneiss', '▒'),    # 4
        Tile('slate', '▓'),     # 5
        Tile('granite', '█'),   # 6
        Tile('basalt', ' ='),    # 7
        Tile('bedrock','Ø'),    # 8
        Tile('leaves', '░', 2),    # 9
        Tile('log', '║', 4),        # 10
        Tile('ladder', '╫'),
        Tile('lava', '$', 5)
    ]

