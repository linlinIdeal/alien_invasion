import sys
import pygame

def check_keydown_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True

def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ship):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ship)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        

def update_screen(ship):
    # 用背景颜色填充屏幕 set screen background color
    ship.screen.fill(ship.ai_settings.bg_color)
    # 绘制飞船
    ship.blitme()
    # 让最近绘制的屏幕可见 make the most recently drawn screen visible
    pygame.display.flip()
