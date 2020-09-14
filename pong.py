import pygame

FPS = 60
WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TITLE_FONT_SIZE = 60
TITLE_FONT_TEXT = 'Pong!'
SUBTITLE_FONT_SIZE = 30
SUBTITLE_FONT_TEXT = 'Made by alevidals'
FONT_TEXT = 20
WIN_SCORE = 5

pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong')

separator_img = pygame.image.load('separator.png')

winner = None

title_font = pygame.font.Font('font.ttf', TITLE_FONT_SIZE)
subtitle_font = pygame.font.Font('font.ttf', SUBTITLE_FONT_SIZE)
font = pygame.font.Font('font.ttf', FONT_TEXT)

title = title_font.render(TITLE_FONT_TEXT, True, BLACK, WHITE)
title_rect = title.get_rect()
title_rect.center = (WIDTH // 2, HEIGHT // 2 - HEIGHT // 4)

subtitle = subtitle_font.render(SUBTITLE_FONT_TEXT, True, BLACK, WHITE)
subtitle_rect = subtitle.get_rect()
subtitle_rect.center = (WIDTH // 2, HEIGHT // 2 + 50)

tip = font.render('Press space to start play', True, BLACK, WHITE)
tip_rect = tip.get_rect()
tip_rect.center = (WIDTH // 2, HEIGHT - 50)

class player():
    def __init__(self, name, x, y, width, height):
        self.name = name
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

    def do_score(self):
        self.score += 1

    def drawScore(self, WIN):
        score = title_font.render('0', True, WHITE)
        score_rect = score.get_rect()
        score_rect.center = (WIDTH // 2 + WIDTH // 4, 50)

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

    def move(self, p1, p2):
        self.x += self.x_vel
        self.y += self.y_vel

        if (self.y > HEIGHT or self.y < 0):
            self.changeYDirection()

        if (self.x <= 0 or self.x > WIDTH):
            if (self.x <= 0):
                p2.do_score()
            elif (self.x > WIDTH):
                p1.do_score()

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
    p1_score = title_font.render(str(p1.score), True, WHITE)
    p2_score = title_font.render(str(p2.score), True, WHITE)
    WIN.blit(p1_score, (WIDTH // 2 + WIDTH // 4, 50))
    WIN.blit(p2_score, (WIDTH // 2 - WIDTH // 4, 50))
    WIN.blit(pygame.transform.scale(separator_img, (1, HEIGHT)), (WIDTH // 2, 0))
    pygame.display.update()


def drawMenuGame():
    WIN.fill(BLACK)
    WIN.blit(title, title_rect)
    WIN.blit(subtitle, subtitle_rect)
    WIN.blit(tip, tip_rect)
    pygame.display.update()

def drawEndGame():
    WIN.fill(BLACK)
    text = title_font.render('{} has win!'.format(winner.name), True, WHITE)
    text_rect = text.get_rect()
    text_rect.center = (WIDTH // 2, HEIGHT // 2)
    WIN.blit(text, text_rect)
    pygame.display.update()


def checkTop(player):
    return player.y >= 0


def checkBottom(player):
    return player.y <= HEIGHT - player.height


run_menu = True
run_game = False
run_end = False
clock = pygame.time.Clock()

p1 = player(input('Name of the player 1: '), 25, 10, 20, 150)
p2 = player(input('Name of the player 2: '), WIDTH - 45, HEIGHT - 160, 20, 150)
ball = ball(WIDTH // 2, HEIGHT // 2, WHITE, 10)

while run_menu:
    clock.tick(FPS)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_menu = False

    if keys[pygame.K_SPACE]:
        run_menu = False
        run_game = True

    drawMenuGame()

while run_game:
    clock.tick(FPS)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_game = False

    if keys[pygame.K_w] and checkTop(p1):
        p1.y -= p1.vel
    if keys[pygame.K_s] and checkBottom(p1):
        p1.y += p1.vel

    if keys[pygame.K_UP] and checkTop(p2):
        p2.y -= p1.vel
    if keys[pygame.K_DOWN] and checkBottom(p2):
        p2.y += p2.vel

    ball.move(p1, p2)
    redrawGame()
    list = [p1.rect, p2.rect]
    ball.hit(list)

    if (p1.score == WIN_SCORE):
        winner = p1
        run_game = False
        run_end = True

    if (p2.score == WIN_SCORE):
        winner = p2
        run_game = False
        run_end = True

while run_end:
    clock.tick(FPS)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_end = False

    drawEndGame()

pygame.quit()
