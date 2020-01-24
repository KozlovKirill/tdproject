import pygame, os, time
from random import randint

pygame.init()

MYEVENTTYPE = 31

MYEVENTTYPE_2 = 30

towers = [[221, 449, 243, 471, None], [222, 352, 244, 374, None], [359, 436, 381, 458, None],
          [359, 363, 381, 385, None], [364, 245, 386, 267, None],
          [412, 46, 434, 68, None], [518, 204, 540, 226, None],
          [634, 203, 656, 225, None], [593, 359, 615, 381, None], [747, 363, 769, 384, None],
          [773, 232, 795, 254, None]]

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
            # Р РЋР вЂљР  Р’В°Р  Р’В·Р  Р вЂ Р  РЎвЂР  Р’В»Р  РЎвЂќР  Р’В°
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
                    self.mode = 'attack'
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
                    self.mode = 'attack'
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

class Tower(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.cost = 0

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
gold = 10000


def draw_tower_1(x, y, f, gold, buy, towers):
    if gold >= buy:
        for i in range(len(towers)):
            if towers[i][0] <= x <= towers[i][2] and towers[i][1] <= y <= towers[i][3]:
                towers[i][-1] = Tower()
                n = i
    flag = False
    if f == 1:
        towers[n][-1].image = load_image('1st_tower.png')
        towers[n][-1].cost = 300
    elif f == 2:
        towers[n][-1].image = load_image('2nd_tower.png')
        towers[n][-1].cost = 500
    elif f == 3:
        towers[n][-1].image = load_image('3d_tower.png')
        towers[n][-1].cost = 1000
    elif f == 4:
        towers[n][-1].image = load_image('4th_tower.png')
        towers[n][-1].cost = 1500
    towers[n][-1].rect = towers[n][-1].image.get_rect()
    if gold >= buy:
        if 221 <= x <= 243 and 449 <= y <= 471:
            all_sprites.add(towers[n][-1])
            towers[n][-1].rect.x = 210
            towers[n][-1].rect.y = 430
            screen.blit(towers[n][-1].image, (x, y))
            flag = True

        elif 222 <= x <= 244 and 352 <= y <= 374:
            all_sprites.add(towers[n][-1])
            towers[n][-1].rect.x = 211
            towers[n][-1].rect.y = 333
            screen.blit(towers[n][-1].image, (x, y))
            flag = True

        elif 359 <= x <= 381 and 436 <= y <= 458:
            all_sprites.add(towers[n][-1])
            towers[n][-1].rect.x = 348
            towers[n][-1].rect.y = 417
            screen.blit(towers[n][-1].image, (x, y))
            flag = True

        elif 359 <= x <= 381 and 363 <= y <= 385:
            all_sprites.add(towers[n][-1])
            towers[n][-1].rect.x = 348
            towers[n][-1].rect.y = 344
            screen.blit(towers[n][-1].image, (x, y))
            flag = True

        elif 364 <= x <= 386 and 245 <= y <= 267:
            all_sprites.add(towers[n][-1])
            towers[n][-1].rect.x = 353
            towers[n][-1].rect.y = 226
            screen.blit(towers[n][-1].image, (x, y))
            flag = True

        elif 412 <= x <= 434 and 36 <= y <= 68:
            all_sprites.add(towers[n][-1])
            towers[n][-1].rect.x = 401
            towers[n][-1].rect.y = 10
            screen.blit(towers[n][-1].image, (x, y))
            flag = True

        elif 518 <= x <= 540 and 204 <= y <= 226:
            all_sprites.add(towers[n][-1])
            towers[n][-1].rect.x = 507
            towers[n][-1].rect.y = 170
            screen.blit(towers[n][-1].image, (x, y))
            flag = True

        elif 634 <= x <= 656 and 203 <= y <= 225:
            all_sprites.add(towers[n][-1])
            towers[n][-1].rect.x = 623
            towers[n][-1].rect.y = 170
            screen.blit(towers[n][-1].image, (x, y))
            flag = True

        elif 593 <= x <= 615 and 359 <= y <= 381:
            all_sprites.add(towers[n][-1])
            towers[n][-1].rect.x = 582
            towers[n][-1].rect.y = 320
            screen.blit(towers[n][-1].image, (x, y))
            flag = True

        elif 747 <= x <= 769 and 363 <= y <= 384:
            all_sprites.add(towers[n][-1])
            towers[n][-1].rect.x = 736
            towers[n][-1].rect.y = 320
            screen.blit(towers[n][-1].image, (x, y))
            flag = True

        elif 773 <= x <= 795 and 232 <= y <= 254:
            all_sprites.add(towers[n][-1])
            towers[n][-1].rect.x = 762
            towers[n][-1].rect.y = 213
            screen.blit(towers[n][-1].image, (x, y))
            flag = True
        else:
            flag = False
    if gold >= buy:
        if f == 1 and flag:
            gold -= 300
        elif f == 2 and flag:
            gold -= 500
        elif f == 3 and flag:
            gold -= 1000
        elif f == 4 and flag:
            gold -= 1500
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


def pause():
    paused = True
    pygame.mixer.music.load('data/pause.mp3')
    pygame.mixer.music.play(-1)
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        font = pygame.font.Font(None, 35)
        text = font.render(str('pause - press the Enter key to continue'), 1, (0, 0, 0))
        screen.blit(text, (300, 20))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False
            pygame.mixer.music.stop()
            pygame.mixer.music.load('data/fon.mp3')
            pygame.mixer.music.play(-1)

        pygame.display.update()
        clock.tick(15)


pygame.mixer.music.load('data/fon.mp3')
pygame.mixer.music.play(-1)

# spawn_ork = pygame.mixer.Sound('data/spawn.mp3')

time_gold = 1000
time_wave = 5000
pygame.time.set_timer(MYEVENTTYPE, time_gold)  # gold
pygame.time.set_timer(MYEVENTTYPE_2, time_wave)  # wave

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)

        if event.type == MYEVENTTYPE:
            if castle.hp > 0:
                gold += 25
                wave()

        if event.type == MYEVENTTYPE_2:
            # spawn_ork.play(1)
            if time_wave > 1000:
                time_wave -= 1000
            pygame.time.set_timer(MYEVENTTYPE, time_wave)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                x, y = pygame.mouse.get_pos()
                for i in towers:
                    if i[0] <= x <= i[2] and i[1] <= y <= i[3] and i[-1] is None:
                        gold, towers = draw_tower_1(x, y, 1, gold, 300, towers)

            if event.key == pygame.K_2:
                x, y = pygame.mouse.get_pos()
                for i in towers:
                    if i[0] <= x <= i[2] and i[1] <= y <= i[3] and i[-1] is None:
                        gold, towers = draw_tower_1(x, y, 2, gold, 500, towers)

            if event.key == pygame.K_3:
                x, y = pygame.mouse.get_pos()
                for i in towers:
                    if i[0] <= x <= i[2] and i[1] <= y <= i[3] and i[-1] is None:
                        gold, towers = draw_tower_1(x, y, 3, gold, 1000, towers)

            if event.key == pygame.K_4:
                x, y = pygame.mouse.get_pos()
                for i in towers:
                    if i[0] <= x <= i[2] and i[1] <= y <= i[3] and i[-1] is None:
                        gold, towers = draw_tower_1(x, y, 4, gold, 1500, towers)

            if event.key == pygame.K_DELETE:
                x, y = pygame.mouse.get_pos()
                for i in towers:
                    if i[0] <= x <= i[2] and i[1] <= y <= i[3] and i[-1] is not None:
                        gold += (i[-1].cost) // 2
                        i[-1].kill()
                        i[-1] = None

            if event.key == pygame.K_ESCAPE:
                pygame.mixer.music.stop()
                pause()

    all_sprites.draw(screen)
    all_sprites.update()
    castle.update()

    draw(gold)

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()

# def cursor():
#    Cursor = load_image('Р РЈРљРђ.png', (255, 255, 255))
#    Cursor = pygame.transform.scale(Cursor, (30, 30))
#    if pygame.mouse.get_focused():
#        pygame.mouse.set_visible(0)
#        screen.blit(Cursor, pygame.mouse.get_pos())
