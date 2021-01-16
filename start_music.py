import pygame
pygame.init()
start = pygame.mixer.Channel(0)
fon = pygame.mixer.Channel(1)
jump_hero = pygame.mixer.Channel(2)
hero_in_air = pygame.mixer.Channel(3)
end = pygame.mixer.Channel(4)
arrow = pygame.mixer.Channel(5)
win = pygame.mixer.Channel(6)
start_go = pygame.mixer.Sound('music/3, 2, 1.wav')
fon_music = pygame.mixer.Sound('music/fon.wav')
jump = pygame.mixer.Sound('music/jump.wav')
in_air = pygame.mixer.Sound('music/hero_in_air.wav')
end_game = pygame.mixer.Sound('music/end_game.wav')
arrow_player = pygame.mixer.Sound('music/arrow.wav')
winner_mus = pygame.mixer.Sound('music/winner.wav')


def mixers_music():
    global fon_music
    global start
    global fon
    fon_music.set_volume(0.3)
    start.play(start_go)
    fon.play(fon_music)
