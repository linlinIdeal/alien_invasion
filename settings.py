class Settings():
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 600
        self.bg_color = (230, 230, 230)
        # self.bullet_speed_factor = 1
        self.bullt_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 3
        # self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        # fleet_direction表示外星人移动方向： 1是向右，-1是向左， 
        # self.fleet_direction = 1 
        # 飞船数量
        self.ship_limit = 3
        # 游戏加速节奏
        self.speedup_scale = 1.1
        # 外星人点数的提高速度
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    # 动态参数部分
    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        # fleet_direction表示外星人移动方向： 1是向右，-1是向左
        self.fleet_direction = 1
        # 记分
        self.alien_points = 50

    # 提高飞船、子弹和外星人的速度
    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)


        