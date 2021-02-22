class Coord:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def changePos(self,x,y):
        self.x = x
        self.y = y
    
    def addX(self, inc):
        self.x += inc

    def addY(self, inc):
        self.y += inc