import pygame
import random


pygame.init()

SIZE = WIDTH, HEIGHT = (1600, 800)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
running = True
FPS = 60


RECTS_SIZE = RECTSWIDTH, RECTSHEIGHT = (10, 100)
PADDLE_VELOCITY = 10
COLORS = WHITE, BLACK = [ (255, 255, 255), (0, 0, 0) ]
BALLRADIUS = 10
SPACE = 50

#MIDLINESIZE = MIDLINEWIDTH, MIDLINEHEIGHT = (5, 20)


def randomSign():
    return 1 if random.random() < 0.5 else -1

def drawText(text, pos, color=WHITE, size=74):

    #print(text, pos, color, size)
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

    VELOCITIES = [4.5, 5, 6, 7, 8, 9, 10, 11, 12]

    def __init__(self, pos, radius, color):
        self._pos = pos
        self._radius = radius
        self._color = color
        self._velocity = [randomSign() * 10, randomSign() * self.VELOCITIES[int(random.random() * len(self.VELOCITIES))]]

 
    def get_pos(self):
        return self._pos

    def draw(self):
        pygame.draw.circle(screen, self._color, self._pos, self._radius)

    def move(self):

        self._pos[0] += self._velocity[0]
        self._pos[1] += self._velocity[1]


        if self._pos[1] - self._radius <= 0 or self._pos[1] + self._radius >= HEIGHT: self._velocity[1] = - self._velocity[1]
    
    def auxMove(self, dx, dy):

        self._pos[0] += dx * 5
        self._pos[1] += dy * 5
        

    def collusion(self, paddle, id):
        
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


        if self._radius >= distance: 
            self._velocity[0] = -1 * self._velocity[0]
            self._velocity[1] = randomSign() * self.VELOCITIES[int(random.random() * len(self.VELOCITIES))]
            if id == 1: self._pos[0] = rectX + RECTSWIDTH + self._radius
            else: self._pos[0] = rectX - self._radius

            return True

        else: return False
    
    def reset(self):
        self._pos = [WIDTH / 2, HEIGHT / 2]
        self._velocity = [randomSign() * 10, randomSign() * self.VELOCITIES[int(random.random() * len(self.VELOCITIES))]]

class Game:

    def __init__(self):
        self.p1 = Paddle([SPACE, HEIGHT / 2 - RECTSHEIGHT / 2], RECTS_SIZE, WHITE)
        self.p2 = Paddle([WIDTH - RECTSWIDTH - SPACE, HEIGHT / 2 - RECTSHEIGHT / 2], RECTS_SIZE, WHITE)
        self.ball = Ball([WIDTH / 2, HEIGHT / 2], BALLRADIUS, WHITE)

        self.points = [0, 0]
        self.score = [0, 0]

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

        # Play against a boot
        rectY = self.p2.get_pos()[1] + RECTSHEIGHT / 2
        if rectY < self.ball.get_pos()[1]: self.p2.move(1)
        if rectY > self.ball.get_pos()[1]: self.p2.move(-1)

    def collusion(self):
        if self.ball.get_pos()[0] < WIDTH / 2 and self.ball.collusion(self.p1, 1): self.score[0] += 1
        elif self.ball.collusion(self.p2, 2): self.score[1] += 1

        if self.ball._pos[0] - self.ball._radius <= 0: self.ball.reset(); self.points[1] += 1; print("Score:", self.score, "Points:", self.points)
        elif self.ball._pos[0] + self.ball._radius >= WIDTH: self.ball.reset(); self.points[1] += 1; print("Score:", self.score, "Points:", self.points)
    

   
g = Game()


if __name__ == "__main__":
    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT: running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: g.p1.move(-1)
        if keys[pygame.K_s]: g.p1.move(1)
        #if keys[pygame.K_UP]: p1.move(-1)
        #if keys[pygame.K_DOWN]: p1.move(1)

        if keys[pygame.K_UP]: g.ball.auxMove(0, -1)
        if keys[pygame.K_DOWN]: g.ball.auxMove(0, 1)
        if keys[pygame.K_LEFT]: g.ball.auxMove(-1, 0)
        if keys[pygame.K_RIGHT]: g.ball.auxMove(1, 0)


        g.move()
        g.collusion()
        g.draw()
        
        clock.tick(FPS)


