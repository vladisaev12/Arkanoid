import datetime
import random
import pygame
import time


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

AXIS_X = 0
AXIS_Y = 1

MAX_LIVES = 5


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Sans', 32)
        self.field = Field(screen.get_size())
        self.platform = Platform(self.field)
        self.ball = Ball(self.platform)
        self.lives = MAX_LIVES
        self.gameOver = False

    def exit(self):
        self.gameOver = True

    def drawLives(self):
        data = '♥' * self.lives
        data = data.ljust(MAX_LIVES, '×')
        print(data)
        text = self.font.render(data, True, RED)
        self.screen.blit(text, text.get_rect())

    def draw(self):
        self.field.draw(self.screen)
        self.platform.draw(self.screen)
        self.ball.draw(self.screen)
        self.drawLives()
        pygame.display.flip()

    def move(self, tickMs, keys):
        if keys[pygame.K_SPACE]:
            self.ball.throw()
        if keys[pygame.K_a]:
            self.platform.moveLeft(tickMs)
        if keys[pygame.K_d]:
            self.platform.moveRight(tickMs)
        if keys[pygame.K_f]:
            pygame.display.toggle_fullscreen()

        if not self.ball.move(tickMs):
            if self.lives > 0:
                self.lives -= 1
                self.ball = Ball(self.platform)
            else:
                self.gameOver = True


class Field:
    def __init__(self, size):
        self.background = BLACK
        (self.width, self.height) = size
    
    def draw(self, screen):
        screen.fill(BLACK)

    def midX(self):
        return self.width / 2


class Platform:
    def __init__(self, field):
        self.fillColor = BLUE
        self.borderColor = RED
        self.borderWidth = 1
        self.width = 150
        self.height = 10
        self.x = field.midX() - self.halfWidth()
        self.y = field.height - 100
        self.v = .5
        self.field = field

    def draw(self, screen):
        pygame.draw.rect(screen, self.borderColor,
                         ((self.x, self.y),
                          (self.width, self.height)))
        pygame.draw.rect(screen, self.fillColor,
                         ((self.x + self.borderWidth, self.y + self.borderWidth),
                          (self.width - self.borderWidth * 2, self.height - self.borderWidth * 2)))

    def halfWidth(self):
        return self.width / 2
    
    def midX(self):
        return self.x + self.halfWidth()
    
    def moveDirection(self, tick, edge, platformOffset, direction):
        l1 = self.v * tick
        platformEdge = self.x + platformOffset
        l2 = edge - direction * platformEdge
        print(f'px={self.x}')
        if l1 > l2:
            self.x = edge - direction * platformOffset
        else:
            self.x += direction * l1

    def moveLeft(self, tick):
        self.moveDirection(tick, 0, 0, -1)

    def moveRight(self, tick):
        self.moveDirection(tick, self.field.width, self.width, 1)


class Ball:
    def __init__(self, platform):
        self.color = GREEN
        self.radius = 2.5 * 10
        self.pos = [platform.midX(), platform.y - self.radius]
        self.v = [0, 0]
        self.thrown = False
        self.platform = platform

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, self.radius)

    def throw(self):
        if self.thrown:
            return

        self.v = [-.25 if random.getrandbits(1) else .25, -.25]
        self.thrown = True

    def vec(self, tick):
        return (self.vx * tick, self.vy * tick)
   
    def moveAxis(self, axis, l, edge, direction, fatal=False):

        l1 = edge - self.radius - direction * self.pos[axis]
        if l > l1:
            if fatal:
                return False

            l2 = l - l1
            self.pos[axis] = direction * (edge - self.radius - l2)
            self.v[axis] = -self.v[axis]
        else:
            self.pos[axis] += direction * l

        return True

    def move(self, tick):
        if not self.thrown:
            self.pos[AXIS_X] = self.platform.midX()

        result = True

        # X coordinate collisions
        lx = abs(self.v[AXIS_X]) * tick
        if self.v[AXIS_X] < 0:
            result &= self.moveAxis(AXIS_X, lx, 0, -1)
        elif self.v[AXIS_X] > 0:
            result &= self.moveAxis(AXIS_X, lx, self.platform.field.width, 1)

        # Y coordinate collisions
        ly = abs(self.v[AXIS_Y]) * tick
        if self.v[AXIS_Y] < 0:
            result &= self.moveAxis(AXIS_Y, ly, 0, -1)
        elif self.v[AXIS_Y] > 0:
            if self.pos[AXIS_X] > self.platform.x and self.pos[AXIS_X] < self.platform.x + self.platform.width and self.pos[AXIS_Y] < self.platform.y:# + self.radius < self.platform.y:
                result &= self.moveAxis(AXIS_Y, ly, self.platform.y, 1)
            else:
                result &= self.moveAxis(AXIS_Y, ly, self.platform.field.height, 1, True)

        return result


pygame.init()
(w, h) = pygame.display.get_desktop_sizes()[0]
screen = pygame.display.set_mode((w / 2, h / 2), flags=pygame.RESIZABLE|pygame.SCALED, vsync=1)
pygame.display.set_caption("Ping-Pong Game")

clock = pygame.time.Clock()
running = True
while running:
    game = Game(screen)
    while not game.gameOver:
        tickMs = clock.tick(60)

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                game.exit()
                running = False

        print(f"{datetime.datetime.now()}")

        game.move(tickMs, keys)
        game.draw()
