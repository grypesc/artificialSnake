
'''
import types

class AgentStrategy:
    def __init__(self, func = None):
        self.name = 'Strategy Example 0'
        if func is not None:
            self.execute = types.MethodType(func, self)

    def execute(self):
        print(self.name)

    def reduceX(self): 
        print(self.name + 'from execute 1')

    def reduceY(self):
        print(self.name + 'from execute 2')
'''

class Agent:
    def __init__(self, game):
        self.game = game
        self._isTuringingAround = False



    def getDistanceToSnack(self):
        deltaX = self.game.snake.body[0].position.x - self.game.snack.position.x
        deltaY = self.game.snake.body[0].position.y - self.game.snack.position.y
        return (deltaX,deltaY)
    def update(self):
        if self._isTuringingAround == True:
            self.__turnAround()
            self._isTuringingAround = False
        
        velocity = self.game.snake.velocity
        (x,y)=self.getDistanceToSnack()
        
        if x == 0: # the snake is either above or below the snack
            if y > 0: # the snake is below the snack
                if velocity.dir == 'Left':
                    self.game.snake.velocity = velocity.turnRight()
                elif velocity.dir == 'Right':
                    self.game.snake.velocity = velocity.turnLeft()
                elif velocity.dir == 'Down':
                    self.__turnAround()
                    self._isTuringingAround=True
            else: # the snake is above the snack
                if velocity.dir == 'Left':
                    self.game.snake.velocity = velocity.turnLeft()
                elif velocity.dir == 'Right':
                    self.game.snake.velocity = velocity.turnRight()
                elif velocity.dir == 'Up':
                    self.__turnAround()
                    self._isTuringingAround=True
        elif y == 0: # the snake is either to the right or to the left to the snack
            if x > 0: # the snake is to the left to the snack
                if velocity.dir == 'Up':
                    self.game.snake.velocity = velocity.turnRight()
                elif velocity.dir == 'Down':
                    self.game.snake.velocity = velocity.turnLeft()
                elif velocity.dir == 'Right':
                    self.__turnAround()
                    self._isTuringingAround=True
            else: # the snake is to the right to the snack
                if velocity.dir == 'Down':
                    self.game.snake.velocity = velocity.turnRight()
                elif velocity.dir == 'Up':
                    self.game.snake.velocity = velocity.turnLeft()
                elif velocity.dir == 'Left':
                    self.__turnAround()
                    self._isTuringingAround=True
        else: #there is no straight way to the snack
            if abs(x) > abs (y):
                if x > 0:
                    if velocity.dir == 'Up':
                        self.game.snake.velocity = velocity.turnRight()
                    elif velocity.dir == 'Down':
                        self.game.snake.velocity = velocity.turnLeft()
                    elif velocity.dir == 'Right':
                        self.__turnAround()
                        self._isTuringingAround=True             
                elif x < 0:
                    if velocity.dir == 'Down':
                        self.game.snake.velocity = velocity.turnRight()
                    elif velocity.dir == 'Up':
                        self.game.snake.velocity = velocity.turnLeft()
                    elif velocity.dir == 'Left':
                        self.__turnAround()
                        self._isTuringingAround=True
                elif y > 0:
                    if velocity.dir == 'Left':
                        self.game.snake.velocity = velocity.turnRight()
                    elif velocity.dir == 'Right':
                        self.game.snake.velocity = velocity.turnLeft()
                    elif velocity.dir == 'Down':
                        self.__turnAround()
                        self._isTuringingAround=True
                else:
                    if velocity.dir == 'Left':
                        self.game.snake.velocity = velocity.turnLeft()
                    elif velocity.dir == 'Right':
                        self.game.snake.velocity = velocity.turnRight()
                    elif velocity.dir == 'Up':
                        self.__turnAround()
                        self._isTuringingAround=True
            elif abs(x) < abs(y):
                if y > 0:
                    if velocity.dir == 'Left':
                        self.game.snake.velocity = velocity.turnRight()
                    elif velocity.dir == 'Right':
                        self.game.snake.velocity = velocity.turnLeft()
                    elif velocity.dir == 'Down':
                        self.__turnAround()
                        self._isTuringingAround=True
                elif y < 0:
                    if velocity.dir == 'Left':
                        self.game.snake.velocity = velocity.turnLeft()
                    elif velocity.dir == 'Right':
                        self.game.snake.velocity = velocity.turnRight()
                    elif velocity.dir == 'Up':
                        self.__turnAround()
                        self._isTuringingAround=True
                elif x > 0:
                    if velocity.dir == 'Up':
                        self.game.snake.velocity = velocity.turnRight()
                    elif velocity.dir == 'Down':
                        self.game.snake.velocity = velocity.turnLeft()
                    elif velocity.dir == 'Right':
                        self.__turnAround()
                        self._isTuringingAround=True
                else:
                    if velocity.dir == 'Down':
                        self.game.snake.velocity = velocity.turnRight()
                    elif velocity.dir == 'Up':
                        self.game.snake.velocity = velocity.turnLeft()
                    elif velocity.dir == 'Left':
                        self.__turnAround()
                        self._isTuringingAround=True

                

        print(str(x)+" "+str(y)+" "+self.game.snake.velocity.dir)
        input()
        
    def __turnAround(self):
        self.game.snake.velocity = self.game.snake.velocity.turnLeft()