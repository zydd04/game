import pygame
import random
import sys
import time
import math
import copy

import pygame.locals

WIDTH = 800
HEIGHT = 400
LIVES = 1
BLACK = (0, 0, 0)


pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kairo")

background = pygame.image.load("mainbg.png")
road = pygame.image.load("road.png")

player = pygame.image.load("player.png").convert_alpha()

lose = False

s = pygame.image.load("s.png").convert_alpha()

sx = 300
sy = 170

showh = True
shows = True

player_x = 350
player_y = 170
player_vel_y = 0
player_speed = 5
gravity = 0.5
jump_strength = -10
on_ground = True



ennemy = pygame.image.load("ennemy.png")
ennemy2 = pygame.image.load("ennemy2.png")

ennemy_x = 790
ennemy_y = 170

ennemy2_x = 10
ennemy2_y = 170

ennemy_speed = 3
ennemy2_speed = 3

lives = LIVES
score = 0

hi_score = 0

road_scroll = 0
road_speed = 3

font = pygame.font.SysFont(None, 30)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()

    

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and on_ground:
        player_vel_y = jump_strength    
        on_ground = False
        score += 1
    
    player_vel_y += gravity
    player_y += player_vel_y

    if player_y >= 170:
        player_y = 170
        player_vel_y = 0
        on_ground = True

    player_x = max(0,  min(player_x, WIDTH - player.get_width()))
    
    if keys[pygame.K_LEFT]:
        player = pygame.image.load("player2.png").convert_alpha()
        player_x -= player_speed

    if keys[pygame.K_RIGHT]:
        player = pygame.image.load("player.png").convert_alpha()
        player_x += player_speed
    
    def touch(x1, y1, w1, h1, x2, y2, w2, h2) :
          return (
        x1 < x2 + w2 and
        x1 + w1 > x2 and
        y1 < y2 + h2 and
        y1 + h1 > y2
          )
   

    road_scroll += road_speed
    if road_scroll >= road.get_width():
        road_scroll = 0

    screen.blit(background, (0, 0))

    for i in range(2):
        screen.blit(road, ( i * road.get_width() - road_scroll, 250))
    

    if touch(player_x, player_y, player.get_width(), player.get_height(), sx, sy, s.get_width(), s.get_height()) & shows == True:
        player_speed *= 2
        shows = False
    
    if touch(player_x, player_y, player.get_width(), player.get_height(), ennemy_x, ennemy_y, ennemy.get_width(), ennemy.get_height()) :
        lives -= 1
        player_speed = 5
    
    if touch(player_x, player_y, player.get_width(), player.get_height(), ennemy2_x, ennemy2_y, ennemy2.get_width(), ennemy2.get_height()) :
        lives -= 1
        player_speed = 5
    
    if ennemy_x < 0:
        ennemy_x = 799
       

    ennemy_x -= ennemy_speed

    if ennemy2_x > 800:
        ennemy2_x = 0
        
    
    ennemy2_x += ennemy2_speed

    screen.blit(ennemy, (ennemy_x, ennemy_y))
    screen.blit(ennemy2, (ennemy2_x, ennemy2_y))
        
    if shows == True:
        screen.blit(s, (sx, sy))
        

    screen.blit(player, (player_x, player_y))

    if lives < 1:
        lose = True
        player_speed = 0
        ennemy2_speed = 0
        ennemy_speed = 0 
        jump_strength = 0
        text = font.render(("WASTED! Press Space to Restart."), True, (255, 255, 255))
        screen.blit(text, (200, 175))

    if event.type == pygame.KEYUP and lives < 1:
        
        if event.key == pygame.K_SPACE and lose:
            score = 0
            lives = 1 
            player_x = 350
            player_y = 170
            jump_strength = -10
            player_speed = 5
            on_ground = True
            ennemy_speed = 3
            ennemy_x = 790
            ennemy_y = 170
            ennemy2_x = 10
            ennemy2_y = 170
            ennemy2_speed = 3
            shows = True
    
    if score > hi_score:
        hi_score = score

    score_text = font.render(f"Score: {score}", True, BLACK)
    
    hi_score_text = font.render(f"High Score: {hi_score}", True, BLACK)
    screen.blit(score_text, (50, 370))
   
    screen.blit(hi_score_text, (50, 350))

    
    clock = pygame.time.Clock()

    pygame.display.flip()
    clock.tick(60)
