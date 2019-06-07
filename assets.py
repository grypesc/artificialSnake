import math
class Point():
    def __init__(self,x,y):
        self.x = x;
        self.y = y;
    def distance (self, p2):
        return math.sqrt(math.pow(self.x-p2.x,2) + math.pow(self.y-p2.y,2))


class Velocity():
    def __init__(self,dir):
        self.dir = dir
        if(dir == "Up"):
            self.vX = 0
            self.vY = -1
        if(dir == "Down"):
            self.vX = 0
            self.vY = 1
        if(dir == "Right"):
            self.vX = 1
            self.vY = 0
        if(dir == "Left"):
            self.vX = -1
            self.vY = 0

    def turnRight(self):
        if(self.dir == "Up"): return Velocity("Right")
        if(self.dir == "Right"): return Velocity("Down")
        if(self.dir == "Down"): return Velocity("Left")
        if(self.dir == "Left"): return Velocity("Up")

    def turnLeft(self):
        if(self.dir == "Up"): return Velocity("Left")
        if(self.dir == "Right"): return Velocity("Up")
        if(self.dir == "Down"): return Velocity("Right")
        if(self.dir == "Left"): return Velocity("Down")
