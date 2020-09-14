import pygame
import time

FPS = 60
WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong')


class player():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 10
        self.rect = None
        self.score = 0

    def draw(self, WIN):
        self.rect = pygame.draw.rect(
            WIN, WHITE, (self.x, self.y, self.width, self.height))


class ball():
    def __init__(self, x, y, color, radius):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.x_vel = 5
        self.y_vel = 5
        self.circle = None

    def draw(self, win):
        self.circle = pygame.draw.circle(
            WIN, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

        if (self.y > HEIGHT or self.y < 0):
            self.changeYDirection()

        if (self.x <= 0 or self.x > WIDTH):
            self.reset()

    def changeYDirection(self):
        self.y_vel *= -1

    def changeXDirection(self):
        self.x_vel *= -1

    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2

    def hit(self, players):
        if self.circle.collidelist(players) != -1:
            self.changeXDirection()


def redrawGame():
    WIN.fill(BLACK)
    p1.draw(WIN)
    p2.draw(WIN)
    ball.draw(WIN)
    pygame.display.update()


def checkTop(player):
    return player.y >= 0


def checkBottom(player):
    return player.y <= HEIGHT - player.height


run = True
clock = pygame.time.Clock()

p1 = player(25, 10, 20, 150)
p2 = player(WIDTH - 45, HEIGHT - 160, 20, 150)
ball = ball(WIDTH // 2, HEIGHT // 2, WHITE, 10)

while run:
    clock.tick(FPS)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if keys[pygame.K_w] and checkTop(p1):
        p1.y -= p1.vel
    if keys[pygame.K_s] and checkBottom(p1):
        p1.y += p1.vel

    if keys[pygame.K_UP] and checkTop(p2):
        p2.y -= p1.vel
    if keys[pygame.K_DOWN] and checkBottom(p2):
        p2.y += p2.vel

    ball.move()
    redrawGame()
    list = [p1.rect, p2.rect]
    ball.hit(list)

pygame.quit()
