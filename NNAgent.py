import math, copy
import random
import numpy as np
import pandas as pd
from sklearn.neural_network import MLPClassifier
from assets import *

class Agent:
    def __init__(self, game):
        self.game = game
        self.neuralNetwork = MLPClassifier(solver='lbfgs', alpha=1e-4,hidden_layer_sizes=(20, 20, 20), random_state=1)
        self.dataFrame = 0
        self.gameNumber = game.gameNumber
        self.features = [ 'index', 'length', 'isSnackOnTheLeft', 'isSnackOnTheRight', 'isSnackHigher', 'isSnackLower',
         'distanceToSnack', 'isLeftClear', 'isRightClear', 'isUpClear', 'isDownClear','distanceToDeath', 'stepEvaluation', 'step' ]
        self.initDataset()
        from sklearn.preprocessing import MinMaxScaler
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.learn()


    def initDataset(self):
        data = np.array([self.features])
        self.dataFrame=pd.DataFrame(data=data[1:,1:], index=data[1:,0], columns=data[0,1:])

    def saveDataset(self):
        self.dataFrame.to_csv('data.csv')

    def getDistanceToSnack(self):
        deltaX = self.game.snake.body[0].position.x - self.game.snack.position.x
        deltaY = self.game.snake.body[0].position.y - self.game.snack.position.y
        return math.sqrt(math.pow(deltaX,2) + math.pow(deltaY,2))
    def isSquareClear(self, direction):
        # v = Velocity(self.game.snake.velocity.dir)
        # if(direction == "Right"): v = v.turnRight()
        # if(direction == "Left"): v = v.turnLeft()
        v = Velocity(direction)
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
    def distanceToDeath(self):
        i = 1
        square = Point(self.game.snake.body[0].position.x, self.game.snake.body[0].position.y)
        while 1:
            square.x = square.x + self.game.map.squareSideLength * self.game.snake.velocity.vX
            square.y = square.y + self.game.map.squareSideLength * self.game.snake.velocity.vY

            for snakeSquare in self.game.snake.body[1:]:
                if snakeSquare.position.x == square.x and snakeSquare.position.y == square.y:
                    return i
            if square.x == 0 or square.x == self.game.map.width-self.game.map.squareSideLength:
                return i
            if square.y == 0 or square.y == self.game.map.height-self.game.map.squareSideLength:
                return i
            i+=1

    def predictMove(self):
        newRow = [ self.game.score, self.isSnackOnTheLeft(), self.isSnackOnTheRight(), self.isSnackHigher(), self.isSnackLower(), self.getDistanceToSnack(),
        self.isSquareClear("Left"), self.isSquareClear("Right"), self.isSquareClear("Up"), self.isSquareClear("Down"), self.distanceToDeath()]
        df = self.dataFrame.iloc[[0]]
        df = df[self.features[1:-2]]
        df.loc[1] = newRow
        df[df.columns] = self.scaler.transform(df[df.columns])
        move = self.neuralNetwork.predict(df)
        self.game.snake.velocity = Velocity(move[0])

    def previousStepEvaluation(self):
        if (len(self.dataFrame.index)==0): return
        previousRow = self.dataFrame.iloc[len(self.dataFrame.index)-1]
        previousStepEvaluation = max((previousRow.distanceToSnack - self.getDistanceToSnack()), 5 )*(1 + self.gameNumber - self.game.gameNumber)

        self.dataFrame.at[len(self.dataFrame.index), "stepEvaluation"] = previousStepEvaluation

    def updateDatasetByHuman(self):
        if(len(self.dataFrame.index)>0):
            self.dataFrame.at[len(self.dataFrame.index), "step"] = self.game.snake.velocity.dir;

    def update(self):
        #self.updateDatasetByHuman()
        self.previousStepEvaluation()
        if(self.game.gameNumber > self.gameNumber): #game was lost
            self.saveDataset()
            self.gameNumber += 1

        newRow = [ self.game.score+1, self.isSnackOnTheLeft(), self.isSnackOnTheRight(), self.isSnackHigher(), self.isSnackLower(), self.getDistanceToSnack(),
        self.isSquareClear("Left"), self.isSquareClear("Right"), self.isSquareClear("Up"), self.isSquareClear("Down"), self.distanceToDeath(), 0, "empty"]
        self.dataFrame.loc[len(self.dataFrame.index)+1] = newRow

        self.predictMove()

    def learn(self):
        dataTrain = pd.read_csv('trainingData.csv', index_col=0)
        dataCorrect = dataTrain[dataTrain['stepEvaluation'] >= 5 ]


        xTrain = dataCorrect[self.features[1:-2]]
        yTrain = dataCorrect["step"]

        xTrain[xTrain.columns] = self.scaler.fit_transform(xTrain[xTrain.columns])
        self.neuralNetwork.fit(xTrain, yTrain)
        print('Accuracy of the classifier on TRAINING set: {:.2f}'.format(self.neuralNetwork.score(xTrain, yTrain)))
