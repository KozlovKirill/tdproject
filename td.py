import pygame, os, time
from random import randint
from pygame import mixer

pygame.init()

MYEVENTTYPE = 31
MYEVENTTYPE_2 = 30
SHIELD = 29
SHIELD_TABLE = 27
HEAL_TABLE = 26
ARROW_TABLE = 25
HEAL = 28
score = 0
towers = [[221, 449, 243, 471, None], [222, 352, 244, 374, None], [359, 436, 381, 458, None],
          [359, 363, 381, 385, None], [364, 245, 386, 267, None],
          [412, 46, 434, 68, None], [518, 204, 540, 226, None],
          [634, 203, 656, 225, None], [593, 359, 615, 381, None], [747, 363, 769, 384, None],
          [773, 232, 795, 254, None]]

f = open('data/score.txt')
l = max([int(line.strip()) for line in f])

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


pygame.display.set_caption('Tower_Defense')
pygame.display.set_icon(load_image("icon.png"))


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
        self.x = -960

    def update(self):
        pygame.draw.rect(screen, pygame.Color('green'), (739, 534, self.hp, 17))
        if self.hp <= 0 and self.crushed == False:
            global waveactive
            fire.add(AnimatedSprite(load_image('fire.png', color_key=-1), 10, 6, 774, 106))
            fire.add(AnimatedSprite(load_image('fire.png', color_key=-1), 10, 6, 885, 96))
            fire.add(AnimatedSprite(pygame.transform.scale(load_image('fire.png', color_key=-1), (960, 576)), 10, 6, 815, 90))
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
        self.q = 0
        self.fr = False

    def attack(self, target):
        target.hp -= target.damage

    def update(self):
        if self.mode == 'walk':
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            if self.q == 0:
                self.image = self.frames[self.cur_frame]
            if self.q == 1:
                self.image = pygame.transform.flip(self.frames[self.cur_frame], True, False)

            if self.rect.x == 280 and self.rect.y == 450:
                self.q = 1
                self.dx = 0
                self.dy = -5
            elif self.rect.x == 280 and self.rect.y == 260:
                self.dx = -5
                self.dy = 0
            elif self.rect.x == 120 and self.rect.y == 260:
                self.dx = 0
                self.dy = -5
                self.q = 0
            elif self.rect.x == 120 and self.rect.y == 100:
                self.dx = 5
                self.dy = 0
            if self.c == 1:
                if self.rect.x == 440 and self.rect.y == 100:
                    self.dx = 0
                    self.dy = 5
                elif self.rect.x == 440 and self.rect.y == 420:
                    self.dx = 5
                    self.dy = 0
                elif self.rect.x == 840 and self.rect.y == 420:
                    self.dx = 0
                    self.dy = -5
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
            else:
                if self.rect.x == 670 and self.rect.y == 100:
                    self.q = 1
                    self.dx = 0
                    self.dy = 5
                elif self.rect.x == 670 and self.rect.y == 250:
                    self.dx = -5
                    self.dy = 0
                elif self.rect.x == 440 and self.rect.y == 250:
                    self.q = 0
                    self.dx = 0
                    self.dy = 5
                elif self.rect.x == 440 and self.rect.y == 420:
                    self.dx = 5
                    self.dy = 0
                elif self.rect.x == 840 and self.rect.y == 420:
                    self.dx = 0
                    self.dy = -5
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
            if self.cur_frame == 4 and shield_f == False:
                self.attack(castle)


class Enemy_2(Enemy):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(sheet, columns, rows, x, y)

    def update(self):
        if self.mode == 'walk':
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            if self.q == 0:
                self.image = self.frames[self.cur_frame]
            if self.q == 1:
                self.image = pygame.transform.flip(self.frames[self.cur_frame], True, False)

            if self.rect.x == 200 and self.rect.y == -50:
                self.dx = 0
                self.dy = 5
            elif self.rect.x == 200 and self.rect.y == 100:
                self.dx = 5
                self.dy = 0
            if self.c == 1:
                if self.rect.x == 440 and self.rect.y == 100:
                    self.dx = 0
                    self.dy = 5
                elif self.rect.x == 440 and self.rect.y == 420:
                    self.dx = 5
                    self.dy = 0
                elif self.rect.x == 840 and self.rect.y == 420:
                    self.dx = 0
                    self.dy = -5
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
            else:
                if self.rect.x == 670 and self.rect.y == 100:
                    self.q = 1
                    self.dx = 0
                    self.dy = 5
                elif self.rect.x == 670 and self.rect.y == 250:
                    self.dx = -5
                    self.dy = 0
                elif self.rect.x == 440 and self.rect.y == 250:
                    self.q = 0
                    self.dx = 0
                    self.dy = 5
                elif self.rect.x == 440 and self.rect.y == 420:
                    self.dx = 5
                    self.dy = 0
                elif self.rect.x == 840 and self.rect.y == 420:
                    self.dx = 0
                    self.dy = -5
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
            if self.cur_frame == 4 and shield_f == False:
                self.attack(castle)


class Tower(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.cost = 0
        self.type = 0
        self.cannonball = None
        self.spike = None
        self.light = None
        self.arrow = None
        self.t = 0
        self.cd = False

    def attack(self, x, y):
        if self.type == 1:
            if self.cannonball is None:
                self.cannonball = pygame.sprite.Sprite(all_sprites)
                self.cannonball.image = load_image('round_bomb_lit.png', color_key=-1)
                self.cannonball.image = pygame.transform.scale(self.cannonball.image, (24, 24))
                self.cannonball.rect = self.cannonball.image.get_rect()
                self.cannonball.rect.x = self.rect.x + 26
                self.cannonball.rect.y = self.rect.y + 10
                self.vx = (x - self.rect.x) // 15
                self.vy = (y - self.rect.y) // 15

        if self.type == 4:
            if self.spike is None:
                self.spike = AnimatedSprite(load_image('spike.png', color_key=-1), 6, 2, x, y)

        if self.type == 3:
            if self.light is None:
                self.light = AnimatedSprite(load_image('lightning.png', color_key=-1), 3, 1, x, y)

        if self.type == 2:
            self.arrow = pygame.sprite.Sprite(all_sprites)
            self.arrow.image = load_image('копье.png', -1)
            self.arrow.image = pygame.transform.scale(self.arrow.image, (24, 24))
            self.arrow.rect = self.arrow.image.get_rect()
            self.arrow.rect.x = self.rect.x + 26
            self.arrow.rect.y = self.rect.y + 10
            self.vx = (x - self.rect.x) // 15
            self.vy = (y - self.rect.y) // 15

    def update(self):
        if self.type == 1:
            if self.cannonball is None:
                cr = None
                for enemy in enemies:
                    r = ((enemy.rect.x - self.rect.x) ** 2 + (
                            enemy.rect.y - self.rect.y) ** 2) ** 0.5

                    if cr is None or r < cr:
                        cr = r
                        self.tx = enemy.rect.x + 15 * enemy.dx
                        self.ty = enemy.rect.y + 15 * enemy.dy
                        self.rx = abs(enemy.rect.x - self.rect.x)
                        self.ry = abs(enemy.rect.y - self.rect.y)
                if cr is not None and cr <= 150 and cr >= 25 and self.cd == False:
                    self.attack(self.tx, self.ty)
                    self.cd = True

            else:
                if self.cannonball.rect.x != self.tx and self.cannonball.rect.y != self.ty \
                        and self.rx >= abs(self.vx) and self.ry >= abs(self.vy):
                    self.cannonball.rect.x += self.vx
                    self.cannonball.rect.y += self.vy
                    self.rx -= abs(self.vx)
                    self.ry -= abs(self.vy)
                else:
                    for enemy in enemies:
                        r = ((enemy.rect.x - self.cannonball.rect.x) ** 2 + (
                                enemy.rect.y - self.cannonball.rect.y) ** 2) \
                            ** 0.5

                        if r <= 25:
                            enemy.hp -= 30
                            if enemy.hp <= 0:
                                enemy.kill()

                    self.cannonball.kill()
                    self.cannonball = None
                    self.tx = None
                    self.ty = None
                    self.rx = None
                    self.ry = None
            if self.cd:
                if self.t == 30:  # cooldawn
                    self.t = 0
                    self.cd = False
                else:
                    self.t += 1

        elif self.type == 2:
            if self.arrow is None:
                cr = None
                for enemy in enemies:
                    r = ((enemy.rect.x - self.rect.x) ** 2 + (
                            enemy.rect.y - self.rect.y) ** 2) ** 0.5
                    if cr is None or r < cr:
                        cr = r
                        self.tx = enemy.rect.x + 15 * enemy.dx
                        self.ty = enemy.rect.y + 15 * enemy.dy
                        self.rx = abs(enemy.rect.x - self.rect.x)
                        self.ry = abs(enemy.rect.y - self.rect.y)
                if cr is not None and cr <= 150 and cr >= 25 and self.cd == False:
                    self.attack(self.tx, self.ty)
                    self.cd = True
            else:
                if self.arrow.rect.x != self.tx and self.arrow.rect.y != self.ty \
                        and self.rx >= abs(self.vx) and self.ry >= abs(self.vy):
                    self.arrow.rect.x += self.vx
                    self.arrow.rect.y += self.vy
                    self.rx -= abs(self.vx)
                    self.ry -= abs(self.vy)
                else:
                    for enemy in enemies:
                        r = ((enemy.rect.x - self.arrow.rect.x) ** 2 + (
                                enemy.rect.y - self.arrow.rect.y) ** 2) \
                            ** 0.5

                        if r <= 25:
                            enemy.hp -= 50
                            if enemy.hp <= 0:
                                enemy.kill()

                    self.arrow.kill()
                    self.arrow = None
                    self.tx = None
                    self.ty = None
                    self.rx = None
                    self.ry = None
            if self.cd:
                if self.t == 50:
                    self.t = 0
                    self.cd = False
                else:
                    self.t += 1

        elif self.type == 4:
            if self.spike is None:
                if not self.cd:
                    cr = None
                    self.ce = None
                    self.cex = None
                    self.cey = None
                    for enemy in enemies:
                        r = ((enemy.rect.x - self.rect.x) ** 2 + (
                                enemy.rect.y - self.rect.y) ** 2) ** 0.5
                        if (cr is None or r < cr) and not enemy.fr and (enemy.dx, enemy.dy) != (0, 0):
                            cr = r
                            self.tx = enemy.rect.x
                            self.ty = enemy.rect.y - 50
                            self.ce = enemy
                            self.cex = enemy.dx
                            self.cey = enemy.dy
                            enemy.hp -= 1
                            if enemy.hp <= 0:
                                enemy.kill()

                    if cr is not None and cr <= 150 and cr >= 25 \
                            and self.cd == False and not self.ce.fr:
                        self.attack(self.tx, self.ty)
                        self.ce.fr = True
                        self.ce.dx = 0
                        self.ce.dy = 0
                        self.cd = True
                if self.cd:
                    if self.t == 50:
                        self.t = 0
                        self.cd = False
                    else:
                        self.t += 1
            else:
                if self.spike.cur_frame == 11:
                    im = self.spike.frames[-1]
                    self.spike.frames = [im]
                    self.cur_frame = 0
                if self.cd:
                    if self.t == 20:
                        self.t = 0
                        self.spike.kill()
                        self.spike = None
                        self.ce.dx = self.cex
                        self.ce.dy = self.cey
                        self.ce.fr = False
                    else:
                        self.t += 1
        elif self.type == 3:
            if self.light is None:
                cr = None
                for enemy in enemies:
                    r = ((enemy.rect.x - self.rect.x) ** 2 + (
                            enemy.rect.y - self.rect.y) ** 2) ** 0.5
                    if cr is None or r < cr:
                        cr = r
                        self.tx = enemy.rect.x
                        self.ty = enemy.rect.y - 160
                        self.ce = enemy
                if cr is not None and cr <= 150 and cr >= 25 and self.cd == False:
                    self.attack(self.tx, self.ty)
                    self.ce.kill()
                    self.ce = None
                    self.cd = True
                if self.cd:
                    if self.t == 90:
                        self.t = 0
                        self.cd = False
                    else:
                        self.t += 1
            else:
                if self.light.cur_frame == 2:
                    self.light.kill()
                    self.light = None


all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
towers_sprites = pygame.sprite.Group()
fire = pygame.sprite.Group()
field = pygame.sprite.Sprite(all_sprites)
field.image = load_image("game.jpg")
field.image = pygame.transform.scale(field.image, (WIDTH, HEIGHT))
field.rect = field.image.get_rect()

running = True


def wave():
    if waveactive:
        if randint(0, 1) == 0:
            ork = Enemy(load_image("orkwalk.png", color_key=-1), 7, 1, 280, 450)
        else:
            ork = Enemy_2(load_image("orkwalk.png", color_key=-1), 7, 1, 200, -50)
        enemies.add(ork)
        return ork


castle = Castle()
gold = 2000


def draw_tower_1(x, y, f, gold, buy, towers):
    if gold >= buy:
        for i in range(len(towers)):
            if towers[i][0] <= x <= towers[i][2] and towers[i][1] <= y <= towers[i][3]:
                towers[i][-1] = Tower()
                n = i
    flag = False
    if gold >= buy:
        if f == 1:
            towers[n][-1].image = load_image('1st_tower.png')
            towers[n][-1].cost = 300
            towers[n][-1].type = 1
        elif f == 2:
            towers[n][-1].image = load_image('2nd_tower.png')
            towers[n][-1].cost = 500
            towers[n][-1].type = 2
        elif f == 3:
            towers[n][-1].image = load_image('3d_tower.png')
            towers[n][-1].cost = 1000
            towers[n][-1].type = 3
        elif f == 4:
            towers[n][-1].image = load_image('4th_tower.png')
            towers[n][-1].cost = 1500
            towers[n][-1].type = 4
        towers[n][-1].rect = towers[n][-1].image.get_rect()
    if gold >= buy:
        if 221 <= x <= 243 and 449 <= y <= 471:
            towers_sprites.add(towers[n][-1])
            towers[n][-1].rect.x = 210
            towers[n][-1].rect.y = 430
            screen.blit(towers[n][-1].image, (x, y))
            flag = True

        elif 222 <= x <= 244 and 352 <= y <= 374:
            towers_sprites.add(towers[n][-1])
            towers[n][-1].rect.x = 211
            towers[n][-1].rect.y = 333
            screen.blit(towers[n][-1].image, (x, y))
            flag = True

        elif 359 <= x <= 381 and 436 <= y <= 458:
            towers_sprites.add(towers[n][-1])
            towers[n][-1].rect.x = 348
            towers[n][-1].rect.y = 417
            screen.blit(towers[n][-1].image, (x, y))
            flag = True

        elif 359 <= x <= 381 and 363 <= y <= 385:
            towers_sprites.add(towers[n][-1])
            towers[n][-1].rect.x = 348
            towers[n][-1].rect.y = 344
            screen.blit(towers[n][-1].image, (x, y))
            flag = True

        elif 364 <= x <= 386 and 245 <= y <= 267:
            towers_sprites.add(towers[n][-1])
            towers[n][-1].rect.x = 353
            towers[n][-1].rect.y = 226
            screen.blit(towers[n][-1].image, (x, y))
            flag = True

        elif 412 <= x <= 434 and 36 <= y <= 68:
            towers_sprites.add(towers[n][-1])
            towers[n][-1].rect.x = 401
            towers[n][-1].rect.y = 10
            screen.blit(towers[n][-1].image, (x, y))
            flag = True

        elif 518 <= x <= 540 and 204 <= y <= 226:
            towers_sprites.add(towers[n][-1])
            towers[n][-1].rect.x = 507
            towers[n][-1].rect.y = 170
            screen.blit(towers[n][-1].image, (x, y))
            flag = True

        elif 634 <= x <= 656 and 203 <= y <= 225:
            towers_sprites.add(towers[n][-1])
            towers[n][-1].rect.x = 623
            towers[n][-1].rect.y = 170
            screen.blit(towers[n][-1].image, (x, y))
            flag = True

        elif 593 <= x <= 615 and 359 <= y <= 381:
            towers_sprites.add(towers[n][-1])
            towers[n][-1].rect.x = 582
            towers[n][-1].rect.y = 320
            screen.blit(towers[n][-1].image, (x, y))
            flag = True

        elif 747 <= x <= 769 and 363 <= y <= 384:
            towers_sprites.add(towers[n][-1])
            towers[n][-1].rect.x = 736
            towers[n][-1].rect.y = 320
            screen.blit(towers[n][-1].image, (x, y))
            flag = True

        elif 773 <= x <= 795 and 232 <= y <= 254:
            towers_sprites.add(towers[n][-1])
            towers[n][-1].rect.x = 762
            towers[n][-1].rect.y = 213
            screen.blit(towers[n][-1].image, (x, y))
            flag = True
        else:
            flag = False
    if gold >= buy:
        if f == 1 and flag:
            gold -= buy
            stoika.play()
        elif f == 2 and flag:
            gold -= buy
            stoika.play()
        elif f == 3 and flag:
            gold -= buy
            stoika.play()
        elif f == 4 and flag:
            gold -= buy
            stoika.play()
    return gold, towers


def draw(gold):
    font = pygame.font.Font(None, 35)
    text = font.render(str(gold), 1, (204, 204, 0))
    text_x = 810
    text_y = 22
    screen.blit(text, (text_x, text_y))

    if 315 < pygame.mouse.get_pos()[0] < 370 and 515 < pygame.mouse.get_pos()[1] < 590:
        text = font.render(str(300), 1, (204, 204, 0))
        text_x = 315
        text_y = 540
        screen.blit(text, (text_x, text_y))

    if 388 < pygame.mouse.get_pos()[0] < 442 and 515 < pygame.mouse.get_pos()[1] < 590:
        text = font.render(str(500), 1, (204, 204, 0))
        text_x = 388
        text_y = 540
        screen.blit(text, (text_x, text_y))

    if 465 < pygame.mouse.get_pos()[0] < 520 and 515 < pygame.mouse.get_pos()[1] < 590:
        text = font.render(str(1000), 1, (204, 204, 0))
        text_x = 465
        text_y = 540
        screen.blit(text, (text_x, text_y))

    if 535 < pygame.mouse.get_pos()[0] < 591 and 515 < pygame.mouse.get_pos()[1] < 590:
        text = font.render(str(1500), 1, (204, 204, 0))
        text_x = 535
        text_y = 540
        screen.blit(text, (text_x, text_y))


def pause(volume, run, zastavka, restart):
    paused = True
    pygame.mixer.music.load('data/pause.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(volume)

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 380 <= x <= 565 and 410 <= y <= 470:  # exit
                    run = False
                    pygame.quit()
                    quit()

                if 380 <= x <= 565 and 330 <= y <= 395:  # main menu
                    zastavka = True
                    pygame.mixer.music.load('data/zastavka.mp3')
                    pygame.mixer.music.play(-1)
                    return volume, run, zastavka, restart

                if 380 <= x <= 565 and 255 <= y <= 320:  # restart
                    restart = True
                    return volume, run, zastavka, restart

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if volume > 0:
                        volume -= 0.1
                    pygame.mixer.music.set_volume(volume)

                if event.key == pygame.K_RIGHT:
                    if volume < 1:
                        volume += 0.1
                    pygame.mixer.music.set_volume(volume)

        screen.blit(load_image('pause_table.png', -1), (300, 100))
        screen.blit(load_image('main_meny.png', -1), (375, 325))
        screen.blit(load_image('restart.png', -1), (375, 250))
        screen.blit(load_image('exit_table.png', -1), (375, 400))
        pygame.mouse.set_visible(1)

        if volume > 0:
            screen.blit(load_image('volume.png', (255, 255, 255)), (920, 560))
        else:
            screen.blit(load_image('volume_exit.png', (255, 255, 255)), (920, 560))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False
            pygame.mixer.music.stop()
            pygame.mixer.music.load('data/fon.mp3')
            pygame.mixer.music.play(-1)

        pygame.display.update()
        clock.tick(15)
    return volume, run, zastavka, restart


spawn_ork = pygame.mixer.Sound(os.path.join('data', 'spawn_ork.wav'))
stoika = pygame.mixer.Sound(os.path.join('data', 'stroika.wav'))

time_gold = 1000
time_wave = 15000

pygame.time.set_timer(MYEVENTTYPE, time_gold)  # gold
pygame.time.set_timer(MYEVENTTYPE_2, time_wave)  # wave

pygame.time.set_timer(SHIELD, 4000)
pygame.time.set_timer(HEAL, 1)

pygame.time.set_timer(SHIELD_TABLE, 15000)
pygame.time.set_timer(HEAL_TABLE, 15000)
pygame.time.set_timer(ARROW_TABLE, 15000)

volume = 0.5
pygame.mixer.music.set_volume(volume)
pluse_gold = 25


def cursor(shield, heal, arrow, zastavka, info):
    x, y = pygame.mouse.get_pos()
    Cursor = load_image('курсор_2.png', (255, 255, 255))
    Cursor = pygame.transform.scale(Cursor, (30, 30))
    if pygame.mouse.get_focused():
        if zastavka == False:
            if 110 <= x <= 155 and 20 <= y <= 60 and shield == False:
                pygame.mouse.set_visible(0)
                screen.blit(Cursor, pygame.mouse.get_pos())
            elif 805 <= x <= 947 and 12 <= y <= 54:
                pygame.mouse.set_visible(0)
                screen.blit(Cursor, pygame.mouse.get_pos())
            elif 740 <= x <= 780 and 15 <= y <= 55 and shield:
                pygame.mouse.set_visible(0)
                screen.blit(Cursor, pygame.mouse.get_pos())
            elif 690 <= x <= 730 and 15 <= y <= 55 and heal:
                pygame.mouse.set_visible(0)
                screen.blit(Cursor, pygame.mouse.get_pos())
            elif 640 <= x <= 680 and 15 <= y <= 55 and arrow:
                pygame.mouse.set_visible(0)
                screen.blit(Cursor, pygame.mouse.get_pos())
            elif 90 <= x <= 180 and 315 <= y <= 415 and arrow == False:
                pygame.mouse.set_visible(0)
                screen.blit(Cursor, pygame.mouse.get_pos())
            elif 850 <= x <= 900 and 520 <= y <= 570 and heal == False:
                pygame.mouse.set_visible(0)
                screen.blit(Cursor, pygame.mouse.get_pos())

            elif 221 <= x <= 243 and 449 <= y <= 471:
                pygame.mouse.set_visible(0)
                screen.blit(Cursor, pygame.mouse.get_pos())

            elif 222 <= x <= 244 and 352 <= y <= 374:
                pygame.mouse.set_visible(0)
                screen.blit(Cursor, pygame.mouse.get_pos())

            elif 359 <= x <= 381 and 436 <= y <= 458:
                pygame.mouse.set_visible(0)
                screen.blit(Cursor, pygame.mouse.get_pos())

            elif 359 <= x <= 381 and 363 <= y <= 385:
                pygame.mouse.set_visible(0)
                screen.blit(Cursor, pygame.mouse.get_pos())

            elif 364 <= x <= 386 and 245 <= y <= 267:
                pygame.mouse.set_visible(0)
                screen.blit(Cursor, pygame.mouse.get_pos())

            elif 412 <= x <= 434 and 36 <= y <= 68:
                pygame.mouse.set_visible(0)
                screen.blit(Cursor, pygame.mouse.get_pos())

            elif 518 <= x <= 540 and 204 <= y <= 226:
                pygame.mouse.set_visible(0)
                screen.blit(Cursor, pygame.mouse.get_pos())

            elif 634 <= x <= 656 and 203 <= y <= 225:
                pygame.mouse.set_visible(0)
                screen.blit(Cursor, pygame.mouse.get_pos())

            elif 593 <= x <= 615 and 359 <= y <= 381:
                pygame.mouse.set_visible(0)
                screen.blit(Cursor, pygame.mouse.get_pos())

            elif 747 <= x <= 769 and 363 <= y <= 384:
                pygame.mouse.set_visible(0)
                screen.blit(Cursor, pygame.mouse.get_pos())

            elif 773 <= x <= 795 and 232 <= y <= 254:
                pygame.mouse.set_visible(0)
                screen.blit(Cursor, pygame.mouse.get_pos())
            else:
                pygame.mouse.set_visible(1)


shield_f = False
shield_find = False
shield_table = False
shield_c = 0

heal_f = False
heal_find = False
heal_table = False
heal_c = 0

arrow_f = False
arrow_find = False
arrow_table = False
arrow_mousition = False
arrow_c = 0

zastavka = True
information_towers = False
restart = False

pygame.mixer.music.load((os.path.join('data', 'zastavka.mp3')))
pygame.mixer.music.play(-1)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN and zastavka:
            if information_towers == False:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    zastavka = False
                    pygame.mixer.music.load(os.path.join('data', 'fon.mp3'))
                    pygame.mixer.music.play(-1)
                    volume = 0.5
            else:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    information_towers = False

        if event.type == pygame.MOUSEBUTTONDOWN and zastavka:
            x, y = pygame.mouse.get_pos()
            print(x, y)
            if 670 <= x <= 710 and 55 <= y <= 95 and information_towers:
                information_towers = False

            if 920 <= x <= 960 and 560 <= y <= 600:
                if volume != 0:
                    volume = 0
                    pygame.mixer.music.set_volume(volume)
                else:
                    volume = 0.5
                    pygame.mixer.music.set_volume(volume)

            if 325 <= x <= 660 and 520 <= y <= 600:
                information_towers = True
            if 812 <= x <= 954 and 362 <= y <= 440 and information_towers == False:
                zastavka = False
                pygame.mixer.music.load(os.path.join('data', 'fon.mp3'))
                pygame.mixer.music.play(-1)
                volume = 0.5
            if 810 <= x <= 955 and 260 <= y <= 331 and information_towers == False:
                running = False
                pygame.quit()
                quit()

        if event.type == pygame.MOUSEBUTTONDOWN and zastavka == False:
            x, y = pygame.mouse.get_pos()
            if castle.hp <= 0:
                if 400 <= x <= 590 and 415 <= y <= 485:  # exit last
                    pygame.quit()
                    quit()

            if 920 <= x <= 960 and 560 <= y <= 600:
                if volume != 0:
                    volume = 0
                    pygame.mixer.music.set_volume(volume)
                else:
                    volume = 0.5
                    pygame.mixer.music.set_volume(volume)

            if 110 <= x <= 155 and 20 <= y <= 60:
                shield_find = True
                shield_table = True
                shield_c += 1

            if 850 <= x <= 900 and 520 <= y <= 570:
                heal_find = True
                heal_table = True
                heal_c += 1

            if 90 <= x <= 165 and 320 <= y <= 415:
                arrow_find = True
                arrow_table = True
                arrow_c += 1

            if 740 <= x <= 780 and 15 <= y <= 55 and shield_find and shield_table == False:
                if gold >= 2000:
                    shield_f = True
                    gold -= 2000

            if 690 <= x <= 730 and 15 <= y <= 55 and heal_find and heal_table == False:
                if gold >= 2000:
                    heal_f = True
                    if castle.hp < 100:
                        gold -= 2000

            if 640 <= x <= 680 and 15 <= y <= 55 and arrow_find and arrow_table == False:
                if gold >= 2000:
                    arrow_f = True
                    arrow_mousition = True
                    gold -= 2000

        if event.type == SHIELD and arrow_find and zastavka == False:
            if castle.hp > 0:
                arrow_f = False

        if event.type == HEAL and arrow_f and zastavka == False:
            if castle.hp > 0:
                for enemy in enemies:
                    if enemy.rect.x == 835 and enemy.rect.y == 170:
                        enemy.hp -= 0.5
                        if enemy.hp <= 0:
                            enemy.kill()

                arrow_mousition = False

        if event.type == HEAL and heal_find and zastavka == False:
            if castle.hp > 0:
                heal_f = False

        if event.type == SHIELD and shield_find and zastavka == False:
            if castle.hp > 0:
                shield_f = False

        if event.type == SHIELD_TABLE and zastavka == False:
            if shield_find and shield_table:
                shield_table = False

        if event.type == HEAL_TABLE and zastavka == False:
            if heal_find and heal_table:
                heal_table = False

        if event.type == ARROW_TABLE and zastavka == False:
            if arrow_find and arrow_table:
                arrow_table = False

        if event.type == MYEVENTTYPE and zastavka == False:
            if castle.hp > 0:
                gold += pluse_gold

        if event.type == MYEVENTTYPE_2 and zastavka == False:
            if castle.hp > 0:
                spawn_ork.play()
                if time_wave > 2000:
                    time_wave -= 1000
                pygame.time.set_timer(MYEVENTTYPE_2, time_wave)
                wave()
                score += 10

        if event.type == pygame.KEYDOWN and zastavka == False:
            if castle.hp > 0:

                if event.key == pygame.K_1:
                    x, y = pygame.mouse.get_pos()
                    for i in towers:
                        if i[0] <= x <= i[2] and i[1] <= y <= i[3] and i[-1] is None:
                            gold, towers = draw_tower_1(x, y, 1, gold, 300, towers)

            if event.key == pygame.K_2:
                if castle.hp > 0:
                    x, y = pygame.mouse.get_pos()
                    for i in towers:
                        if i[0] <= x <= i[2] and i[1] <= y <= i[3] and i[-1] is None:
                            gold, towers = draw_tower_1(x, y, 2, gold, 500, towers)

            if event.key == pygame.K_3:
                if castle.hp > 0:
                    x, y = pygame.mouse.get_pos()
                    for i in towers:
                        if i[0] <= x <= i[2] and i[1] <= y <= i[3] and i[-1] is None:
                            gold, towers = draw_tower_1(x, y, 3, gold, 1000, towers)

            if event.key == pygame.K_4:
                if castle.hp > 0:
                    x, y = pygame.mouse.get_pos()
                    for i in towers:
                        if i[0] <= x <= i[2] and i[1] <= y <= i[3] and i[-1] is None:
                            gold, towers = draw_tower_1(x, y, 4, gold, 1500, towers)

            if event.key == pygame.K_DELETE:
                if castle.hp > 0:
                    x, y = pygame.mouse.get_pos()
                    for i in towers:
                        if i[0] <= x <= i[2] and i[1] <= y <= i[3] and i[-1] is not None:
                            gold += (i[-1].cost) // 2
                            i[-1].kill()
                            i[-1] = None
                            stoika.play()


            if event.key == pygame.K_ESCAPE:
                pygame.mixer.music.stop()
                volume, running, zastavka, restart = pause(volume, running, zastavka, restart)
                if zastavka or restart:
                    if zastavka:
                        zastavka = True
                    if restart:
                        pygame.mixer.music.load('data/fon.mp3')
                        pygame.mixer.music.play(-1)
                        restart = False

                    for t in towers_sprites:
                        t.kill()
                    for enemy in enemies:
                        enemy.kill()
                    towers = [[221, 449, 243, 471, None], [222, 352, 244, 374, None], [359, 436, 381, 458, None],
                              [359, 363, 381, 385, None], [364, 245, 386, 267, None],
                              [412, 46, 434, 68, None], [518, 204, 540, 226, None],
                              [634, 203, 656, 225, None], [593, 359, 615, 381, None], [747, 363, 769, 384, None],
                              [773, 232, 795, 254, None]]

                    pluse_gold = 25
                    castle.hp = 100
                    score = 0
                    gold = 2000
                    time_wave = 15000
                    pygame.time.set_timer(SHIELD_TABLE, 15000)
                    pygame.time.set_timer(HEAL_TABLE, 15000)
                    pygame.time.set_timer(ARROW_TABLE, 15000)
                    pygame.time.set_timer(MYEVENTTYPE, time_gold)  # gold
                    pygame.time.set_timer(MYEVENTTYPE_2, time_wave)  # wave

                    shield_f = False
                    shield_find = False
                    shield_table = False
                    shield_c = 0

                    heal_f = False
                    heal_find = False
                    heal_table = False
                    heal_c = 0

                    arrow_f = False
                    arrow_find = False
                    arrow_table = False
                    arrow_mousition = False
                    arrow_c = 0

            if event.key == pygame.K_RETURN:
                if shield_table:
                    pygame.time.set_timer(SHIELD_TABLE, 1)
                if heal_table:
                    pygame.time.set_timer(HEAL_TABLE, 1)
                if arrow_table:
                    pygame.time.set_timer(ARROW_TABLE, 1)

            if event.key == pygame.K_LEFT:
                if volume > 0:
                    volume -= 0.1
                pygame.mixer.music.set_volume(volume)

            if event.key == pygame.K_RIGHT:
                if volume < 1:
                    volume += 0.1
                pygame.mixer.music.set_volume(volume)

            if event.key == pygame.K_UP:
                x, y = pygame.mouse.get_pos()
                if 805 <= x <= 945 and 10 <= y <= 55:
                    if gold >= 1000:
                        gold -= 1000
                        pluse_gold += 25

    if zastavka == False:
        if volume > 0:
            screen.blit(load_image('volume.png', (255, 255, 255)), (920, 560))
        else:
            screen.blit(load_image('volume_exit.png', (255, 255, 255)), (920, 560))
        pygame.mixer.music.set_volume(volume)

        all_sprites.draw(screen)
        all_sprites.update()
        towers_sprites.draw(screen)
        towers_sprites.update()
        castle.update()
        draw(gold)
        screen.blit(font.render(str(score), 7, (100, 100, 100)), (50, 535))

        if castle.hp <= 0:
            screen.blit(load_image('exit_table.png', -1), (400, 415))
            screen.blit(load_image('конец.png', -1), (0, 0))

        if arrow_find:
            screen.blit(load_image('look.png'), (640, 15))

        if shield_find:
            screen.blit(load_image('shield.png'), (740, 15))

        if heal_find:
            screen.blit(load_image('heal.png'), (690, 15))

        if shield_table and shield_c <= 1:
            screen.blit(load_image('shield_table.png', -1), (300, 225))
        if heal_table and heal_c <= 1:
            screen.blit(load_image('heal_table_1.png', -1), (300, 225))
        if arrow_table and arrow_c <= 1:
            screen.blit(load_image('arrow_table.png', -1), (300, 225))

        if castle.hp > 0:
            if arrow_f:
                if arrow_f and arrow_find and arrow_table == False:
                    screen.blit(load_image('anazonki.png', -1), (0, 0))
                    screen.blit(load_image('Arrow_1.png', -1), (930, 140))
                    screen.blit(pygame.transform.flip(load_image('Arrow_1.png', -1), True, False), (750, 195))
                    screen.blit(load_image('Arrow_1.png', -1), (780, 190))
                    screen.blit(load_image('Arrow_1.png', -1), (900, 190))

            if shield_f:
                if shield_f and shield_find and shield_table == False:
                    screen.blit(pygame.transform.scale(load_image('ice.png', -1), (100, 185)), (810, 20))
                    screen.blit(load_image('vedma.png', -1), (0, 0))

            if heal_f:
                if heal_f and heal_find and heal_table == False:
                    if castle.hp <= 80:
                        castle.hp += randint(10, 20)
                    elif 80 <= castle.hp <= 95:
                        castle.hp += randint(2, 5)
                    elif 95 <= castle.hp <= 99:
                        castle.hp += 1

        else:
            pygame.mouse.set_visible(1)

    if zastavka:
        pygame.mouse.set_visible(1)
        x, y = pygame.mouse.get_pos()
        screen.blit(load_image('zastavka.png'), (0, 0))
        screen.blit(load_image('svitok.png', -1), (0, 30))

        screen.blit(load_image('best_score.png', -1), (800, 400))

        font = pygame.font.Font(None, 35)
        screen.blit(font.render(str('best score'), 1, (0, 0, 0)), (805, 480))
        screen.blit(font.render(str(l), 1, (0, 0, 0)), (805, 510))
        if 810 <= x <= 953 and 260 <= y <= 332:
            screen.blit(load_image('exit_big.png', -1), (770, 240))
        else:
            screen.blit(load_image('exit.png', -1), (805, 240))

        if 325 <= x <= 650 and 520 <= y <= 600:
            screen.blit(load_image('information_tower_big.png', -1), (300, 470))
        else:
            screen.blit(load_image('information.png', -1), (325, 500))

        if 812 <= x <= 954 and 352 <= y <= 442:
            screen.blit(load_image('play_now_big.png', -1), (770, 360))
        else:
            screen.blit(load_image('play_now.png', -1), (800, 300))
        if information_towers:
            screen.blit(load_image('information_tower.png', -1), (0, 0))

    if information_towers:
        screen.blit(load_image('strelka.png', (255, 255, 255)), (670, 55))

    if volume > 0:
        screen.blit(load_image('volume.png', (255, 255, 255)), (920, 560))
    else:
        screen.blit(load_image('volume_exit.png', (255, 255, 255)), (920, 560))

    cursor(shield_find, heal_find, arrow_find, zastavka, information_towers)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

if castle.hp <= 0:
    f.close()
    f = open('data/score.txt', 'a')
    f.write(str(score) + '\n')
