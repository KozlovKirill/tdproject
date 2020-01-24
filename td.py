import pygame, os, time
from random import randint

pygame.init()

HP = 100

MYEVENTTYPE = 31

MYEVENTTYPE_2 = 31

FPS = 10
WIDTH = 960
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


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


Cursor = load_image('arrow.png', -1)


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


class Enemy(AnimatedSprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(sheet, columns, rows, x, y)
        self.dx = 0
        self.dy = 0
        self.mode = 'walk'
        self.c = randint(0, 1)
        self.hp = 100

    def update(self):
        if self.mode == 'walk':
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        if self.rect.x == 280 and self.rect.y == 470:
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
            self.rect.x += self.dx
            self.rect.y += self.dy


class Enemy_2(AnimatedSprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(sheet, columns, rows, x, y)
        self.dx = 0
        self.dy = 0
        self.mode = 'walk'
        self.c = randint(0, 1)
        self.hp = 100

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
            self.rect.x += self.dx
            self.rect.y += self.dy


pygame.time.set_timer(MYEVENTTYPE, 1000)  # таймер на 1 секунду

pygame.time.set_timer(MYEVENTTYPE_2, 2000)

all_sprites = pygame.sprite.Group()
field = pygame.sprite.Sprite(all_sprites)
field.image = load_image("game.jpg")
field.image = pygame.transform.scale(field.image, (WIDTH, HEIGHT))
field.rect = field.image.get_rect()

running = True


def wave():
    if randint(0, 1) == 0:
        dragon = Enemy(load_image("orkwalk.png", color_key=-1), 7, 1, 280, 470)
    else:
        dragon = Enemy_2(load_image("orkwalk.png", color_key=-1), 7, 1, 200, -50)
    return dragon


gold = 1000


def draw(gold):  # рисуем золото
    font = pygame.font.Font(None, 35)
    text = font.render(str(gold), 1, (204, 204, 0))
    text_x = 810
    text_y = 22
    screen.blit(text, (text_x, text_y))

    if 315 < pygame.mouse.get_pos()[0] < 370 and 515 < pygame.mouse.get_pos()[1] < 590:
        text = font.render(str(1000), 1, (204, 204, 0))
        text_x = 315
        text_y = 540
        screen.blit(text, (text_x, text_y))

    if 388 < pygame.mouse.get_pos()[0] < 442 and 515 < pygame.mouse.get_pos()[1] < 590:
        text = font.render(str(1000), 1, (204, 204, 0))
        text_x = 388
        text_y = 540
        screen.blit(text, (text_x, text_y))

    if 465 < pygame.mouse.get_pos()[0] < 520 and 515 < pygame.mouse.get_pos()[1] < 590:
        text = font.render(str(1000), 1, (204, 204, 0))
        text_x = 465
        text_y = 540
        screen.blit(text, (text_x, text_y))

    if 535 < pygame.mouse.get_pos()[0] < 591 and 515 < pygame.mouse.get_pos()[1] < 590:
        text = font.render(str(1000), 1, (204, 204, 0))
        text_x = 535
        text_y = 540
        screen.blit(text, (text_x, text_y))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass
        if event.type == MYEVENTTYPE:  # каждую секундку прибавлется по 25 золота
            gold += 25
            # print(pygame.mouse.get_pos()[0])
            # print(pygame.mouse.get_pos()[1])
        if event.type == MYEVENTTYPE_2:
            # каждую 5 секундку прибавлется по 1 юниту
            wave()

    screen.fill(pygame.Color("black"))
    all_sprites.draw(screen)
    all_sprites.update()

    draw(gold)

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()


class Castle:
    # КООРДИНАТЫ НАЧАЛА ЗЕЛЕННОЙ ПОЛОСКИ (ЛЕВЫЙ ВЕРХНИЙ УГОЛ) (740, 495)
    # КООРДИНАТЫ ПРАВОГО НИЖНЕГО УГЛА(840, 510)
    pass

# разворот изображения pygame.transform.flip(pig.image, True, False)
