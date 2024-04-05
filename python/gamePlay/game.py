import pygame
import sys
import random
from settings import (SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, background, 
                      menu_image, score, score_font, game_over_image, sprite_rect,menu_image_scaled, click_sound,upgrade_plane)
from entities.game_entities import Bullet, EnemyBullet, create_enemy, enemy_images, Player, PowerUp

# 初始化 Pygame 和字体
pygame.init()
font_size = 36
font = pygame.font.Font(None, font_size)  # 使用默认字体和指定的大小

# 初始化玩家位置和游戏状态变量
player_target_x = SCREEN_WIDTH / 2 - 50  # 屏幕宽度的一半减去50
player_target_y = (SCREEN_HEIGHT / 2) + (SCREEN_HEIGHT / 4) 
game_over = False
enemy_spawn_interval = 2000  # 每2000毫秒生成一个新敌人
last_enemy_spawn_time = pygame.time.get_ticks()

# 暂停游戏函数
def pause_game(screen):
    paused = True
    pause_text = font.render("Game Paused. Click to Continue.", True, pygame.Color('white'))
    pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    clock = pygame.time.Clock()
    
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                paused = False  # 点击任意位置继续游戏

        screen.fill(BLACK)  # 可以选择一个更适合暂停画面的背景色
        screen.blit(pause_text, pause_rect)
        pygame.display.flip()
        clock.tick(60)

# 检查碰撞函数
def check_collisions(player, enemies, bullets, enemy_bullets, screen):
    global game_over, score
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.rect.colliderect(enemy.rect):
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += enemy.score
                break

    for enemy in enemies[:]:
        if player.rect.colliderect(enemy.rect):
            game_over = True
            break

    for bullet in enemy_bullets[:]:
        if bullet.rect.colliderect(player.rect):
            game_over = True
            break

# 游戏结束处理
def handle_game_over(screen):
    screen.blit(game_over_image, (50, 150))
    pygame.display.flip()
    pygame.time.wait(2000)  # 等待2秒后退出

# 显示得分
def display_score(screen, score):
    score_text = score_font.render(f"Score: {score}", True, pygame.Color('white'))
    screen.blit(score_text, (10, 10))

# 玩家移动
def move_towards_target_position(player, target_x, target_y):
    dx = target_x - player.x
    dy = target_y - player.y
    move_x = int(player.speed if dx > 0 else -player.speed)
    move_y = int(player.speed if dy > 0 else -player.speed)

    player.x += move_x if abs(dx) > abs(move_x) else (target_x - player.x)
    player.y += move_y if abs(dy) > abs(move_y) else (target_y - player.y)
    player.rect.x = player.x
    player.rect.y = player.y

# 更新背景位置
def update_background_position(current_position, speed, screen_height):
    new_position = current_position + speed
    return 0 if new_position >= screen_height else new_position

def start_game(screen):
    global game_over, score, last_enemy_spawn_time
    game_over = False
    score = 0  # 重置得分
    player = Player()
    menu_button_pos = (SCREEN_WIDTH - menu_image_scaled.get_width() - 10, 10)  # 使用缩放后的图像宽度

# 确保同时考虑x和y轴的移动
    while player.x < player_target_x or player.y > player_target_y:
        move_towards_target_position(player, player_target_x, player_target_y)
        screen.fill(BLACK)
        screen.blit(background, (0, 0))
        player.draw(screen)
        pygame.display.flip()
        pygame.time.delay(10)

    
    bullets = []  # 玩家的子弹
    enemies = []  # 敌人列表
    enemy_bullets = []  # 敌人子弹
    background_position = 0  # 背景位置
    clock = pygame.time.Clock()
    last_enemy_spawn_time = pygame.time.get_ticks()
    last_powerup_time = pygame.time.get_ticks()
    powerups = []
    # 以下是游戏的主循环代码...


    # 游戏开始，玩家移动到初始位置
    while not game_over:
        current_time = pygame.time.get_ticks()
        screen.fill(BLACK)  # 清空屏幕
        screen.blit(background, (0, background_position))
        screen.blit(background, (0, background_position - SCREEN_HEIGHT))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 检查是否点击了菜单按钮
                mouse_x, mouse_y = event.pos
                if menu_button_pos[0] <= mouse_x <= menu_button_pos[0] + menu_image.get_width() and \
                   menu_button_pos[1] <= mouse_y <= menu_button_pos[1] + menu_image.get_height():
                    click_sound.play()

                    # 暂停游戏
                    pause_game(screen)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # 处理玩家输入
        keys = pygame.key.get_pressed()

        player.update(keys, bullets) # 更新玩家位置

        # 生成敌人逻辑
        if current_time - last_enemy_spawn_time > enemy_spawn_interval:
            create_enemy(enemies, enemy_images)
            last_enemy_spawn_time = current_time

        # 更新游戏元素的位置

        for enemy in enemies:
            enemy.update()
            enemy.shoot(enemy_bullets)
        for bullet in enemy_bullets:
            bullet.update()
            if bullet.y > SCREEN_HEIGHT:  # 如果敌人子弹飞出屏幕下方，从列表中移除
                enemy_bullets.remove(bullet)

        # 更新玩家子弹的位置
        for bullet in bullets[:]:  # 使用列表的副本来避免在遍历过程中修改列表
            bullet.update()
            if bullet.y < 0:  # 如果子弹飞出屏幕顶端，则从列表中移除
                bullets.remove(bullet)

        if current_time - last_powerup_time > 10000:  # 每10秒生成一个道具
            kind = random.choice(['player_upgrade', 'ammo_upgrade'])
            x = random.randint(0, SCREEN_WIDTH - 20)
            y = 0  # 从屏幕顶部开始
            new_powerup = PowerUp(kind, x, y)
            powerups.append(new_powerup)
            last_powerup_time = current_time

        # 更新和绘制所有道具
        for powerup in powerups[:]:
            powerup.update()
            powerup.draw(screen)
            if powerup.y > SCREEN_HEIGHT:  # 如果道具移动到屏幕外，移除它
                powerups.remove(powerup)

        for powerup in powerups[:]:
            if player.rect.colliderect(powerup.rect):
                if powerup.kind == 'player_upgrade':
                    # 假设有一个预定义的新飞机图像变量 new_player_image
                    player.upgrade_plane(upgrade_plane)  # 升级玩家飞机的图像
                elif powerup.kind == 'ammo_upgrade':
                    player.upgrade_bullet()  # 升级玩家的子弹发射模式为三连发
                powerups.remove(powerup)




        # 碰撞检测
        check_collisions(player, enemies, bullets, enemy_bullets, screen)

        # 绘制游戏元素
        player.draw(screen)  # 绘制玩家
        for bullet in bullets:
            bullet.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        for bullet in enemy_bullets:
            bullet.draw(screen)

        # 绘制背景
        background_position = update_background_position(background_position, 1, SCREEN_HEIGHT)
        # 注意：根据您的背景实现方式，这里可能需要调整绘制背景的代码


        # 绘制UI元素（如分数）
        display_score(screen, score)

        screen.blit(menu_image_scaled, menu_button_pos)  # 绘制菜单按钮

        # 检查游戏结束条件
        if game_over:
            handle_game_over(screen)
            break  # 或者可以根据游戏设计返回到主菜单或其他状态

        pygame.display.flip()  # 更新屏幕显示
        clock.tick(60)  # 控制游戏刷新率为60FPS

    # 返回到游戏的下一个状态或结束游戏
    return 'main_menu'  # 或者根据实际需求进行调整
