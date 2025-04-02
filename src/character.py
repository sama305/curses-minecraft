from tiles import Tiles as t
from coord import Coord as p
import generation as g
import math
import util as u

class Character:
    # Intializer
    def __init__(self):
        # Position of the player (y=50 is above the water)
        self.pos = p(y=50)
        # Current chunk the player is within
        self.current_chunk = 0
        # Chunk index of the chunk the player is within
        self.current_chunk_index = 0
        # Chunk index to the left of current_chunk
        self.left_chunk_index = 0
        # Chunk index to the right of the current_chunk
        self.right_chunk_index = 0
        # Current position along the curent chunk (y can be ignored)
        self.current_chunk_pos = math.floor(self.pos.x % 16)
        # List of all chunks (used instead of world.chunk_list)
        self.chunk_list = []
        # Tile ID of tile to place when using the placeTile method
        self.equipped_tile = 0


    """
    Simply attempts to render the player character relative to the world origin
    and a set offset (often the camera position)

    Pre:
    - Offset must have a pos attribute
    - stdscr must not be null or undefined

    Post:
    - The player will either get rendered somewhere on the screen or simply
    won't (this won't happen as the Camera is centered on the player)
    """
    def render(self, offset, stdscr):
        try:
            stdscr.addstr(self.pos.y + offset.y, self.pos.x + offset.x, '☺')
        except:
            pass


    """
    Get's chunk index relative to a chunk + offset

    Pre:
    - chunk_id must be an int
    - offset must be an int

    Post:
    - Returns index of chunk who's position is chunk.pos + offset
    """
    def getAdjacentChunk(self, chunk_id, offset):
        return self.getIndexOfChunk(chunk_id + offset)


    """
    Check for specific tile at a position within a chunk

    Pre:
    - tile_index must be a positive number that isn't greater than the length of
      the tile_list in tiles.py
    - chunk_index must be an int
    - pos must be a Coord object

    Post:
    - Return True if the tile exists at the position, return False otherwise
    """
    def checkForTileInChunk(self, tile_index, chunk_index, pos):
        if (self.chunk_list[chunk_index].data[u.coordToIndex(p(y=pos.y, x=pos.x))] == tile_index):
            return True
        return False


    """
    Get the isSolid attribute of a tile at a position within a chunk

    Pre:
    - chunk_index must be int
    - pos must be a Coord object

    Post:
    - Return the isSolid attribute of the tile at the position
    """
    def collisionCheck(self, chunk_index, pos):
        return t.tile_list[self.chunk_list[chunk_index].data[u.coordToIndex(p(y=pos.y, x=pos.x))]].isSolid

    def bedrockCheck(self, chunk_index, pos):
        return self.chunk_list[chunk_index].data[u.coordToIndex(p(y=pos.y, x=pos.x))] == 8

    def climbableCheck(self, chunk_index, pos):
        return t.tile_list[self.chunk_list[chunk_index].data[u.coordToIndex(p(y=pos.y, x=pos.x))]].isClimbable

    def getIndexOfChunk(self, _id):
        for i in range(len(self.chunk_list)):
            if (self.chunk_list[i].chunk_pos == _id):
                return i
        return -1


    def update(self, chunk_list):
        self.current_chunk = math.floor(self.pos.x / 16)
        self.current_chunk_pos = math.floor(self.pos.x % 16)
        self.chunk_list = chunk_list

        self.current_chunk_index = self.getIndexOfChunk(
            self.current_chunk)
        self.left_chunk_index = self.getAdjacentChunk(
            self.current_chunk, -1)
        self.right_chunk_index = self.getAdjacentChunk(
            self.current_chunk, 1)


    def movePlr(self, _dir):
        if (self.collisionCheck(self.current_chunk_index, p(x=self.current_chunk_pos, y=self.pos.y + 1))
         or self.climbableCheck(self.current_chunk_index, p(x=self.current_chunk_pos, y=self.pos.y))):

            chunk_to_check = self.current_chunk_index
            if (_dir[0] == 0):
                pos_to_check = self.current_chunk_pos + _dir[1]

                if (_dir[1] == 1 and self.current_chunk_pos == 15):
                    pos_to_check = 0
                    chunk_to_check = self.right_chunk_index
                elif (_dir[1] == -1 and self.current_chunk_pos == 0):
                    pos_to_check = 15
                    chunk_to_check = self.left_chunk_index

                if (not self.collisionCheck(chunk_to_check, p(x=pos_to_check, y=self.pos.y))):
                    self.pos.addX(_dir[1])
                elif (not self.collisionCheck(chunk_to_check, p(x=pos_to_check, y=self.pos.y-1))):
                    self.pos.addX(_dir[1])
                    self.pos.addY(-1)

            elif (abs(_dir[0]) == 1):
                if (self.climbableCheck(chunk_to_check, p(x=self.current_chunk_pos, y=self.pos.y))
                and self.climbableCheck(chunk_to_check, p(x=self.current_chunk_pos, y=self.pos.y + _dir[0]))):
                    self.pos.addY(_dir[0])

        # If tile below player is air, just make player fall
        else:
            self.pos.y += 1


    def plrPlaceTile(self, _dir):
        place_pos = p(x=self.current_chunk_pos + _dir[1], y=self.pos.y + _dir[0])
        chunk_to_check = self.current_chunk_index

        # bedrock can't be placed on
        if self.bedrockCheck(chunk_to_check, place_pos):
            return

        if (_dir[1] == 1 and self.current_chunk_pos == 15):
            place_pos.x = 0
            chunk_to_check = self.right_chunk_index
        elif (_dir[1] == -1 and self.current_chunk_pos == 0):
            place_pos.x = 15
            chunk_to_check = self.left_chunk_index

        g.placeTile(self.chunk_list[chunk_to_check].data, place_pos, self.equipped_tile)
