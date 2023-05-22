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


class Field:
    def __init__(self, width, height):
        self.background = BLACK
        self.width = width
        self.height = height
    
    def rect(self):
        return (self.width, self.height)
    
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

    def draw(self):
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
        self.moveDirection(tick, field.width, self.width, 1)


class Ball:
    def __init__(self, platform):
        self.color = GREEN
        self.radius = 2.5 * 10
        self.pos = [platform.midX(), platform.y - self.radius]
        self.v = [0, 0]
        self.thrown = False
    
    def throw(self):
        if self.thrown:
            return

        self.v = [-.25 if random.getrandbits(1) else .25, -.25]
        self.thrown = True

    def vec(self, tick):
        return (self.vx * tick, self.vy * tick)
   
    def moveAxis(self, axis, l, edge, direction):
        l1 = edge - self.radius - direction * self.pos[axis]
        if l > l1:
            l2 = l - l1
            self.pos[axis] = direction * (edge - self.radius - l2)
            self.v[axis] = -self.v[axis]
        else:
            self.pos[axis] += direction * l

    def move(self, tick):
        if not self.thrown:
            self.pos[AXIS_X] = platform.midX()

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
            if self.pos[AXIS_X] > platform.x and self.pos[AXIS_X] < platform.x + platform.width and self.pos[AXIS_Y] + self.radius < platform.y:
                self.moveAxis(AXIS_Y, ly, platform.y, 1)
            else:
                self.moveAxis(AXIS_Y, ly, field.height, 1)


pygame.init()
(w, h) = pygame.display.get_desktop_sizes()[0]
field = Field(w / 2, h / 2)
screen = pygame.display.set_mode(field.rect(), flags=pygame.RESIZABLE|pygame.SCALED, vsync=1)
pygame.display.set_caption("Ping-Pong Game")

platform = Platform(field)
ball = Ball(platform)

clock = pygame.time.Clock()
running = True
while running:
    tickMs = clock.tick(60)

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            running = False

    print(f"{datetime.datetime.now()}")

    if keys[pygame.K_SPACE]:
        ball.throw()
    if keys[pygame.K_a]:
        platform.moveLeft(tickMs)
    if keys[pygame.K_d]:
        platform.moveRight(tickMs)
    if keys[pygame.K_f]:
        pygame.display.toggle_fullscreen()
    
    ball.move(tickMs)
    
    screen.fill(BLACK)
    platform.draw()
    pygame.draw.circle(screen, ball.color, ball.pos, ball.radius)
    pygame.display.flip()