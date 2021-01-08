import pygame
import os
import sys
import datetime
import time
from PIL import Image, ImageFilter

pygame.init()
isUP = False
isUP1 = False

count_UP = 0
count_DOWN = 0
count_UP1 = 0
count_DOWN1 = 0
finish = 0


def main():
    global finish
    global isUP1
    global isUP
    global count_UP
    global count_DoWN
    start = pygame.mixer.Channel(0)
    fon = pygame.mixer.Channel(1)
    jump_hero = pygame.mixer.Channel(2)
    hero_in_air = pygame.mixer.Channel(3)
    end = pygame.mixer.Channel(4)
    arrow = pygame.mixer.Channel(5)
    start_go = pygame.mixer.Sound('music/3, 2, 1.wav')
    fon_music = pygame.mixer.Sound('music/fon.wav')
    fon_music.set_volume(0.3)
    jump = pygame.mixer.Sound('music/jump.wav')
    in_air = pygame.mixer.Sound('music/hero_in_air.wav')
    end_game = pygame.mixer.Sound('music/end_game.wav')
    arrow_player = pygame.mixer.Sound('music/arrow.wav')
    start.play(start_go)
    fon.play(fon_music)

    clock = pygame.time.Clock()
    fps = 31
    Bird_update = 10
    screen_width = 864
    screen_height = 760

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Chicken-Run')

    # define game variables

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
        'wall': load_image('ground.jpg'),
        'finish-line': pygame.transform.scale(load_image('Finish-line.png'), (95, 230))
    }
    tile_width = tile_height = 50

    tiles_group = pygame.sprite.Group()
    tiles_group1 = pygame.sprite.Group()
    tiles_group3 = pygame.sprite.Group()
    tiles_group4 = pygame.sprite.Group()
    start_group = pygame.sprite.Group()
    finish_group = pygame.sprite.Group()
    arrows_group = pygame.sprite.Group()

    image1 = pygame.transform.scale(load_image('Chicken-up_stay.png'), (40, 50))  # motion animation
    image2 = pygame.transform.scale(load_image('Chicken-up_run.png'), (40, 50))  # motion animation
    images_UP = []
    images_UP.append(image1)
    images_UP.append(image2)

    image3 = pygame.transform.scale(load_image('Chicken-down_stay.png'), (40, 50))  # motion animation
    image4 = pygame.transform.scale(load_image('Chicken-down_run.png'), (40, 50))  # motion animation
    images_DOWN = []
    images_DOWN.append(image3)
    images_DOWN.append(image4)

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
            self.image = load_image('box.jpg')
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y + 30)

    class Tile4(pygame.sprite.Sprite):
        def __init__(self, tile_type, pos_x, pos_y):
            super().__init__(tiles_group4)
            self.image = load_image('box.jpg')
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y - 50)

    class Finish_line(pygame.sprite.Sprite):
        def __init__(self, tile_type, pos_x, pos_y):
            super().__init__(finish_group)
            self.image = tile_images[tile_type]
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect().move(
                tile_width * pos_x + 60, tile_height * pos_y)

    class Arrow(pygame.sprite.Sprite):
        def __init__(self, tile_type, pos_x, pos_y):
            super().__init__(arrows_group)
            self.image = pygame.transform.scale(load_image('arrow.png'), (65, 65))
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)

    class Bird(pygame.sprite.Sprite):
        def __init__(self, sheet, level):
            super().__init__(bird_group)
            self.frames = []
            self.image = sheet
            self.x = 0
            self.y = 0
            self.vel = 10
            self.rect = self.image.get_rect()
            for y in range(len(level)):
                for x in range(len(level[y])):
                    if level[y][x] == '@':
                        self.y = y * tile_height
                        self.x = x * tile_width

        def update(self):
            global finish
            global winner
            if start == 0:
                self.x += 0.4
            if pygame.sprite.spritecollideany(self, tiles_group3):
                self.x -= 5

            if pygame.sprite.spritecollideany(self, tiles_group4):
                self.x -= 5
            self.rect = self.image.get_rect().move(self.x, self.y)

            if isUP == True:
                draw_UP()
            if not pygame.sprite.spritecollideany(self, tiles_group1) and isUP == False:
                if not pygame.sprite.spritecollideany(self, tiles_group4) and isUP == False:
                    self.y += self.vel
                else:
                    self.x += 5
            if not pygame.sprite.spritecollideany(self, tiles_group) and isUP == True:
                if not pygame.sprite.spritecollideany(self, tiles_group3) and isUP == True:
                    self.y -= self.vel
                else:
                    self.x += 5
            if pygame.sprite.spritecollideany(self, finish_group):
                end.play(end_game)
                fon_music.set_volume(0)
                finish = 1
                if winner == 0:
                    winner = 'flappy'
            if pygame.sprite.spritecollideany(self, arrows_group):
                    arrow.play(arrow_player)
                    self.x += 240


    class Bird1(pygame.sprite.Sprite):
        def __init__(self, sheet, level):
            super().__init__(bird_group)
            self.frames = []
            self.image = sheet
            self.x = 0
            self.y = 0
            self.vel = 10
            self.rect = self.image.get_rect()
            for y in range(len(level)):
                for x in range(len(level[y])):
                    if level[y][x] == '@':
                        self.y = y * tile_height
                        self.x = x * tile_width

        def update(self):
            global finish
            global winner
            if start == 0:
                self.x += 0.4
            if pygame.sprite.spritecollideany(self, tiles_group3):
                self.x -= 5

            if pygame.sprite.spritecollideany(self, tiles_group4):
                self.x -= 5
            self.rect = self.image.get_rect().move(self.x, self.y)

            if isUP1 == True:
                draw_UP1()
            if not pygame.sprite.spritecollideany(self, tiles_group1) and isUP1 == False:
                if not pygame.sprite.spritecollideany(self, tiles_group4) and isUP1 == False:
                    self.y += self.vel
                else:
                    self.x += 5
            if not pygame.sprite.spritecollideany(self, tiles_group) and isUP1 == True:
                if not pygame.sprite.spritecollideany(self, tiles_group3) and isUP1 == True:
                    self.y -= self.vel
                else:
                    self.x += 5
            if pygame.sprite.spritecollideany(self, finish_group):
                end.play(end_game)
                fon_music.set_volume(0)
                finish = 1
                if winner == 0:
                    winner = 'flappy1'
            if pygame.sprite.spritecollideany(self, arrows_group):
                    arrow.play(arrow_player)
                    self.x += 240


    class Start_line(pygame.sprite.Sprite):
        def __init__(self, sheet, level):
            super().__init__(start_group)
            self.image = sheet
            self.x = 0
            self.y = 0
            self.vel = 10
            self.rect = self.image.get_rect()
            for y in range(len(level)):
                for x in range(len(level[y])):
                    if level[y][x] == '/':
                        self.y = y * tile_height - 110
                        self.x = x * tile_width - 80

        def update(self):
            self.rect = self.image.get_rect().move(self.x, self.y)

    class Button():
        def __init__(self, x, y, image):
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.clicked = False

        def draw(self):
            action = False

            # get mouse position
            pos = pygame.mouse.get_pos()

            # check mouseover and clicked conditions
            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    action = True
                    self.clicked = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            # draw button
            screen.blit(self.image, self.rect)

            return action

    def draw_UP():  # motion animation
        global count_UP
        if count_UP == 4:
            count_UP = 0
        flappy.image = images_UP[count_UP // 2]
        count_UP += 1

    def draw_DOWN():  # motion animation
        global count_DOWN
        if count_DOWN == 4:
            count_DOWN = 0
        flappy.image = images_DOWN[count_DOWN // 2]
        count_DOWN += 1

    def draw_UP1():  # motion animation
        global count_UP1
        if count_UP1 == 4:
            count_UP1 = 0
        flappy1.image = images_UP[count_UP1 // 2]
        count_UP1 += 1

    def draw_DOWN1():  # motion animation
        global count_DOWN1
        if count_DOWN1 == 4:
            count_DOWN1 = 0
        flappy1.image = images_DOWN[count_DOWN1 // 2]
        count_DOWN1 += 1

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
                    if a <= 43:
                        Tile('wall', x - c, y)  # upper blocks
                        a += 1
                    else:
                        Tile1('wall', x - c, y)  # lower blockы
                elif level[y][x] == '|':
                    Finish_line('finish-line', x - c, y)
                elif level[y][x] == '!':
                    if a <= 43:
                        Tile('wall', x - c, y)
                        Tile3('wall', x - c, y)  # upper barriers
                        a += 1
                    else:
                        Tile1('wall', x - c, y)
                        Tile4('wall', x - c, y)  # lower barriers
                elif level[y][x] == '>':
                    Arrow('arrow', x - c, y)

        # we will return the player, as well as the size of the field in cells
        return new_player, x, y

    def blur_background():
        time.sleep(1.5)
        rect = pygame.Rect(0, 0, 864, 760)
        sub = screen.subsurface(rect)
        pygame.image.save(sub, "screenshot.jpg")
        im = Image.open('screenshot.jpg')
        im = im.filter(ImageFilter.GaussianBlur(radius=2))  # Blur background screenshot
        im.save('screenshot.jpg')
        bg = pygame.image.load('screenshot.jpg')
        screen.blit(bg, (0, 0))

    bird_group = pygame.sprite.Group()
    level_map = load_level('map.txt')
    flappy = Bird(pygame.transform.scale(load_image('Chicken-down_stay.png'), (40, 50)), level_map)
    flappy1 = Bird1(pygame.transform.scale(load_image('Chicken-down_stay.png'), (40, 50)), level_map)
    start_line = Start_line(
        pygame.transform.rotate(pygame.transform.scale(load_image('Start-line.png'), (170, 150)), 90),
        level_map)
    bird_group.add(flappy)
    bird_group.add(flappy1)
    start_group.add(start_line)

    winner = 0
    map_speed = 1
    start = 1  # start line close
    run = True
    first_time = datetime.datetime.now()
    lose = 0
    restart_img = pygame.transform.scale(pygame.image.load('data/restart.png'), (95, 95))
    home_img = pygame.transform.scale(pygame.image.load('data/home.png'), (110, 110))
    restart_button = Button(screen_width // 2 + 30, screen_height // 2 - 80, restart_img)
    home_button = Button(screen_width // 2 - 120, screen_height // 2 - 90, home_img)

    while run:
        clock.tick(fps)
        if finish == 0:
            if flappy.x < 0 and lose == 0:
                hero_in_air.play(in_air)
                fon_music.set_volume(0)
                lose = 1
                finish = 1
                winner = 'flappy'
                blur_background()  # blur
            if flappy.y <= 265 and lose == 0 and finish == 0:
                hero_in_air.play(in_air)
                fon_music.set_volume(0)
                lose = 1
                finish = 1
                winner = 'flappy'
                blur_background()  # blur
            if flappy.y >= 510 and lose == 0 and finish == 0:
                hero_in_air.play(in_air)
                fon_music.set_volume(0)
                lose = 1
                finish = 1
                winner = 'flappy'
                blur_background()  # blur


            if flappy1.x < 0 and lose == 0:
                hero_in_air.play(in_air)
                fon_music.set_volume(0)
                lose = 1
                finish = 1
                winner = 'flappy1'
                blur_background()  # blur
            if flappy1.y <= 265 and lose == 0 and finish == 0:
                hero_in_air.play(in_air)
                fon_music.set_volume(0)
                lose = 1
                finish = 1
                winner = 'flappy1'
                blur_background()  # blur
            elif flappy1.y >= 510 and lose == 0 and finish == 0:
                hero_in_air.play(in_air)
                fon_music.set_volume(0)
                lose = 1
                finish = 1
                winner = 'flappy1'
                blur_background()  # blur


            flappy.update()
            flappy1.update()


            if isUP1 == False:
                draw_DOWN1()

            if isUP == False:
                draw_DOWN()
            # draw background
            tiles_group = pygame.sprite.Group()  # upper blocks
            tiles_group1 = pygame.sprite.Group()  # lower blocks
            tiles_group3 = pygame.sprite.Group()  # upper barriers
            tiles_group4 = pygame.sprite.Group()  # lower barriers
            finish_group = pygame.sprite.Group()  # lower barriers
            arrows_group = pygame.sprite.Group()  # lower barriers
            screen.blit(bg, (0, 0))
            hero, level_x, level_y = generate_level(level_map, map_speed)

            tiles_group.draw(screen)
            tiles_group.update()
            tiles_group1.draw(screen)
            tiles_group1.update()
            tiles_group3.draw(screen)
            tiles_group3.update()
            tiles_group4.draw(screen)
            tiles_group4.update()
            finish_group.draw(screen)
            finish_group.update()
            bird_group.draw(screen)
            bird_group.update()
            arrows_group.draw(screen)
            arrows_group.update()
        start_group.draw(screen)
        start_group.update()

        if start == 0:  # run after start line
            map_speed += 0.1
            start_line.update()
        second_time = datetime.datetime.now()
        delta = second_time - first_time
        if '03' == str(delta).split(':')[2].split('.')[0]:  # 3 seconds stop
            start = 0  # start line open
            start_line.x = -100
            start_line.y = 0

        if finish == 1:
            blur_background()  # blur

            restart_button.draw()  # RESTART BUTTON
            home_button.draw()  # HOME BUTTON
            win_baner = pygame.transform.scale(pygame.image.load('data/win_baner.png'), (250, 100))
            screen.blit(win_baner, (310, 80))
            if winner == 'flappy':
                flapp = pygame.transform.scale(pygame.image.load('data/Chicken-down_stay.png'), (40, 50))
                screen.blit(flapp, (415, 150))

            elif winner == 'flappy1':
                flapp = pygame.transform.scale(pygame.image.load('data/Chicken-down_stay.png'), (40, 50))
                screen.blit(flapp, (415, 150))
            flappy = 0
            flappy1 = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            key = pygame.key.get_pressed()
            if key[pygame.K_UP] and isUP == False and finish == 0:
                jump_hero.play(jump)
                isUP = True
                bird_group.draw(screen)
                bird_group.update()
            if key[pygame.K_DOWN] and isUP == True and finish == 0:
                jump_hero.play(jump)
                isUP = False

            if key[pygame.K_w] and isUP1 == False and finish == 0:
                jump_hero.play(jump)
                isUP1 = True
                bird_group.draw(screen)
                bird_group.update()
            if key[pygame.K_s] and isUP1 == True and finish == 0:
                jump_hero.play(jump)
                isUP1 = False

            if event.type == pygame.MOUSEBUTTONDOWN and finish == 1:
                if 562 >= event.pos[0] >= 462 and 300 <= event.pos[1] <= 400:  # PUSH RESTART
                    finish = 0
                    main()  # RESTART

        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
