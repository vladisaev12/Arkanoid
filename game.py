import pygame
import time
import datetime

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

AXIS_X = 0
AXIS_Y = 1


class Field:
    def __init__(self):
        self.background = BLACK
        self.width = 1000
        self.height = 700
    
    def rect(self):
        return (self.width, self.height)
    
    def midX(self):
        return self.width / 2


class Platform:
    def __init__(self, field):
        self.color = BLUE
        self.width = 150
        self.height = 10
        self.x = field.midX() - self.halfWidth()
        self.y = field.height - 200
        self.v = .5

    def halfWidth(self):
        return self.width / 2
    
    def midX(self):
        return self.x + self.halfWidth()
    
    def moveRight(self, tick):
        self.x += self.v * tick
    
    def moveLeft(self, tick):
        self.x -= self.v * tick


class Ball:
    def __init__(self, platform):
        self.color = GREEN
        self.radius = 2.5 * 10
        self.pos = [platform.midX(), platform.y - self.radius]
        self.v = [-.25, -.25]
    
    def vec(self, tick):
        return (self.vx * tick, self.vy * tick)
   
    def moveAxis(self, axis, l, edge, direction):
        l1 = direction * (edge - self.pos[axis])
        if l > l1:# - self.radius:
            l2 = l - l1
            self.pos[axis] = direction * (edge - l2)
            self.v[axis] = -self.v[axis]
        else:
            self.pos[axis] += direction * l

    def move(self, tick):
        # X coordinate collisions
        lx = abs(self.v[AXIS_X]) * tick
        if self.v[AXIS_X] < 0:
            self.moveAxis(AXIS_X, lx, 0, -1)
        elif self.v[AXIS_X] > 0:
            self.moveAxis(AXIS_X, lx, field.width, 1)

        # Y coordinate collisions
        ly = abs(self.v[AXIS_Y]) * tick
        if self.v[AXIS_Y] < 0:
            self.moveAxis(AXIS_Y, ly, 0, -1)
        elif self.v[AXIS_Y] > 0:
            if self.pos[AXIS_X] > platform.x and self.pos[AXIS_X] < platform.x + platform.width:
                print("Platform!!!")
                self.moveAxis(AXIS_Y, ly, platform.y, 1)
            else:
                self.moveAxis(AXIS_Y, ly, field.height, 1)


field = Field()
platform = Platform(field)
ball = Ball(platform)

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(field.rect())
pygame.display.set_caption("Ping-Pong Game")

running = True

while running:
    tickMs = clock.tick(15)

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            running = False

    print(f"{datetime.datetime.now()}")

    if keys[pygame.K_a]:
        platform.moveLeft(tickMs)
    if keys[pygame.K_d]:
        platform.moveRight(tickMs)
    
    ball.move(tickMs)
    
    screen.fill(BLACK)
    pygame.draw.rect(screen, platform.color, ((platform.x, platform.y), (platform.width, platform.height)))
    pygame.draw.circle(screen, ball.color, ball.pos, ball.radius)
    pygame.display.flip()

