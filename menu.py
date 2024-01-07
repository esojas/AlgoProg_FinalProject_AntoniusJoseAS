import pygame
from sys import exit
from settings import *

class Game_Menu:
    """
    this class is responsible in creating the pause menu and main menu

    Attributes:
        - self.image_bg : load background image
        - self.image_bg : transform background size relative to screen size
        - self.display : takes the screen to display them on screen
        - self.text_font : set the text font and size
        - self.mouse_pos : gets mouse_pos
        - self.mouse_Lclick : gets mouse input
    Methods:
        - main_menu : responsible in creating how the main menu layed out and what happens to each text if its clicked
        - pause_menu : responsible in creating how the pause menu layed out and what happens to each text if its clicked
    """
    def __init__(self,display):
        super().__init__()
        self.image_bg = pygame.image.load("img/Background/Summer2.png").convert_alpha()
        self.image_bg = pygame.transform.scale(self.image_bg, (screen_width, screen_height))
        self.display = display
        self.text_font = pygame.font.SysFont("Arial",30)
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_Lclick = pygame.mouse.get_pressed()

    def main_menu(self):
        play_text = self.text_font.render("New Game", False, "Green")
        play_text_rec = play_text.get_rect(center=(screen_width / 2, screen_height / 3))
        quit_text = self.text_font.render("Quit", False, "Red")
        quit_text_rec = quit_text.get_rect(center=(screen_width / 2, screen_height / 2.45))
        select_text = self.text_font.render("Select Level", False, "Blue")
        select_text_rec = select_text.get_rect(center=(screen_width / 2, screen_height / 2))
        level1 = self.text_font.render("Level 1", False, "Blue")
        level2 = self.text_font.render("Level 2", False, "Blue")
        level3 = self.text_font.render("Level 3", False, "Blue")
        level1_rect = level1.get_rect(center = ((screen_width/3),(screen_height / 3)*1.8))
        level2_rect = level2.get_rect(center = (screen_width/2,(screen_height / 3)*1.8))
        level3_rect = level3.get_rect(center = ((screen_width/1.5),(screen_height / 3)*1.8))
        # displaying the text
        self.display.blit(play_text, play_text_rec)
        self.display.blit(quit_text, quit_text_rec)
        self.display.blit(select_text, select_text_rec)
        self.display.blit(level1, level1_rect)
        self.display.blit(level2, level2_rect)
        self.display.blit(level3, level3_rect)
        # if text are click
        if self.mouse_Lclick[0]:
            if quit_text_rec.collidepoint(self.mouse_pos):
                exit()
            if play_text_rec.collidepoint(self.mouse_pos):
                return 'play'
            if level1_rect.collidepoint(self.mouse_pos):
                return 'level1'
            if level2_rect.collidepoint(self.mouse_pos):
                return 'level2'
            if level3_rect.collidepoint(self.mouse_pos):
                return 'level3'
            else:
                return True
        else:
            return True

    def pause_menu(self):
        play_text = self.text_font.render("Play",False,"Green")
        play_text_rec = play_text.get_rect(center = (screen_width/2,screen_height/3))
        quit_text = self.text_font.render("Quit",False,"Red")
        quit_text_rec = quit_text.get_rect(center=(screen_width / 2, (screen_height / 3)*1.8))
        restart_text = self.text_font.render("Restart", False, "Blue")
        restart_text_rec = restart_text.get_rect(center=(screen_width / 2, screen_height / 2.45))
        main_menu_text = self.text_font.render("Main Menu",False,"Green")
        main_menu_text_rect = main_menu_text.get_rect(center=(screen_width / 2, screen_height / 2))
        # displaying the text
        self.display.blit(play_text, play_text_rec)
        self.display.blit(main_menu_text, main_menu_text_rect)
        self.display.blit(quit_text, quit_text_rec)
        self.display.blit(restart_text, restart_text_rec)
        # if text are click
        if self.mouse_Lclick[0]:
            if quit_text_rec.collidepoint(self.mouse_pos):
                exit()
            if main_menu_text_rect.collidepoint(self.mouse_pos):
                return 'main_menu'
            if play_text_rec.collidepoint(self.mouse_pos):
                return False
            if restart_text_rec.collidepoint(self.mouse_pos):
                return 'restart'
            else:
                return True
        else:
            return True






