import pygame
import random
from FeedFowardNeuralNetwork import *

pygame.init()

SIZE = WIDTH, HEIGHT = (1600, 800)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
running = True
FPS = 120


RECTS_SIZE = RECTSWIDTH, RECTSHEIGHT = (10, 100)
PADDLE_VELOCITY = 5
COLORS = WHITE, BLACK = [ (255, 255, 255), (0, 0, 0) ]
BALLRADIUS = 10
SPACE = 50

#MIDLINESIZE = MIDLINEWIDTH, MIDLINEHEIGHT = (5, 20)


def randomSign() -> int: 
    return 1 if random.random() < 0.5 else -1

def drawText(text, pos, color=WHITE, size=74):

    #print(text, pos, color, size
    font = pygame.font.Font(None, size)

    text = font.render(text, True, color)
    rect = text.get_rect()
    rect.center = pos
    screen.blit(text, rect)


class Paddle:

    def __init__(self, pos, size, color):
        self._pos = pos
        self._size = size
        self._color = color
        self._velocity = PADDLE_VELOCITY

    def get_pos(self):
        return self._pos
    
    def draw(self):
        pygame.draw.rect(screen, self._color, [self._pos[0], self._pos[1], self._size[0], self._size[1]])

    def move(self, dy):

        self._pos[1] += dy * self._velocity

        if self._pos[1] < 0: self._pos[1] = 0
        if self._pos[1] > HEIGHT - RECTSHEIGHT: self._pos[1] = HEIGHT - RECTSHEIGHT


class Ball:

    VELOCITIES = [2, 2.25, 2.5, 2.75, 3, 3.25, 3.50, 3.75, 4, 4.25, 5.50, 4.75, 5, 5.25, 5.50, 5.75, 6]

    def __init__(self, pos, radius, color):
        self._pos = pos
        self._radius = radius
        self._color = color
        self._velocity = [randomSign() * 5, randomSign() * self.VELOCITIES[int(random.random() * len(self.VELOCITIES))]]

 
    def get_pos(self):
        return self._pos

    def draw(self):
        pygame.draw.circle(screen, self._color, self._pos, self._radius)

    def move(self):

        self._pos[0] += self._velocity[0]
        self._pos[1] += self._velocity[1]


        if self._pos[1] - self._radius <= 0 or self._pos[1] + self._radius >= HEIGHT: self._velocity[1] = - self._velocity[1]; self._pos[1] += self._velocity[1]
    

    # Control the ball with the arrows
    def auxMove(self, dx, dy):

        self._pos[0] += dx * 5
        self._pos[1] += dy * 5
    
    def distance(self, paddle: Paddle):
        auxPointX = self._pos[0]
        auxPointY = self._pos[1]

        rectX, rectY = paddle.get_pos()

        if self._pos[0] < rectX: auxPointX = rectX

        elif self._pos[0] > rectX + RECTSWIDTH: auxPointX = rectX + RECTSWIDTH

        if self._pos[1] < rectY: auxPointY = rectY

        elif self._pos[1] > rectY + RECTSHEIGHT: auxPointY = rectY + RECTSHEIGHT

        distanceX = self._pos[0] - auxPointX
        distanceY = self._pos[1] - auxPointY
        distance = (distanceX * distanceX + distanceY * distanceY) ** (1/2)

        return distance - self._radius
        

    def collusion(self, paddle):

        distance = self.distance(paddle)
        rectX = paddle.get_pos()[0]

        if distance <= 0: 
            self._velocity[0] = -1 * self._velocity[0]
            self._velocity[1] = randomSign() * self.VELOCITIES[int(random.random() * len(self.VELOCITIES))]

            if self._pos[0] - self._radius <= rectX: self._pos[0] = rectX - 2 * self._radius
            else: self._pos[0] = rectX + RECTSWIDTH + 2 * self._radius

            return True

        else: return False
    
    def reset(self):
        self._pos = [WIDTH / 2, HEIGHT / 2]
        self._velocity = [randomSign() * 5, randomSign() * self.VELOCITIES[int(random.random() * len(self.VELOCITIES))]]

class Game:

    def __init__(self, nn1: NeuralNetwork = None, nn2: NeuralNetwork = None, frames=FPS):
        self.p1 = Paddle([SPACE, HEIGHT / 2 - RECTSHEIGHT / 2], RECTS_SIZE, WHITE)
        self.p2 = Paddle([WIDTH - RECTSWIDTH - SPACE, HEIGHT / 2 - RECTSHEIGHT / 2], RECTS_SIZE, WHITE)
        self.ball = Ball([WIDTH / 2, HEIGHT / 2], BALLRADIUS, WHITE)

        self.nn1 = nn1
        self.nn2 = nn2

        self.points = [0, 0]
        self.hits = [0, 0]
        self.score = [self.points, self.hits]
        self.running = True
        self.frames = frames
        self.clock = pygame.time.Clock()

    def draw(self):

        screen.fill(BLACK)

        # Drawing the scores
        drawText(str(self.points[0]), (WIDTH // 4, 75))
        drawText(str(self.points[1]), (WIDTH * 3 // 4, 75))

        numRects = 45

        for i in range(numRects):
            if i % 2 == 0:
                pygame.draw.rect(screen, "white", [WIDTH // 2, i * HEIGHT // numRects, 5, HEIGHT // numRects])

        self.p1.draw()
        self.p2.draw()
        self.ball.draw()
        pygame.display.flip()


    def move(self):
        self.ball.move()

        # Play against a bot
        # rectY = self.p2.get_pos()[1] + RECTSHEIGHT / 2
        # if rectY < self.ball.get_pos()[1]: self.p2.move(1)
        # if rectY > self.ball.get_pos()[1]: self.p2.move(-1)

        # Play against a Neural Network
        # self.nextMove(self.p2, self.nn2)

        # Let 2 Neural Networks play against each other
        # self.nextMove(self.p1, self.nn1)
        # self.nextMove(self.p2, self.nn2)

        # Let a bot play against a Neural Network
        rectY = self.p1.get_pos()[1] + RECTSHEIGHT / 2
        if rectY < self.ball.get_pos()[1]: self.p1.move(1)
        if rectY > self.ball.get_pos()[1]: self.p1.move(-1)
        self.nextMove(self.p2, self.nn2)


    def nextMove(self, paddle: Paddle, nn: NeuralNetwork):

        ball_pos = self.ball.get_pos()
        output = nn.output([paddle.get_pos()[1], ball_pos[1], self.ball.distance(paddle)])

        if len(output) == 1:
            # Tanh activation / output function
            # move = -1 if output[0] < - 0.1 else 0 if output[0] < 0.1 else 1 # For 3 outputs
            move = -1 if output[0] < 0 else 1
            

            # Simoid activation / output funciton
            # move = -1 if output[0] < -0.33 else 0 if output[0] < 0.33 else 1
            paddle.move(move)
        
        # For 2 outputs
        elif len(output) == 2:
            if output[0] > output[1]:  paddle.move(-1)
            else: paddle.move(1)
            
        # For 3 outputs
        elif len(output) == 3:
            maximum, index = output[0], 0
            for i in range(len(output)):
                if output[i] > maximum: index = i; maximum = output[i]

            paddle.move(index - 1)


    def collusion(self):
        if self.ball.collusion(self.p1): self.hits[0] += 1
        elif self.ball.collusion(self.p2): self.hits[1] += 1

        if self.ball._pos[0] - self.ball._radius <= 0: self.ball.reset(); self.points[1] += 1 #; print("Score:", self.score, "Points:", self.points)
        elif self.ball._pos[0] + self.ball._radius >= WIDTH: self.ball.reset(); self.points[0] += 1 #; print("Score:", self.score, "Points:", self.points)

    def endGame(self):
    
        if self.points[0] >= 10 or self.points[1] >= 10: self.running = False; return True
        if self.points[0] >= 3 and self.hits[1] == 0 or self.hits[1] == 1 and self.points[0] >= 5: self.running = False; return True

    def runGame(self):

        while(self.running == True):

            for event in pygame.event.get():

                if event.type == pygame.QUIT: self.running = False; pygame.quit()

            self.move()
            self.collusion()
            self.draw()

            self.endGame()
            self.clock.tick(self.frames)

        self.score = [self.points, self.hits]
        return self.score
        
    

   
# g = Game(nn2=NeuralNetwork(3, 10, 1, activation_func=tanh, output_func=tanh))

g = Game(nn2 = NeuralNetwork.getNNFromFile(3, 10, 1))


if __name__ == "__main__":
    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT: running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: g.p1.move(-1)
        if keys[pygame.K_s]: g.p1.move(1)
        #if keys[pygame.K_UP]: p1.move(-1)
        #if keys[pygame.K_DOWN]: p1.move(1)

        # Control the ball
        if keys[pygame.K_UP]: g.ball.auxMove(0, -1)
        if keys[pygame.K_DOWN]: g.ball.auxMove(0, 1)
        if keys[pygame.K_LEFT]: g.ball.auxMove(-1, 0)
        if keys[pygame.K_RIGHT]: g.ball.auxMove(1, 0)

        g.move()
        g.collusion()
        g.draw()

        if (g.endGame() == True): running = False
        
        clock.tick(FPS)


