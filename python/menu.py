import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, home_image, navy_blue, click_sound

def show_main_menu(screen, font):
    # 加载“play”按钮图片
    play_button_image = pygame.image.load('./res/img/play.png')  # 确保路径正确
    button_width = 200
    button_height = 70
    play_button_image = pygame.transform.scale(play_button_image, (button_width, button_height))
    
    button_position = [(SCREEN_WIDTH - button_width) / 2, (SCREEN_HEIGHT - button_height) / 2]

    # 游戏标题设置
    title_text = "Space Invaders Clone"
    title_font = pygame.font.Font('./res/pdark.ttf', 60)  # 确保路径正确
    
    # 首先创建标题文本表面和矩形
    title_surface = title_font.render(title_text, True, navy_blue)  
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 200))
    
    # 描边颜色和偏移
    stroke_color = (255, 255, 255)  # 白色
    offsets = [(-2, -2), (-2, 2), (2, -2), (2, 2)]  # 描边偏移量
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if button_position[0] <= mouse_x <= button_position[0] + button_width and \
                   button_position[1] <= mouse_y <= button_position[1] + button_height:
                    
                    click_sound.play()
                    return 'start_game'

        screen.blit(home_image, (0, 0))  # 绘制背景图像
        # 绘制描边
        for dx, dy in offsets:
            stroke_surface = title_font.render(title_text, True, stroke_color)
            screen.blit(stroke_surface, (title_rect.x + dx, title_rect.y + dy))
        
        # 绘制原始标题文本
        screen.blit(title_surface, title_rect)
        
        screen.blit(play_button_image, button_position)  # 绘制“play”按钮
        
        pygame.display.flip()
