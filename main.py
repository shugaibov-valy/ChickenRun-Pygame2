import pygame
import os
import sys
import datetime
import time
from PIL import Image, ImageFilter
from gif_chikens import *

pygame.init()
click_red_chicken = 'down'
click_blue_chicken = 'down'

count_UP = 0
count_DOWN = 0
count_UP1 = 0
count_DOWN1 = 0
finish = 0
winner = 0
d = 0


def main():
    global d
    d = 0
    global winner
    global finish
    global click_red_chicken
    global click_blue_chicken
    global count_UP
    global count_DOWN

    clock = pygame.time.Clock()
    fps = 31
    Bird_update = 10
    screen_width = 864
    screen_height = 760
    d = 0
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

    tile_width = tile_height = 50

    gif_chickens()

    up_earth_group = pygame.sprite.Group()
    low_earth_group = pygame.sprite.Group()
    up_barrier_box_group = pygame.sprite.Group()
    low_barrier_box_group = pygame.sprite.Group()
    start_group = pygame.sprite.Group()
    finish_group = pygame.sprite.Group()
    arrows_group = pygame.sprite.Group()
    waters_group = pygame.sprite.Group()

    tile_images = {
        'wall': load_image('ground.jpg'),
        'finish-line': pygame.transform.scale(load_image('Finish-line.png'), (95, 230))
    }

    class UpperEarth(pygame.sprite.Sprite):
        def __init__(self, tile_type, pos_x, pos_y):
            super().__init__(up_earth_group)
            self.image = tile_images[tile_type]
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)

    class LowerEarth(pygame.sprite.Sprite):
        def __init__(self, tile_type, pos_x, pos_y):
            super().__init__(low_earth_group)
            self.image = tile_images[tile_type]
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)

    class UpperBarrierBox(pygame.sprite.Sprite):
        def __init__(self, pos_x, pos_y):
            super().__init__(up_barrier_box_group)
            self.image = pygame.transform.scale(load_image('box.jpg'), (40, 40))
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y + 30)

    class LowerBarrierBox(pygame.sprite.Sprite):
        def __init__(self, pos_x, pos_y):
            super().__init__(low_barrier_box_group)
            self.image = pygame.transform.scale(load_image('box.jpg'), (40, 40))
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y - 30)

    class Water(pygame.sprite.Sprite):
        def __init__(self, pos_x, pos_y):
            super().__init__(waters_group)
            self.image = pygame.transform.scale(load_image('water.png'), (100, 33))
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)

    class Finish_line(pygame.sprite.Sprite):
        def __init__(self, tile_type, pos_x, pos_y):
            super().__init__(finish_group)
            self.image = tile_images[tile_type]
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect().move(
                tile_width * pos_x + 60, tile_height * pos_y)

    class Arrow(pygame.sprite.Sprite):
        def __init__(self, pos_x, pos_y):
            super().__init__(arrows_group)
            self.image = pygame.transform.scale(load_image('arrow.png'), (85, 85))
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
                    if level[y][x] == '$':
                        self.y = y * tile_height
                        self.x = x * tile_width

        def update(self):
            global finish
            global winner
            if start == 0:
                self.x += 0.4
            if pygame.sprite.spritecollideany(self, up_barrier_box_group):
                self.x -= 5

            if pygame.sprite.spritecollideany(self, low_barrier_box_group):
                self.x -= 5
            self.rect = self.image.get_rect().move(self.x, self.y)

            if click_red_chicken == 'up':
                draw_chicken_red_up()
            if not pygame.sprite.spritecollideany(self, low_earth_group) and click_red_chicken == 'down':
                if chicken_red.y >= chicken_blue.y or not pygame.sprite.spritecollideany(self,
                                                                                         bird_group1) and click_red_chicken == 'down':
                    if not pygame.sprite.spritecollideany(self, low_barrier_box_group) and click_red_chicken == 'down':
                        self.y += self.vel
                    else:
                        self.x += 5
            if not pygame.sprite.spritecollideany(self, up_earth_group) and click_red_chicken == 'up':
                if chicken_red.y <= chicken_blue.y or not pygame.sprite.spritecollideany(self,
                                                                                         bird_group1) or chicken_red.y >= chicken_blue.y and click_red_chicken == 'up':
                    if not pygame.sprite.spritecollideany(self, up_barrier_box_group) and click_red_chicken == 'up':
                        self.y -= self.vel
                    else:
                        self.x += 5
            if pygame.sprite.spritecollideany(self, finish_group):
                end.play(end_game)
                fon_music.set_volume(0)
                finish = 1
                if winner == 0:
                    winner = 'chicken_red'
            if pygame.sprite.spritecollideany(self, arrows_group):
                arrow.play(arrow_player)
                self.x += 240
            if pygame.sprite.spritecollideany(self, waters_group):
                self.x += 10
                self.y += 20

    class Bird1(pygame.sprite.Sprite):
        def __init__(self, sheet, level):
            super().__init__(bird_group1)
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
            if pygame.sprite.spritecollideany(self, up_barrier_box_group):
                self.x -= 5

            if pygame.sprite.spritecollideany(self, low_barrier_box_group):
                self.x -= 5
            self.rect = self.image.get_rect().move(self.x, self.y)

            if click_blue_chicken == 'up':
                draw_chicken_blue_up()
            if not pygame.sprite.spritecollideany(self, low_earth_group) and click_blue_chicken == 'down':
                if chicken_blue.y >= chicken_red.y or not pygame.sprite.spritecollideany(self,
                                                                                         bird_group) and click_blue_chicken == 'down':
                    if not pygame.sprite.spritecollideany(self, low_barrier_box_group) and click_blue_chicken == 'down':
                        self.y += self.vel
                    else:
                        self.x += 5
            if not pygame.sprite.spritecollideany(self, up_earth_group) and click_blue_chicken == 'up':
                if chicken_blue.y <= chicken_red.y or not pygame.sprite.spritecollideany(self,
                                                                                         bird_group) and click_blue_chicken == 'up':
                    if not pygame.sprite.spritecollideany(self, up_barrier_box_group) and click_blue_chicken == 'up':
                        self.y -= self.vel
                    else:
                        self.x += 5
            if pygame.sprite.spritecollideany(self, finish_group):
                end.play(end_game)
                fon_music.set_volume(0)
                finish = 1
                if winner == 0:
                    winner = 'chicken_blue'
            if pygame.sprite.spritecollideany(self, arrows_group):
                arrow.play(arrow_player)
                self.x += 240
            if pygame.sprite.spritecollideany(self, waters_group):
                self.x += 10
                self.y += 20

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

    def draw_chicken_red_up():  # motion animation
        global count_UP
        if count_UP == 4:
            count_UP = 0
        chicken_red.image = chicken_red_up_gif[count_UP // 2]
        count_UP += 1

    def draw_chicken_red_down():  # motion animation
        global count_DOWN
        if count_DOWN == 4:
            count_DOWN = 0
        chicken_red.image = chicken_red_down_gif[count_DOWN // 2]
        count_DOWN += 1

    def draw_chicken_blue_up():  # motion animation
        global count_UP1
        if count_UP1 == 4:
            count_UP1 = 0
        chicken_blue.image = chicken_blue_up_gif[count_UP1 // 2]
        count_UP1 += 1

    def draw_chicken_blue_down():  # motion animation
        global count_DOWN1
        if count_DOWN1 == 4:
            count_DOWN1 = 0
        chicken_blue.image = chicken_blue_down_gif[count_DOWN1 // 2]
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
                    if a <= 40:
                        UpperEarth('wall', x - c, y)  # upper blocks
                        a += 1
                    else:
                        LowerEarth('wall', x - c, y)  # lower blocks
                elif level[y][x] == '|':
                    Finish_line('finish-line', x - c, y)
                elif level[y][x] == '~':
                    Water(x - c, y)
                elif level[y][x] == '!':
                    if a <= 40:
                        UpperEarth('wall', x - c, y)
                        UpperBarrierBox(x - c, y)  # upper barriers
                        a += 1
                    else:
                        LowerEarth('wall', x - c, y)
                        LowerBarrierBox(x - c, y)  # lower barriers
                elif level[y][x] == '>':
                    Arrow(x - c, y)

        # we will return the player, as well as the size of the field in cells
        return new_player, x, y

    def blur_background():
        global d
        if d == 0:
            time.sleep(1.5)
            print(d)
            rect = pygame.Rect(0, 0, 864, 760)
            sub = screen.subsurface(rect)
            pygame.image.save(sub, "screenshot.jpg")
            im = Image.open('screenshot.jpg')
            im = im.filter(ImageFilter.GaussianBlur(radius=2))  # Blur background screenshot
            im.save('screenshot.jpg')
            bg = pygame.image.load('screenshot.jpg')
            screen.blit(bg, (0, 0))
            d += 1

    bird_group = pygame.sprite.Group()
    bird_group1 = pygame.sprite.Group()
    level_map = load_level('map.txt')
    chicken_red = Bird(pygame.transform.scale(load_image('ChickenRed-down_stay.png'), (40, 50)), level_map)
    chicken_blue = Bird1(pygame.transform.scale(load_image('ChickenBlue-down_stay.png'), (40, 50)), level_map)
    start_line = Start_line(
        pygame.transform.rotate(pygame.transform.scale(load_image('Start-line.png'), (170, 150)), 90),
        level_map)
    bird_group.add(chicken_red)
    bird_group1.add(chicken_blue)
    start_group.add(start_line)

    map_speed = 1
    start = 1  # start line close
    run = True
    lose = 0
    restart_img = pygame.transform.scale(pygame.image.load('data/restart.png'), (95, 95))
    home_img = pygame.transform.scale(pygame.image.load('data/home.png'), (110, 110))
    restart_button = Button(screen_width // 2 + 30, screen_height // 2 - 80, restart_img)
    home_button = Button(screen_width // 2 - 120, screen_height // 2 - 90, home_img)
    blur = 0
    d = 0
    w = 0

    def terminate():
        pygame.quit()
        sys.exit()

    def loading():
        loading_fons = []
        loading = 0
        loading_time = 0
        fon1 = pygame.transform.scale(load_image('Loading1.png'), (864, 760))
        loading_fons.append(fon1)
        fon2 = pygame.transform.scale(load_image('Loading2.png'), (864, 760))
        loading_fons.append(fon2)
        while loading_time < 40:
            screen.blit(loading_fons[loading], (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
            pygame.display.flip()
            if loading <= 1:
                clock.tick(10)
                loading += 1
            if loading == 2:
                loading = 0
            loading_time += 1

    def start_screen():
        global run
        loading_use = 0
        count_fon = 0
        start_fons = []
        fon0 = pygame.transform.scale(load_image('START1.png'), (864, 760))
        start_fons.append(fon0)
        fon2 = pygame.transform.scale(load_image('Chicken_anim_fon1.png'), (864, 760))
        start_fons.append(fon2)
        fon3 = pygame.transform.scale(load_image('Chicken_anim_fon2.png'), (864, 760))
        start_fons.append(fon3)
        fon4 = pygame.transform.scale(load_image('Chicken_anim_fon3.png'), (864, 760))
        start_fons.append(fon4)
        fon5 = pygame.transform.scale(load_image('Chicken_anim_fon4.png'), (864, 760))
        start_fons.append(fon5)

        while True:
            print(count_fon)
            screen.blit(start_fons[count_fon], (0, 0))
            for event in pygame.event.get():
                if count_fon > 1:
                    if event.type == pygame.QUIT:
                        terminate()
                    elif event.type == pygame.KEYDOWN or \
                            event.type == pygame.MOUSEBUTTONDOWN:

                        #                        pygame.mixer.music.play(loops=0, start=0.0)
                        run = True
                        return
            pygame.display.flip()
            if count_fon <= 1:
                clock.tick(0.5)
                count_fon += 1
            if loading_use < 1:
                clock.tick(0.5)
                loading()
                loading_use += 1
            if count_fon > 1:
                clock.tick(2)
                count_fon += 1
            if count_fon > 4:
                count_fon = 2

    start_screen()

    start = pygame.mixer.Channel(0)
    fon = pygame.mixer.Channel(1)
    jump_hero = pygame.mixer.Channel(2)
    hero_in_air = pygame.mixer.Channel(3)
    end = pygame.mixer.Channel(4)
    arrow = pygame.mixer.Channel(5)
    win = pygame.mixer.Channel(6)
    start_go = pygame.mixer.Sound('music/3, 2, 1.wav')
    fon_music = pygame.mixer.Sound('music/fon.wav')
    fon_music.set_volume(0.3)
    jump = pygame.mixer.Sound('music/jump.wav')
    in_air = pygame.mixer.Sound('music/hero_in_air.wav')
    end_game = pygame.mixer.Sound('music/end_game.wav')
    arrow_player = pygame.mixer.Sound('music/arrow.wav')
    winner_mus = pygame.mixer.Sound('music/winner.wav')
    start.play(start_go)
    fon.play(fon_music)

    first_time = datetime.datetime.now()
    while run:
        clock.tick(fps)
        if finish == 0:
            if chicken_red.x < 0 and lose == 0:
                hero_in_air.play(in_air)
                fon_music.set_volume(0)
                lose = 1
                finish = 1
                winner = 'chicken_blue'
                blur_background()

            if chicken_red.y <= 265 and lose == 0:
                hero_in_air.play(in_air)
                fon_music.set_volume(0)
                lose = 1
                finish = 1
                winner = 'chicken_blue'
                blur_background()  # blur
            if chicken_red.y >= 510 and lose == 0:
                hero_in_air.play(in_air)
                fon_music.set_volume(0)
                lose = 1
                finish = 1
                winner = 'chicken_blue'
                blur_background()  # blur

            if chicken_blue.x < 0 and lose == 0:
                hero_in_air.play(in_air)
                fon_music.set_volume(0)
                lose = 1
                finish = 1
                winner = 'chicken_red'
                blur_background()  # blur

            if chicken_blue.y <= 265 and lose == 0 and finish == 0:
                hero_in_air.play(in_air)
                fon_music.set_volume(0)
                lose = 1
                finish = 1
                winner = 'chicken_red'
                blur_background()  # blur
            elif chicken_blue.y >= 510 and lose == 0 and finish == 0:
                hero_in_air.play(in_air)
                fon_music.set_volume(0)
                lose = 1
                finish = 1
                winner = 'chicken_red'
                blur_background()  # blur

            chicken_red.update()
            chicken_blue.update()

            if click_blue_chicken == 'down':
                draw_chicken_blue_down()

            if click_red_chicken == 'down':
                draw_chicken_red_down()
            # draw background
            up_earth_group = pygame.sprite.Group()  # upper blocks
            low_earth_group = pygame.sprite.Group()  # lower blocks
            up_barrier_box_group = pygame.sprite.Group()  # upper barriers
            low_barrier_box_group = pygame.sprite.Group()  # lower barriers
            finish_group = pygame.sprite.Group()  # lower barriers
            arrows_group = pygame.sprite.Group()  # lower barriers
            waters_group = pygame.sprite.Group()  # lower barriers
            screen.blit(bg, (0, 0))
            hero, level_x, level_y = generate_level(level_map, map_speed)

            up_earth_group.draw(screen)
            up_earth_group.update()
            low_earth_group.draw(screen)
            low_earth_group.update()
            up_barrier_box_group.draw(screen)
            up_barrier_box_group.update()
            low_barrier_box_group.draw(screen)
            low_barrier_box_group.update()
            finish_group.draw(screen)
            finish_group.update()
            bird_group.draw(screen)
            bird_group.update()
            bird_group1.draw(screen)
            bird_group1.update()
            arrows_group.draw(screen)
            arrows_group.update()
            waters_group.draw(screen)
            waters_group.update()
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
            if winner == 'chicken_red':
                flapp = pygame.transform.scale(pygame.image.load('data/ChickenRed-down_stay.png'), (40, 50))
                screen.blit(flapp, (415, 150))

            elif winner == 'chicken_blue':
                flapp = pygame.transform.scale(pygame.image.load('data/ChickenBlue-down_stay.png'), (40, 50))
                screen.blit(flapp, (415, 150))
            if w == 0:
                win.play(winner_mus)
                w += 1
            winner = 0
            chicken_red = 0
            chicken_blue = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            key = pygame.key.get_pressed()
            if key[pygame.K_UP] and click_red_chicken == 'down' and finish == 0:
                jump_hero.play(jump)
                click_red_chicken = 'up'
                bird_group.draw(screen)
                bird_group.update()
            if key[pygame.K_DOWN] and click_red_chicken == 'up' and finish == 0:
                jump_hero.play(jump)
                click_red_chicken = 'down'

            if key[pygame.K_w] and click_blue_chicken == 'down' and finish == 0:
                jump_hero.play(jump)
                click_blue_chicken = 'up'
                bird_group1.draw(screen)
                bird_group1.update()
            if key[pygame.K_s] and click_blue_chicken == 'up' and finish == 0:
                jump_hero.play(jump)
                click_blue_chicken = 'down'

            if event.type == pygame.MOUSEBUTTONDOWN and finish == 1:
                if 562 >= event.pos[0] >= 462 and 300 <= event.pos[1] <= 400:  # PUSH RESTART
                    end_game.set_volume(0)
                    finish = 0
                    bird_group = pygame.sprite.Group()
                    bird_group1 = pygame.sprite.Group()
                    level_map = load_level('map.txt')
                    chicken_red = Bird(pygame.transform.scale(load_image('ChickenRed-down_stay.png'), (40, 50)),
                                       level_map)
                    chicken_blue = Bird1(pygame.transform.scale(load_image('ChickenBlue-down_stay.png'), (40, 50)),
                                         level_map)
                    start_line = Start_line(
                        pygame.transform.rotate(pygame.transform.scale(load_image('Start-line.png'), (170, 150)), 90),
                        level_map)
                    bird_group.add(chicken_red)
                    bird_group1.add(chicken_blue)
                    start_group.add(start_line)

                    map_speed = 1
                    start = 1  # start line close
                    # run = True
                    lose = 0
                    restart_img = pygame.transform.scale(pygame.image.load('data/restart.png'), (95, 95))
                    home_img = pygame.transform.scale(pygame.image.load('data/home.png'), (110, 110))
                    restart_button = Button(screen_width // 2 + 30, screen_height // 2 - 80, restart_img)
                    home_button = Button(screen_width // 2 - 120, screen_height // 2 - 90, home_img)
                    blur = 0
                    d = 0
                    w = 0
                    first_time = datetime.datetime.now()

                    start = pygame.mixer.Channel(0)
                    fon = pygame.mixer.Channel(1)
                    jump_hero = pygame.mixer.Channel(2)
                    hero_in_air = pygame.mixer.Channel(3)
                    end = pygame.mixer.Channel(4)
                    arrow = pygame.mixer.Channel(5)
                    win = pygame.mixer.Channel(6)
                    start_go = pygame.mixer.Sound('music/3, 2, 1.wav')
                    fon_music = pygame.mixer.Sound('music/fon.wav')
                    fon_music.set_volume(0.3)
                    jump = pygame.mixer.Sound('music/jump.wav')
                    in_air = pygame.mixer.Sound('music/hero_in_air.wav')
                    end_game = pygame.mixer.Sound('music/end_game.wav')
                    arrow_player = pygame.mixer.Sound('music/arrow.wav')
                    winner_mus = pygame.mixer.Sound('music/winner.wav')
                    start.play(start_go)
                    fon.play(fon_music)

                    run = True  # RESTART
                elif 462 >= event.pos[0] >= 320 and 300 <= event.pos[1] <= 400:  # PUSH HOME
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
