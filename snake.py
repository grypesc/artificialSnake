import sys, pygame, copy, random
import importlib
from assets import *



class Map():
    def __init__(self, width, height, squareSideLength):
        self.width = width
        self.height = height
        self.squareSideLength = squareSideLength
        #self.squares = [[0 for x in range((int)(width/squareSideLength))] for y in range((int)(height/squareSideLength))]

    def getWidthInSquares(self):
        return (int)(self.width/self.squareSideLength)
    def getHeightInSquares(self):
        return (int)(self.height/self.squareSideLength)

class Snack():
    def __init__(self, startingPoint, map):
        self.position = startingPoint
        self.color = (230, 230, 0)
    def __init__(self, map):
        self.color = (230, 230, 0)
        self.map = map
        self.position = Point(0,0)
        while (self.position.x == 0 or self.position.x == self.map.width - self.map.squareSideLength):
            self.position.x = map.squareSideLength*random.randint(0,map.getWidthInSquares()-1)
        while (self.position.y == 0 or self.position.y == self.map.height - self.map.squareSideLength):
            self.position.y = map.squareSideLength*random.randint(0,map.getHeightInSquares()-1)



class Snake():
    def __init__(self, startingPoint, velocity, map):
        self.velocity = velocity
        self.color = (50,205,50)
        self.headColor = (0,255,0)
        self.map = map
        self.body = []
        self.body.append(BodySquare(startingPoint, velocity))

    def move(self):
        snakeHead = self.body[0]
        snakeHead.velocity.vX = self.velocity.vX;
        snakeHead.velocity.vY = self.velocity.vY;
        previousPosition = copy.deepcopy(snakeHead)
        snakeHead.position.x += self.map.squareSideLength*self.velocity.vX
        snakeHead.position.y += self.map.squareSideLength*self.velocity.vY
        # if snakeHead.position.x >= self.map.width: snakeHead.position.x = 0;
        # if snakeHead.position.x < 0: snakeHead.position.x = self.map.width - self.map.squareSideLength;
        # if snakeHead.position.y >= self.map.height: snakeHead.position.y = 0;
        # if snakeHead.position.y < 0: snakeHead.position.y = self.map.height - self.map.squareSideLength;
        for i in range (1, len(self.body)):
            temp = copy.deepcopy(self.body[i])
            self.body[i] = previousPosition
            previousPosition = temp

class BodySquare():
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

class Game():
    def __init__(self, width, height, squareSideLength):
        self.screen = pygame.display.set_mode((width, height))
        self.map = Map(width, height, squareSideLength)
        self.snake = Snake(Point(350,200), Velocity("Right"), self.map)
        self.snack = Snack( self.map)
        self.score = 0

    def drawGrid(self):
        x = 0
        y = 0
        while x < self.map.width:
            x = x + self.map.squareSideLength
            pygame.draw.line(self.screen, (100,100,100), (x,0),(x,self.map.height))
        while y < self.map.height:
            y = y + self.map.squareSideLength
            pygame.draw.line(self.screen, (100,100,100), (0,y),(self.map.width,y))

    def drawEdges(self):
        pygame.draw.rect(self.screen,(0, 0, 51),(0,0,self.map.width,self.map.squareSideLength))
        pygame.draw.rect(self.screen,(0, 0, 51),(0,self.map.height-self.map.squareSideLength,self.map.width,self.map.squareSideLength))
        pygame.draw.rect(self.screen,(0, 0, 51),(self.map.height-self.map.squareSideLength,0,self.map.squareSideLength,self.map.height))
        pygame.draw.rect(self.screen,(0, 0, 51),(0,0,self.map.squareSideLength,self.map.height))

    def drawSnake(self):
        pygame.draw.rect(self.screen,self.snake.headColor,(self.snake.body[0].position.x,self.snake.body[0].position.y,self.map.squareSideLength,self.map.squareSideLength))
        for snakeSquare in self.snake.body[1:]:
            pygame.draw.rect(self.screen,self.snake.color,(snakeSquare.position.x,snakeSquare.position.y,self.map.squareSideLength,self.map.squareSideLength))

    def drawSnack(self):
        pygame.draw.rect(self.screen,self.snack.color,(self.snack.position.x,self.snack.position.y,self.map.squareSideLength,self.map.squareSideLength))

    def lose(self):
        print("You lost, score: ", self.score)
        self.snake = Snake(Point(350,200), Velocity("Right"), self.map)
        self.snack = Snack(self.map)
        self.score = 0

    def redrawWindow(self):
        self.screen.fill((0,0,0))
        self.drawSnake()
        self.drawSnack()
        self.drawGrid()
        self.drawEdges()
        pygame.display.flip()

    def update(self):
        self.handleEvents()
        self.snake.move()
        self.checkCollisions()


    def checkCollisions(self):
        if (self.snake.body[0].position.x == self.snack.position.x) and (self.snake.body[0].position.y == self.snack.position.y):
            self.snack = Snack(self.map)
            self.score+=1
            lastSnakeBody = self.snake.body[-1]
            newSnakeBodySquare=BodySquare(Point(lastSnakeBody.position.x - self.map.squareSideLength*lastSnakeBody.velocity.vX , lastSnakeBody.position.y- self.map.squareSideLength*lastSnakeBody.velocity.vY), self.snake.body[-1].velocity)
            self.snake.body.append(newSnakeBodySquare)
        headPosition = self.snake.body[0].position
        for snakeSquare in self.snake.body[1:]:
            if snakeSquare.position.x == headPosition.x and snakeSquare.position.y == headPosition.y:
                self.lose()
        if headPosition.x == 0 or headPosition.x == self.map.width-self.map.squareSideLength:
            self.lose()
        if headPosition.y == 0 or headPosition.y == self.map.height-self.map.squareSideLength:
            self.lose()

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_a] and self.snake.velocity.dir != "Right" and self.snake.velocity.dir != "Left":
                    self.snake.velocity = Velocity("Left")
                elif keys[pygame.K_d] and self.snake.velocity.dir != "Left" and self.snake.velocity.dir != "Right":
                    self.snake.velocity = Velocity("Right")
                elif keys[pygame.K_w] and self.snake.velocity.dir != "Down" and self.snake.velocity.dir != "Up":
                    self.snake.velocity = Velocity("Up")
                elif keys[pygame.K_s] and self.snake.velocity.dir != "Up" and self.snake.velocity.dir != "Down" :
                    self.snake.velocity = Velocity("Down")



pygame.init()
game = Game(500, 500, 25)
import NNAgent
agent = NNAgent.Agent(game)
clock = pygame.time.Clock()

while 1:
    agent.agentUpdate()
    game.update()
    game.redrawWindow()
    pygame.time.delay(50)
    clock.tick(10)
