import math, copy
import random
import numpy as np
import pandas as pd
from sklearn.neural_network import MLPClassifier
from assets import *
from sklearn.preprocessing import MinMaxScaler
import time

class Agent:
    def __init__(self, game):
        self.game = game
        self.neuralNetwork = MLPClassifier(solver='adam', alpha=1e-3,hidden_layer_sizes=(30, 30, 30), random_state=1)
        self.dataFrame = 0
        self.startingTime = time.time()
        self.generation = 1
        self.gameNumber = game.gameNumber
        self.features = [ 'index', 'length', 'isSnackOnTheLeft', 'isSnackOnTheRight', 'isSnackHigher', 'isSnackLower',
         'distanceToSnack', 'isLeftClear', 'isRightClear', 'isUpClear', 'isDownClear','distanceToDeath',
          'turnsTotal', 'lastTurn',  'stepEvaluation', 'step' ]
        self.initDataset()
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
    def distanceToTail(self):
        if(len(self.game.snake.body) == 0):
            return 0
        return self.game.snake.body[0].position.distance(self.game.snake.body[-1].position)
    def turnsTotal(self):
        i = 0
        dir = self.game.snake.body[0].velocity.dir
        for snakeSquare in self.game.snake.body[1:]:
            if (dir != snakeSquare.velocity.dir):
                dir = snakeSquare.velocity.dir
                i+=1
        return i
    def lastTurn(self):
        i = 0
        dir = self.game.snake.body[0].velocity.dir
        for snakeSquare in self.game.snake.body[1:]:
            if (dir == snakeSquare.velocity.dir):
                i+=1
        return i

    def predictMove(self):
        newRow = [ self.game.score, self.isSnackOnTheLeft(), self.isSnackOnTheRight(), self.isSnackHigher(), self.isSnackLower(),
        self.isSquareClear("Left"), self.isSquareClear("Right"), self.isSquareClear("Up"), self.isSquareClear("Down"), self.distanceToDeath(),
        self.turnsTotal(), self.lastTurn()]
        df = self.dataFrame.iloc[[0]]
        df = df[self.features[1:-2]]
        df.drop("distanceToSnack", inplace=True, axis=1)
        df.loc[1] = newRow
        df[df.columns] = self.scaler.transform(df[df.columns])
        move = self.neuralNetwork.predict(df)
        prob = self.neuralNetwork.predict_proba(df)
        possibilities = ["Right", "Left", "Up", "Down"]
        probThreshold = min(0.90, 0.65 + float(self.generation)/200.0);
        if prob[0][0]<probThreshold and prob[0][1]<probThreshold and prob[0][len(prob[0])-1]<probThreshold and prob[0][len(prob[0])-2]<probThreshold :
            move = (possibilities[random.randint(0, 3)])
            self.game.snake.velocity = Velocity(move)
            self.dataFrame.at[len(self.dataFrame.index), "step"] = move;
        else:
            self.game.snake.velocity = Velocity(move[0])
            self.dataFrame.at[len(self.dataFrame.index), "step"] = move[0];


    def previousStepEvaluation(self):
        if (len(self.dataFrame.index)==0): return
        previousRow = self.dataFrame.iloc[len(self.dataFrame.index)-1]
        previousStepEvaluation = max((previousRow.distanceToSnack - self.getDistanceToSnack()), 5 )*(1 + self.gameNumber - self.game.gameNumber)

        self.dataFrame.at[len(self.dataFrame.index), "stepEvaluation"] = previousStepEvaluation

    def learn(self):

        if (self.generation == 1):
            dataTrain = pd.read_csv('startingData.csv', index_col=0)
            self.dataFrame = dataTrain;
        # else :
        #     dataTrain = pd.read_csv('data.csv', index_col=0)

        if self.generation % 4 == 0:
            self.dataFrame = self.dataFrame.iloc[math.floor(len(self.dataFrame.index)/10):]
            self.dataFrame.index = range(1,len(self.dataFrame)+1)
        print("GENERATION: ", self.generation)
        dataCorrect = self.dataFrame[self.dataFrame['stepEvaluation'] >= 7 ]
        dataCorrect.drop("distanceToSnack", inplace=True, axis=1)
        learningFeatures = copy.deepcopy(self.features[1:-2])
        learningFeatures.remove("distanceToSnack")
        xTrain = dataCorrect[learningFeatures]
        yTrain = dataCorrect["step"]
        xTrain[xTrain.columns] = self.scaler.fit_transform(xTrain[xTrain.columns])
        self.neuralNetwork.fit(xTrain, yTrain)
        print('Accuracy of the classifier on TRAINING set: {:.2f}'.format(self.neuralNetwork.score(xTrain, yTrain)))

    def update(self):
        self.previousStepEvaluation()
        if(self.game.gameNumber > self.gameNumber): #game was lost
            self.gameNumber += 1
        newRow = [ self.game.score+1, self.isSnackOnTheLeft(), self.isSnackOnTheRight(), self.isSnackHigher(), self.isSnackLower(), self.getDistanceToSnack(),
        self.isSquareClear("Left"), self.isSquareClear("Right"), self.isSquareClear("Up"), self.isSquareClear("Down"), self.distanceToDeath(),
        self.turnsTotal(), self.lastTurn(),  0, "empty"]
        self.dataFrame.loc[len(self.dataFrame.index)+1] = newRow
        self.predictMove()

        if(time.time() - self.startingTime > 3 + self.generation*0.2):
            self.game.lose()
            self.gameNumber = self.game.gameNumber
            self.generation+=1
            self.saveDataset()
            self.learn()
            self.startingTime = time.time()
