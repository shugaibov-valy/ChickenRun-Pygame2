import pygame
import os
import sys

pygame.init()

clock = pygame.time.Clock()
fps = 31
Bird_update = 10
screen_width = 864
screen_height = 760

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Chicken-Run')

# define game variables
isUP = False
game_over = False
score = 0

# load images
bg = pygame.image.load('img/bg.png')


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


tile_images = {
    'wall': load_image('box.png'),
}
tile_width = tile_height = 50

tiles_group = pygame.sprite.Group()
tiles_group1 = pygame.sprite.Group()
tiles_group3 = pygame.sprite.Group()
tiles_group4 = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group)
        self.image = tile_images[tile_type]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)


class Tile1(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group1)
        self.image = tile_images[tile_type]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)


class Tile3(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group3)
        self.image = tile_images[tile_type]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)
        self.image = tile_images[tile_type]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y + 50)


class Tile4(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group4)
        self.image = tile_images[tile_type]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)
        self.image = tile_images[tile_type]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y - 50)


class Bird(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, level):
        super().__init__(bird_group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.x = 0
        self.y = 0
        self.vel = 10
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '@':
                    self.y = y * tile_height
                    self.x = x * tile_width

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.x += 2
        if pygame.sprite.spritecollideany(self, tiles_group3):
            self.x -= 5

        if pygame.sprite.spritecollideany(self, tiles_group4):
            self.x -= 5
        self.rect = self.image.get_rect().move(self.x, self.y - 35)
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        if isUP == True:
            self.image = pygame.image.load(f'img/bird1.png')
        if not pygame.sprite.spritecollideany(self, tiles_group1) and isUP == False:
            self.y += self.vel
        if not pygame.sprite.spritecollideany(self, tiles_group) and isUP == True:
            self.y -= self.vel


def load_level(filename):
    filename = "data/" + filename
    # reading the level by removing newline characters
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    # and calculate the maximum length
    max_width = max(map(len, level_map))

    # complete each line with empty cells ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level, c):
    a = 0
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                if a <= 42:
                    Tile('wall', x - c, y)
                    a += 1
                else:
                    Tile1('wall', x - c, y)
            elif level[y][x] == '!':
                if a <= 42:
                    Tile3('wall', x - c, y)
                    a += 1
                else:
                    Tile4('wall', x - c, y)

    # we will return the player, as well as the size of the field in cells
    return new_player, x, y


bird_group = pygame.sprite.Group()
level_map = load_level('map.txt')
flappy = Bird(load_image('Chicken-sprite.png'), 2, 1, level_map)


bird_group.add(flappy)


map_speed = 1

run = True
while run:

    clock.tick(fps)

    # draw background
    tiles_group = pygame.sprite.Group()
    tiles_group1 = pygame.sprite.Group()
    tiles_group3 = pygame.sprite.Group()
    tiles_group4 = pygame.sprite.Group()

    screen.blit(bg, (0, 0))
    hero, level_x, level_y = generate_level(level_map, map_speed)

    map_speed += 0.1
    tiles_group.draw(screen)
    tiles_group.update()
    tiles_group1.draw(screen)
    tiles_group1.update()
    tiles_group3.draw(screen)
    tiles_group3.update()
    tiles_group4.draw(screen)
    tiles_group4.update()
    bird_group.draw(screen)
    bird_group.update()
    flappy.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and isUP == False:
            isUP = True
            bird_group.draw(screen)
            bird_group.update()
        if key[pygame.K_DOWN] and isUP == True:
            isUP = False
    pygame.display.update()
pygame.quit()
