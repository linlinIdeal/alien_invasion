import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group

def run_game():
    # 初始化游戏 initialize game
    pygame.init()
    ai_settings = Settings()

    # 创建屏幕对象 create a screen for the game
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('外星人入侵-Alien Invasion')

    ship = Ship(ai_settings, screen)
    bullets = Group()
    # 进入游戏主循环 start the main loop
    while True:
        # 监视事件 watch events
        gf.check_events(ship, bullets)

        # 更新飞船
        ship.update()

        # 更新子弹
        gf.update_bullets(bullets)
        
        # 更新屏幕
        gf.update_screen(ship,bullets)

run_game()