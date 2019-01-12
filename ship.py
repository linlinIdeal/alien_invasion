import pygame
import system
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        # 获取图片路径（Linux系统和Windows系统路径不同）
        ship_img = system.real_path('images/ship.bmp')
        
        # 加载飞船，获取其外接矩形
        self.image = pygame.image.load(ship_img)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 将每艘飞船放在屏幕底部重要
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
    
        self.center = float(self.rect.centerx)

        self.moving_right = False
        self.moving_left = False
        self.ship_speed_factor = ai_settings.ship_speed_factor
        
    def blitme(self):
        # 绘制飞船
        self.screen.blit(self.image, self.rect)
    
    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.centerx += self.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.rect.centerx -= self.ship_speed_factor

    def center_ship(self):
        self.center = self.screen_rect.centerx    

