import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    # 初始化游戏 initialize game
    pygame.init()
    ai_settings = Settings()

    # 创建屏幕对象 create a screen for the game
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('外星人入侵-Alien Invasion')

    # 创建Play按钮
    play_button = Button(ai_settings, screen, 'Play')

    ship = Ship(ai_settings, screen)
    bullets = Group()
    # alien = Alien(ai_settings, screen)

    aliens = Group()
    gf.create_fleet(ship, aliens)

    stats = GameStats(ai_settings)
    # 创建记分牌
    sb = Scoreboard(ai_settings, screen, stats)
    # 进入游戏主循环 start the main loop
    while True:
        # 监视事件 watch events
        gf.check_events(ship, aliens, bullets, play_button, sb, stats)
        if stats.game_active:
            # 更新飞船
            ship.update()
            # 更新子弹
            gf.update_bullets(ship, bullets, aliens, stats, sb)
            # 更新外星人
            gf.update_aliens(ship, aliens, bullets, stats, sb)
                
        # 更新屏幕
        gf.update_screen(ship, bullets, aliens, stats, sb, play_button)

run_game()