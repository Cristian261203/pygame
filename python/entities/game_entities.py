import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, sprite_rect,normal_bullet,shoot_sound, enemy_bullet, upgrade_image,upgrade_ammo
import random

enemy_images = [
    pygame.image.load('./res/img/10024.png'),  # 敌人A的图像
    pygame.image.load('./res/img/10025.png'),  # 敌人B的图像
    pygame.image.load('./res/img/10026.png'),  # 敌人C的图像
]
# 在函数外部定义enemy_scores
enemy_scores = [1, 3, 5]

def create_enemy(enemies, enemy_images):
    idx = random.randint(0, len(enemy_images) - 1)  # 随机选择敌人图像
    new_enemy = Enemy(enemy_scores[idx], enemy_images[idx])
    enemies.append(new_enemy)

    

class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH / 2 - 50  # 屏幕宽度的一半减去50
        self.y = SCREEN_HEIGHT  # 玩家的起始位置在屏幕底部之外
        self.bullet_type = 'single'  # 新增：追踪当前子弹类型，默认为'single'
        self.speed = 3
        self.width = 100
        self.height = 100
        self.image = sprite_rect
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.shoot_cooldown = 500  # 子弹发射冷却时间，单位毫秒
        self.last_shoot_time = 0  # 上次发射子弹的时间

    def draw(self, screen):
        screen.blit(self.image, self.rect)  # 使用self.rect来定位
    
    def update(self, keys, bullets):
        # 临时变量，用于存储可能的浮点数位置
        temp_x = self.x
        temp_y = self.y
        current_time = pygame.time.get_ticks()  # 获取当前时间

        if keys[pygame.K_w]: temp_y -= self.speed
        if keys[pygame.K_s]: temp_y += self.speed
        if keys[pygame.K_a]: temp_x -= self.speed
        if keys[pygame.K_d]: temp_x += self.speed

        # 限制玩家移动范围，并确保值是整数
        self.x = max(0, min(SCREEN_WIDTH - self.width, int(temp_x)))
        self.y = max(0, min(SCREEN_HEIGHT - self.height, int(temp_y)))

        # 更新rect位置以反映新的x和y坐标
        self.rect.x = self.x
        self.rect.y = self.y

        # 如果按下空格键并且自上次射击以来已经过了足够的冷却时间，则创建并发射子弹
        if keys[pygame.K_SPACE] and current_time - self.last_shoot_time > self.shoot_cooldown:
    # 定义子弹向左偏移的距离
            offset = 32  # 子弹向左偏移的像素数

            # 基于当前的bullet_type发射不同模式的子弹
            if self.bullet_type == 'single':
                # 发射单颗子弹，向左偏移
                bullets.append(Bullet(self.rect.centerx - offset, self.rect.top))
            elif self.bullet_type == 'triple':
                # 发射三颗子弹，每颗子弹都向左偏移
                bullets.append(Bullet(self.rect.centerx - offset, self.rect.top))  # 中心，向左偏移
                bullets.append(Bullet(self.rect.left - offset, self.rect.centery))  # 左侧，向左偏移
                bullets.append(Bullet(self.rect.right - offset, self.rect.centery))  # 右侧，向左偏移
            self.last_shoot_time = current_time  # 更新上次发射子弹的时间
            shoot_sound.play()

    def upgrade_plane(self, upgrade_plane):
        """升级玩家飞机的图像"""
        self.image = upgrade_plane
        self.rect = self.image.get_rect(center=self.rect.center)  # 更新rect以保持位置

    def upgrade_bullet(self):
        """升级子弹类型为三连发"""
        self.bullet_type = 'triple'

class Enemy:
    def __init__(self, score, image):
        self.x = random.randint(0, 750)
        self.y = random.randint(-150, -50)
        self.score = score
        self.image = image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.shoot_interval = 1000  # 射击间隔，单位毫秒
        self.last_shot = pygame.time.get_ticks()
        self.speed = 2  # 假设敌人下落的速度

    def update(self):
        """更新敌人位置"""
        self.y += self.speed  # 向下移动
        self.rect.y = self.y  # 更新rect位置以保持与self.y一致

    def shoot(self, enemy_bullets):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_interval:
            bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
            enemy_bullets.append(bullet)
            self.last_shot = now

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 10
        # 加载子弹图片
        self.image = normal_bullet
        # 获取图片的大小，用于绘制和碰撞检测
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, screen):
        # 使用图片绘制子弹，而不是绘制矩形
        screen.blit(self.image, self.rect)

    def update(self):
        """更新子弹的位置并检测与敌人的碰撞"""
        self.y -= self.speed
        self.rect.y = self.y
        print(f"子弹位置更新为: {self.y}")  # 打印子弹的y坐标来调试

        

class EnemyBullet:
    def __init__(self, x, y, speed=3):
        self.x = x
        self.y = y
        self.speed = speed
        self.image = enemy_bullet
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self):
        """向下移动子弹"""
        self.y += self.speed
        self.rect.y = self.y

    def draw(self, screen):
        screen.blit(self.image, self.rect)

enemies = [
    Enemy(enemy_scores[0], enemy_images[0]),  # 敌人A，分数为1
    Enemy(enemy_scores[1], enemy_images[1]),  # 敌人B，分数为3
    Enemy(enemy_scores[2], enemy_images[2]),  # 敌人C，分数为5
]

class PowerUp:
    def __init__(self, kind, x, y, speed=2):
        self.kind = kind  # 'player_upgrade' 或 'ammo_upgrade'
        self.x = x
        self.y = y
        self.speed = speed
        # 根据道具类型选择图像
        if self.kind == 'player_upgrade':
            self.image = upgrade_image
        else:  # 'ammo_upgrade'
            self.image = upgrade_ammo
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self):
        """更新道具位置"""
        self.y += self.speed
        self.rect.y = self.y

    def draw(self, screen):
        # 绘制道具图像
        screen.blit(self.image, self.rect)

