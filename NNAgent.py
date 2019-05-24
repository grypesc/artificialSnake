import math
import random
import numpy as np
import pandas as pd
from sklearn.neural_network import MLPClassifier
from assets import *

class Agent:
    def __init__(self, game):
        self.game = game
        self.previousStepScore = 0;
        self.neuralNetwork = MLPClassifier(solver='adam', alpha=1e-6,hidden_layer_sizes=(5, 5), random_state=1)
        self.dataFrame = 0
        self.createDataset()

    def createDataset(self):
        data = np.array([['index', 'isSnackOnTheLeft', 'isSnackOnTheRight', 'isSnackHigher', 'isSnackLower',
         'distanceToSnack', 'isLeftClear', 'isRightClear', 'isForwardClear'],
                        ['1',0,0,0,0,0,0,0,0]])
        self.dataFrame=pd.DataFrame(data=data[1:,1:],
                          index=data[1:,0],
                          columns=data[0,1:])
        self.dataFrame.to_csv('data.csv')

    def stepEvaluation(self):
        pass

    def getDistanceToSnack(self):
        deltaX = game.snake.body[0].position.x - game.snack.position.x
        deltaY = game.snake.body[0].position.y - game.snack.position.y
        return math.sqrt(math.pow(deltaX,2) + math.pow(deltaY,2))

    def isSquareClear(self, direction):
        v = Velocity(self.game.snake.velocity.dir)
        if(direction == "Right"): v = v.turnRight()
        if(direction == "Left"): v = v.turnLeft()
        headPosition = self.game.snake.body[0].position
        square = Point(headPosition.x + v.vX*self.game.map.squareSideLength, headPosition.y + v.vY*self.game.map.squareSideLength)
        # if square.x >= self.game.map.width: square.x = 0;
        # if square.x < 0: square.x = self.game.map.width - self.game.map.squareSideLength;
        # if square.y >= self.game.map.height: square.y = 0;
        # if square.y < 0: square.y = self.game.map.height - self.game.map.squareSideLength;
        if square.x == 0 or square.x == self.game.map.width-self.game.map.squareSideLength:
            return 0
        if square.y == 0 or square.y == self.game.map.height-self.game.map.squareSideLength:
            return 0
        for snakeSquare in self.game.snake.body[1:]:
            if snakeSquare.position.x == square.x and snakeSquare.position.y == square.y:
                return 0
        return 1

    def isSnackOnTheRight(self):
        return self.game.snack.position.x>self.game.snake.body[0].position.x

    def isSnackOnTheLeft(self):
        return self.game.snack.position.x<self.game.snake.body[0].position.x

    def isSnackHigher(self):
        return self.game.snack.position.y<self.game.snake.body[0].position.y

    def isSnackLower(self):
        return self.game.snack.position.y>self.game.snake.body[0].position.y

    def predictMove(self):
        pass



    def agentUpdate(self):
        pass



    def learn(self):
        pass
