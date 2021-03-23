class Tiles:
    class Tile:
        def __init__(self, name, texture, color_pair=1, isSolid=True, isClimbable=False):
            self.name = name
            self.texture = texture
            self.color_pair = color_pair
            self.isSolid = isSolid
            self.isClimbable = isClimbable

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
        Tile('leaves', '░', 2, isSolid=False, isClimbable=True),    # 9
        Tile('log', '║', 3, isSolid=False, isClimbable=True),        # 10
        Tile('ladder', '╫', 3, isSolid=False, isClimbable=True), #11
        Tile('lava', '░', 4, isSolid=False, isClimbable=True), # 12
        Tile('begonia', '♣', 5, isSolid=False), # 13
        Tile('rose', '♠', 4, isSolid=False), # 14
        Tile('poppy', '☼', 6, isSolid=False), # 15
        Tile('wood', '=', 3), # 16
        Tile('redwood', 'H', 3, isSolid=False, isClimbable=True), # 17
        Tile('gold', '§', 3), # 18
        Tile('diamond', '♦', 6), # 19
        Tile('loam', '~', 7), # 20
        Tile('plant stem', '|', 2, isSolid=False), # 21
        Tile('snowy grass', '#'), # 22
        Tile('snowy leaves', '░', isSolid=False), # 23
        Tile('snowy layer', '_', isSolid=False), # 24
        Tile('door', '|', 3, isSolid=False, isClimbable=True), # 25
        Tile('solid log', '║', 3), # 26
        Tile('table', '╥', 3, isSolid=False), # 27
        Tile('friend 1', '☻', 6, isSolid=False, isClimbable=True), # 28
        Tile('friend 2', '☺', 4, isSolid=False, isClimbable=True), # 29
        Tile('red concrete', '█', 4), # 30
        Tile('cyan concrete', '█', 6), # 31
        Tile('green concrete', '█', 2), # 32
        Tile('white concrete', '█', 1), # 33
        Tile('magenta concrete', '█', 5), # 34
        Tile('yellow concrete', '█', 3), # 35
        Tile('blue concrete', '█', 8), # 36
        Tile('heckstone', '#', 9), # 37
        Tile('heckslate', '░', 9), # 38
        Tile('firelily', '♀', 4, isSolid=False), # 39
        Tile('water', '░', 8, isSolid=False, isClimbable=True), # 40
        Tile('kelp', '⌠', 2, isSolid=False, isClimbable=True), # 41
        Tile('seaweed left', ')', 2, isSolid=False, isClimbable=True), # 42
        Tile('seaweed right', '(', 2, isSolid=False, isClimbable=True), # 43
        Tile('boat left', '\\', 3, isSolid=False, isClimbable=True), # 44
        Tile('boat right', '/', 3, isSolid=False, isClimbable=True), # 45
        Tile('wood floor', '_', 3, isSolid=False, isClimbable=True), # 46
        Tile('flag', '>', 4, isSolid=False), # 47
        Tile('cod', '◄', 1, isSolid=False, isClimbable=True), # 48
        Tile('salmon', '»', 6, isSolid=False, isClimbable=True), # 49
        Tile('bass', '≤', 4, isSolid=False, isClimbable=True), # 50
        Tile('snowman head', '☻', 1, isSolid=False), # 51
        Tile('snowman torso', 'O', 1, isSolid=False), # 


    ]
