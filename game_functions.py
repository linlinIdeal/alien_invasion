import sys
import pygame
from bullet import Bullet

def fire_bullet(ship, bullets):
    if len(bullets) < ship.ai_settings.bullet_allowed:
        new_bullet = Bullet(ship)
        bullets.add(new_bullet)
def check_keydown_events(event, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ship, bullets)

def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    

def check_events(ship, bullets):
    for event in pygame.event.get():
        if event.type == pygame.K_q:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        

def update_screen(ship, bullets):
    # 用背景颜色填充屏幕 set screen background color
    ship.screen.fill(ship.ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    # 绘制飞船
    ship.blitme()
    # 让最近绘制的屏幕可见 make the most recently drawn screen visible
    pygame.display.flip()

def update_bullets(bullets):
    bullets.update()
    # 删除已消失的子弹
    # we use copy here. Think why
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
