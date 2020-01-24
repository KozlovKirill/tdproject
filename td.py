import pygame, os
pygame.init()

FPS = 10
WIDTH = 960
HEIGHT = 540
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
        self.dx = 5
        self.dy = 0
        self.mode = 'walk'
    def update(self):
        if self.mode == 'walk':
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        if self.rect.x == 195 and self.rect.y == -45:
            self.dx = 0
            self.dy = 10
        elif self.rect.x == 195 and self.rect.y == 95:
            self.dx = 10
            self.dy = 0
        elif self.rect.x == 435 and self.rect.y == 95:
            self.dx = 0
            self.dy = 10
        elif self.rect.x == 435 and self.rect.y == 415:
            self.dx = 10
            self.dy = 0
        elif self.rect.x == 835 and self.rect.y == 415:
            self.dx = 0
            self.dy = -10
        elif self.rect.x == 835 and self.rect.y == 175:
            self.dx = 0
            self.dy = 0
            self.frames = []
            self.cut_sheet(load_image('orkattack.png', color_key=-1), 7, 1)
            self.rect.x = 835
            self.rect.y = 176
            self.cur_frame = 0
            self.image = self.frames[self.cur_frame]
        self.rect.x += self.dx
        self.rect.y += self.dy

all_sprites = pygame.sprite.Group()
field = pygame.sprite.Sprite(all_sprites)
field.image = load_image("game.jpg")
field.image = pygame.transform.scale(field.image, (WIDTH, HEIGHT))
field.rect = field.image.get_rect()

running = True
dragon = Enemy(load_image("orkwalk.png", color_key=-1), 7, 1, 195, -45)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
    screen.fill(pygame.Color("black"))
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()