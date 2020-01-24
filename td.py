import pygame, os, time
from random import randint

pygame.init()

MYEVENTTYPE = 31
1
MYEVENTTYPE_2 = 31

FPS = 10
WIDTH = 960
HEIGHT = 600
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
        pygame.draw.rect(screen, pygame.Color('red'), (739, 534, self.hp, 17))
        if self.hp <= 0 and self.crushed == False:
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
            # РЎР‚Р В°Р В·Р Р†Р С‘Р В»Р С”Р В°
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


pygame.time.set_timer(MYEVENTTYPE, 1000)
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
            ork = Enemy(load_image("orkwalk.png", color_key=-1), 7, 1, 280, 470)
        else:
            ork = Enemy_2(load_image("orkwalk.png", color_key=-1), 7, 1, 200, -50)
        enemies.add(ork)
        return ork


castle = Castle()
gold = 1000


def draw(gold):
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


def draw_tower_1(x, y, f, gold):
    tower = pygame.sprite.Sprite()
    if f == 1:
        tower.image = load_image('1_st_tower.png')
        gold -= 300
    elif f == 2:
        tower.image = load_image('2nd_tower.png')
        gold -= 300
    elif f == 3:
        tower.image = load_image('3_d_tower.png')
        gold -= 300
    elif f == 4:
        tower.image = load_image('4_th_tower.png')
        gold -= 300
    tower.rect = tower.image.get_rect()
    if 221 < x < 243 and 449 < y < 471:
        all_sprites.add(tower)
        tower.rect.x = 210
        tower.rect.y = 430
        screen.blit(tower.image, (x, y))

    if 222 < x < 244 and 352 < y < 374:
        all_sprites.add(tower)
        tower.rect.x = 211
        tower.rect.y = 333
        screen.blit(tower.image, (x, y))

    if 359 < x < 381 and 436 < y < 458:
        all_sprites.add(tower)
        tower.rect.x = 348
        tower.rect.y = 417
        screen.blit(tower.image, (x, y))

    if 359 < x < 381 and 363 < y < 385:
        all_sprites.add(tower)
        tower.rect.x = 348
        tower.rect.y = 344
        screen.blit(tower.image, (x, y))

    if 364 < x < 386 and 245 < y < 267:
        all_sprites.add(tower)
        tower.rect.x = 353
        tower.rect.y = 226
        screen.blit(tower.image, (x, y))

    if 412 < x < 434 and 36 < y < 68:
        all_sprites.add(tower)
        tower.rect.x = 401
        tower.rect.y = 10
        screen.blit(tower.image, (x, y))

    if 518 < x < 540 and 204 < y < 226:
        all_sprites.add(tower)
        tower.rect.x = 507
        tower.rect.y = 170
        screen.blit(tower.image, (x, y))

    if 634 < x < 656 and 203 < y < 225:
        all_sprites.add(tower)
        tower.rect.x = 623
        tower.rect.y = 170
        screen.blit(tower.image, (x, y))

    if 593 < x < 615 and 359 < y < 381:
        all_sprites.add(tower)
        tower.rect.x = 582
        tower.rect.y = 320
        screen.blit(tower.image, (x, y))

    if 747 < x < 769 and 363 < y < 384:
        all_sprites.add(tower)
        tower.rect.x = 736
        tower.rect.y = 320
        screen.blit(tower.image, (x, y))

    if 773 < x < 795 and 232 < y < 254:
        all_sprites.add(tower)
        tower.rect.x = 762
        tower.rect.y = 213
        screen.blit(tower.image, (x, y))
    return gold


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == MYEVENTTYPE:
            if castle.hp > 0:
                gold += 25
        if event.type == MYEVENTTYPE_2:
            wave()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                x, y = pygame.mouse.get_pos()
                gold = draw_tower_1(x, y, 1, gold)

            if event.key == pygame.K_2:
                x, y = pygame.mouse.get_pos()
                gold = draw_tower_1(x, y, 2, gold)

            if event.key == pygame.K_3:
                x, y = pygame.mouse.get_pos()
                gold = draw_tower_1(x, y, 3, gold)

            if event.key == pygame.K_4:
                x, y = pygame.mouse.get_pos()
                gold = draw_tower_1(x, y, 4, gold)

    all_sprites.draw(screen)
    all_sprites.update()
    castle.update()

    draw(gold)

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
