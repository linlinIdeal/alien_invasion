import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien

# 外星人撞击飞船或者到达底端
def ship_hit(ship, aliens, bullets, stats, sb):
    if stats.ships_left > 0:
        # 剩余飞船数减一
        stats.ships_left -= 1
        # 更新记分牌
        sb.prep_ships()

        # 清空外星人和子弹
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人
        create_fleet(ship, aliens)
        # 把飞船放到屏幕底部中央
        ship.center_ship()

        # 暂停0.5s
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
        

# 外星人到达屏幕底端
def check_aliens_bottom(ship, aliens, bullets, stats, sb):
    screen_rect = ship.screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ship, aliens, bullets, stats, sb)
            break

# 发射子弹
def fire_bullet(ship, bullets):
    # 判断是否超出子弹个数限制，如果没有超出则创建新的子弹
    if len(bullets) < ship.ai_settings.bullet_allowed:
        new_bullet = Bullet(ship)
        bullets.add(new_bullet)

# 按下键盘事件
def check_keydown_events(event, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ship, bullets)

# 松开键盘事件
def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    
# 鼠标和键盘事件的监测
def check_events(ship, aliens, bullets, play_button, sb, stats):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ship, aliens, bullets,stats, play_button,sb, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

# 检查Play按钮事件
def check_play_button(ship, aliens, bullets, stats, play_button, sb, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True

        # 清空外星人和子弹
        aliens.empty()
        bullets.empty()

        # 创建外星人，并设置飞船居中
        create_fleet(ship, aliens)
        ship.center_ship()

        # 重置记分牌、最高分和等级图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

# 更新背景
def update_screen(ship, bullets, aliens, stats, sb, play_button):
    # 用背景颜色填充屏幕 set screen background color
    ship.screen.fill(ship.ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    # 绘制飞船
    ship.blitme()
    # 绘制外星人
    aliens.draw(ship.screen)
    # 显示计分
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    # 让最近绘制的屏幕可见 make the most recently drawn screen visible
    pygame.display.flip()
def check_bullet_alien_collisions(ship, bullets, aliens, stats, sb):
    # 检查是否有子弹击中了外星人，如果有就删除子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    # 更新得分并更新记分牌
    if collisions:
        for aliens in collisions.values():
            stats.score += sb.ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    # 外星人全部被消灭后就创建新的舰队
    if len(aliens) == 0:
        bullets.empty()
        # 加快游戏速度
        ship.ai_settings.increase_speed()
        # 提高等级
        stats.level += 1
        sb.prep_level()
        create_fleet(ship, aliens)

# 更新子弹
def update_bullets(ship, bullets, aliens, stats, sb):
    bullets.update()
    # 删除已消失的子弹
    # we use copy here. Think why
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ship, bullets, aliens, stats, sb)

# 获取每行外星人个数
def get_number_alien_x(ai_settings, screen):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    available_space_x = ai_settings.screen_width - 2*alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

# 获取外星人每列个数
def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height - 3 * alien_height - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

# 创建外星人
def greate_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

# 创建外星人舰队
def create_fleet(ship, aliens):
    alien = Alien(ship.ai_settings, ship.screen)
    number_aliens_x = get_number_alien_x(ship.ai_settings, ship.screen)
    number_rows = get_number_rows(ship.ai_settings, ship.rect.height, alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            greate_alien(ship.ai_settings, ship.screen, aliens, alien_number, row_number)

# 检查是否有外星人碰触到了边缘
def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        # 判断是否有外星人触碰到边缘
        if alien.check_edges():
            # 改变左右移动方向
            change_fleet_direction(ai_settings, aliens)
            break

# 修改外星人舰队左右移动方向
def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

# 更新外星人舰队
def update_aliens(ship, aliens, bullets, stats, sb):
    check_fleet_edges(ship.ai_settings, aliens)
    aliens.update()
    # 监测外星人有没有和飞船碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ship, aliens, bullets, stats, sb)
    check_aliens_bottom(ship, aliens, bullets, stats, sb)

# 检查最高分
def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

