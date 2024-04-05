# settings.py
# 游戏设置和常量
import pygame
# 初始化pygame的mixer模块
pygame.mixer.init()

pygame.font.init()  # 初始化字体模块
# 屏幕尺寸
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900

icon = pygame.image.load('./res/img/icon_game.png')  
pygame.display.set_icon(icon)

# 颜色定义
BLACK = (0, 0, 0)
navy_blue = (0, 0, 128)  # 定义深蓝色


background = pygame.image.load('./res/img/background.jpg')  # 确保这里的路径和文件名与你的图片匹配
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT)) 
background_position = 0


sprite_rect = pygame.image.load('./res/img/plane.png')
upgrade_plane = pygame.image.load('./res/img/10013.png')

normal_bullet = pygame.image.load('./res/img/bulletNormal.png')
enemy_bullet = pygame.image.load('./res/img/enemybullet.png')
sprite_sheet = pygame.image.load("./res/img/menu.png")
props_sheet = pygame.image.load("./res/img/props_sheet.png")


clip_rect = pygame.Rect(150, 142, 55, 59)
ammo_rect = pygame.Rect(326, 142, 46, 43)

upgrade_image = props_sheet.subsurface(clip_rect)
upgrade_ammo = props_sheet.subsurface(ammo_rect)




score_font = pygame.font.SysFont("Arial", 36)  # 创建一个字体对象
score = 0  # 初始化玩家的分数

home_image = pygame.image.load('./res/img/home_img.jpeg')  # 加载游戏结束图片
home_image = pygame.transform.scale(home_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # 调整图像大小

game_over = False  # 在游戏主循环开始之前添加这个标志

game_over_image = pygame.image.load('./res/img/gameover.png')  # 加载游戏结束图片
game_over_image = pygame.transform.scale(game_over_image, (800, 500))

# 从素材图中裁剪出按钮图片
button_menu = pygame.Rect(787, 762, 336, 148)  # 确保这些值对应于你的 sprite sheet 中的正确位置和大小
menu_image = sprite_sheet.subsurface(button_menu)

# 从素材图中裁剪出按钮图片
button_menu = pygame.Rect(787, 762, 336, 148)  # 原始尺寸
menu_image = sprite_sheet.subsurface(button_menu)

# 调整图像的大小
button_menu_size = (180, 80)  # 新尺寸
menu_image_scaled = pygame.transform.scale(menu_image, button_menu_size)



# 音效
shoot_sound = pygame.mixer.Sound("./res/sound/shoot.mp3")
game_sound = pygame.mixer.Sound("./res/sound/game.mp3")
click_sound = pygame.mixer.Sound("./res/sound/button.mp3")



class MenuButton:
    def __init__(self, x, y, image, function=None):
        self.image = image  # 直接使用传入的 Surface 对象
        self.rect = self.image.get_rect(topleft=(x, y))
        self.function = function

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def check_click(self, position):
        if self.rect.collidepoint(position):
            if self.function:
                self.function()
            return True
        return False
    
def your_menu_function():
    print("Menu button clicked!")

menu_button = MenuButton(32, 24, menu_image_scaled, function=your_menu_function)
