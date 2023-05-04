import pygame_menu as pymenu
import threading
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

fps = 60



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
        self.y = field.height - 100
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
   
    def moveAxis(self, axis, l, edge, direction, fatal=False):
        l1 = edge - self.radius - direction * self.pos[axis]
        print(f'axis={"Y" if axis else "X"}')
        print(f'l={l}')
        print(f'l1={l1}')
        if l > l1:
            print(f'!!!!!!!!!!!!!!!! Hit !!!!!!!!!!!!!!!')
            if fatal:
                return False

            l2 = l - l1
            print(f'l2={l2}')
            print(f'old={self.pos[axis]}')
            self.pos[axis] = direction * (edge - self.radius - l2)
            print(f'new={self.pos[axis]}')
            self.v[axis] = -self.v[axis]
        else:
            print(f'Direct!')
            print(f'old={self.pos[axis]}')
            self.pos[axis] += direction * l
            print(f'new={self.pos[axis]}')

        return True

    def move(self, tick):
        result = True

        # X coordinate collisions
        lx = abs(self.v[AXIS_X]) * tick
        if self.v[AXIS_X] < 0:
            result &= self.moveAxis(AXIS_X, lx, 0, -1)
        elif self.v[AXIS_X] > 0:
            result &= self.moveAxis(AXIS_X, lx, field.width, 1)

        # Y coordinate collisions
        ly = abs(self.v[AXIS_Y]) * tick
        if self.v[AXIS_Y] < 0:
            result &= self.moveAxis(AXIS_Y, ly, 0, -1)
        elif self.v[AXIS_Y] > 0:
            if self.pos[AXIS_X] > platform.x and self.pos[AXIS_X] < platform.x + platform.width:
                print("Platform!!!")
                result &= self.moveAxis(AXIS_Y, ly, platform.y, 1)
            else:
                result &= self.moveAxis(AXIS_Y, ly, field.height, 1, True)

        return result


field = Field()
platform = Platform(field)
ball = Ball(platform)

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(field.rect())
pygame.display.set_caption("Ping-Pong Game")

running = True

started = False

def set_fps(value, fps):
    clock.tick(fps)

def start_the_game():
    started = True
    menu.disable()

menu = pymenu.Menu('Arkanoid', field.width, field.height, theme=pymenu.themes.THEME_BLUE)

menu.add.selector('fps :', [('30', 1), ('60', 2)], onchange=set_fps)
menu.add.button('Play', start_the_game)

while running:
    tickMs = clock.tick(5)

    keys = pygame.key.get_pressed()
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            running = False
    if menu.is_enabled():
        field = Field()
        platform = Platform(field)
        ball = Ball(platform)
        menu.update(events)
        menu.mainloop(screen)
    if menu.is_enabled() == False:
        print(f"{datetime.datetime.now()}")
        
        if keys[pygame.K_a]:
            platform.moveLeft(tickMs)
        if keys[pygame.K_d]:
            platform.moveRight(tickMs)
        
        if ball.move(tickMs):
            screen.fill(BLACK)
            pygame.draw.rect(screen, platform.color, ((platform.x, platform.y), (platform.width, platform.height)))
            ballrect = pygame.draw.circle(screen, ball.color, ball.pos, ball.radius)
            pygame.display.flip()
        else:
            menu.full_reset()
            menu.enable()

