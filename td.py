import pygame, os, time
from random import randint

pygame.init()

MYEVENTTYPE = 31

MYEVENTTYPE_2 = 31

FPS = 10
WIDTH = 960
HEIGHT = 540
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
waveactive = True


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

class Castle():
    def __init__(self):
        self.hp = 100
        self.damage = 1
        self.crushed = False

    def update(self):
        pygame.draw.rect(screen, pygame.Color('red'), (740, 495, self.hp, 15))
        if self.hp == 0 and self.crushed == False:
            global waveactive
            AnimatedSprite(load_image('fire.png', color_key=-1), 10, 6, 774, 106)
            AnimatedSprite(load_image('fire.png', color_key=-1), 10, 6, 885, 96)
            AnimatedSprite(pygame.transform.scale(load_image('fire.png', color_key=-1), (960, 576)), 10, 6, 815, 90)
            waveactive = False
            self.crushed = True
            for enemy in enemies:
                enemy.mode = 'stop'

class Enemy(AnimatedSprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(sheet, columns, rows, x, y)
        self.dx = 0
        self.dy = 0
        self.mode = 'walk'
        self.c = randint(0, 1)
        self.hp = 100

    def attack(self, target):
        target.hp -= target.damage

    def update(self):
        if self.mode == 'walk':
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            if self.rect.x == 280 and self.rect.y == 500:
                self.dx = 0
                self.dy = -10
            elif self.rect.x == 280 and self.rect.y == 260:
                self.dx = -10
                self.dy = 0
            elif self.rect.x == 120 and self.rect.y == 260:
                self.dx = 0
                self.dy = -10
            elif self.rect.x == 120 and self.rect.y == 100:
                self.dx = 10
                self.dy = 0
            # развилка
            if self.c == 1:
                if self.rect.x == 440 and self.rect.y == 100:
                    self.dx = 0
                    self.dy = 10
                elif self.rect.x == 440 and self.rect.y == 420:
                    self.dx = 10
                    self.dy = 0
                elif self.rect.x == 840 and self.rect.y == 420:
                    self.dx = 0
                    self.dy = -10
                elif self.rect.x == 840 and self.rect.y == 170:
                    self.dx = 0
                    self.dy = 0
                    self.frames = []
                    self.cut_sheet(load_image('orkattack.png', color_key=-1), 7, 1)
                    self.rect.x = 835
                    self.rect.y = 170
                    self.cur_frame = 0
                    self.image = self.frames[self.cur_frame]
                self.rect.x += self.dx
                self.rect.y += self.dy
            else:
                if self.rect.x == 670 and self.rect.y == 100:
                    self.dx = 0
                    self.dy = 10
                elif self.rect.x == 670 and self.rect.y == 250:
                    self.dx = -10
                    self.dy = 0
                elif self.rect.x == 440 and self.rect.y == 250:
                    self.dx = 0
                    self.dy = 10
                elif self.rect.x == 440 and self.rect.y == 420:
                    self.dx = 10
                    self.dy = 0
                elif self.rect.x == 840 and self.rect.y == 420:
                    self.dx = 0
                    self.dy = -10
                elif self.rect.x == 840 and self.rect.y == 170:
                    self.dx = 0
                    self.dy = 0
                    self.frames = []
                    self.cut_sheet(load_image('orkattack.png', color_key=-1), 7, 1)
                    self.rect.x = 835
                    self.rect.y = 170
                    self.cur_frame = 0
                    self.image = self.frames[self.cur_frame]
                    self.mode = 'attack'
                self.rect.x += self.dx
                self.rect.y += self.dy
        elif self.mode == 'attack':
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            if self.cur_frame == 4:
                self.attack(castle)


class Enemy_2(Enemy):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(sheet, columns, rows, x, y)

    def update(self):
        if self.mode == 'walk':
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            if self.rect.x == 200 and self.rect.y == -50:
                self.dx = 0
                self.dy = 10
            elif self.rect.x == 200 and self.rect.y == 100:
                self.dx = 10
                self.dy = 0
            # развилка
            if self.c == 1:
                if self.rect.x == 440 and self.rect.y == 100:
                    self.dx = 0
                    self.dy = 10
                elif self.rect.x == 440 and self.rect.y == 420:
                    self.dx = 10
                    self.dy = 0
                elif self.rect.x == 840 and self.rect.y == 420:
                    self.dx = 0
                    self.dy = -10
                elif self.rect.x == 840 and self.rect.y == 170:
                    self.dx = 0
                    self.dy = 0
                    self.frames = []
                    self.cut_sheet(load_image('orkattack.png', color_key=-1), 7, 1)
                    self.rect.x = 835
                    self.rect.y = 170
                    self.cur_frame = 0
                    self.image = self.frames[self.cur_frame]
                self.rect.x += self.dx
                self.rect.y += self.dy
            else:
                if self.rect.x == 670 and self.rect.y == 100:
                    self.dx = 0
                    self.dy = 10
                elif self.rect.x == 670 and self.rect.y == 250:
                    self.dx = -10
                    self.dy = 0
                elif self.rect.x == 440 and self.rect.y == 250:
                    self.dx = 0
                    self.dy = 10
                elif self.rect.x == 440 and self.rect.y == 420:
                    self.dx = 10
                    self.dy = 0
                elif self.rect.x == 840 and self.rect.y == 420:
                    self.dx = 0
                    self.dy = -10
                elif self.rect.x == 840 and self.rect.y == 170:
                    self.dx = 0
                    self.dy = 0
                    self.frames = []
                    self.cut_sheet(load_image('orkattack.png', color_key=-1), 7, 1)
                    self.rect.x = 835
                    self.rect.y = 170
                    self.cur_frame = 0
                    self.image = self.frames[self.cur_frame]
                    self.mode = 'attack'
                self.rect.x += self.dx
                self.rect.y += self.dy
        elif self.mode == 'attack':
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            if self.cur_frame == 4:
                self.attack(castle)

pygame.time.set_timer(MYEVENTTYPE, 1000)  # таймер на 1 секунду
pygame.time.set_timer(MYEVENTTYPE_2, 2000)

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
field = pygame.sprite.Sprite(all_sprites)
field.image = load_image("game.jpg")
field.image = pygame.transform.scale(field.image, (WIDTH, HEIGHT))
field.rect = field.image.get_rect()

running = True


def wave():
    if waveactive:
        if randint(0, 1) == 0:
            ork = Enemy(load_image("orkwalk.png", color_key=-1), 7, 1, 280, 500)
        else:
            ork = Enemy_2(load_image("orkwalk.png", color_key=-1), 7, 1, 200, -50)
        enemies.add(ork)
        return ork

castle = Castle()
gold = 1000


def draw(gold):  # рисуем золото
    font = pygame.font.Font(None, 35)
    text = font.render(str(gold), 1, (255, 99, 71))
    text_x = 810
    text_y = 22
    screen.blit(text, (text_x, text_y))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
        if event.type == MYEVENTTYPE:  # каждую секундку прибавлется по 25 золота
            gold += 25
        if event.type == MYEVENTTYPE_2:
            # каждую 5 секундку прибавлется по 1 юниту
            wave()

    screen.fill(pygame.Color("black"))
    all_sprites.draw(screen)
    all_sprites.update()
    castle.update()

    draw(gold)

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()