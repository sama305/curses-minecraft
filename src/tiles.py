class Tiles:
    class Tile:
        def __init__(self, name, texture, color_pair=1, isSolid=True):
            self.name = name
            self.texture = texture
            self.color_pair = color_pair
            self.isSolid = isSolid

    tile_list = [
        Tile('air', ' ', isSolid=False),       # 0
        Tile('grass','#', 2),      # 1
        Tile('dirt','≈', 7),       # 2
        Tile('shale', '░'),     # 3
        Tile('gneiss', '▒'),    # 4
        Tile('slate', '▓'),     # 5
        Tile('granite', '█'),   # 6
        Tile('basalt', '='),    # 7
        Tile('bedrock','Ø'),    # 8
        Tile('leaves', '░', 2, isSolid=False),    # 9
        Tile('log', '║', 3, isSolid=False),        # 10
        Tile('ladder', '╫', isSolid=False),
        Tile('lava', '$', 4),
        Tile('begonia', '♣', 5, isSolid=False),
        Tile('rose', '♠', 4, isSolid=False),
        Tile('poppy', '☼', 6, isSolid=False),
        Tile('wood', '=', 3)
    ]
