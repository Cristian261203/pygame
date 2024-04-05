import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, game_sound
from menu import show_main_menu
from gamePlay.game import start_game


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Space Invaders Clone")
    font = pygame.font.Font(None, 36)
    game_sound.play(loops=-1)
    current_state = 'main_menu'

    while True:        
        if current_state == 'main_menu':
            current_state = show_main_menu(screen, font)
        elif current_state == 'start_game':
            current_state = start_game(screen)
        elif current_state == 'quit':
            pygame.quit()
            sys.exit()
        

        clock.tick(60)

if __name__ == '__main__':
    main()



#/Library/Frameworks/Python.framework/Versions/3.12/bin/python3 -u "/Users/a595/Documents/One piece/python/main.py"