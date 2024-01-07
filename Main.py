import pygame
from sys import exit
from settings import *
from level import Level
from add_bullet import Gun
from menu import Game_Menu

# pygame setup
pygame.init()
pygame.mixer.init()
# sound
game_active_bg = 'Sound/Undertale Enemy approaching.mp3'
gun_sound_effect = pygame.mixer.Sound('Sound/pew_sound_effect.mp3')
pygame.mixer.music.set_volume(0.05)
# game
pygame.display.set_caption("GunScape")
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
background = pygame.image.load("img/Background/Summer2.png").convert_alpha()
background = pygame.transform.scale(background, (screen_width,screen_height))
# level
current_level = 0
level = [Level(level_map, screen), Level(level_map_1, screen), Level(level_map_2, screen)]
toggle = False
bullet_group = pygame.sprite.Group()
# Menu setting
Menu = Game_Menu(screen)
Main_menu = True
Game_pause = False
#cooldown for shooting
last_click_time = 0  # Initialize the last click time
click_cooldown = 250  # Cooldown time in milliseconds

#Game running
while True:
    screen.blit(background, (0, 0))
    #initialize the mouse pos inside loop
    Menu.mouse_pos = pygame.mouse.get_pos()
    Menu.mouse_Lclick = pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        # gun mechanics
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                if not toggle:
                    toggle = True
                else:
                    toggle = False

            # if user wish to pause game
            if event.key == pygame.K_ESCAPE:
                Game_pause = not Game_pause
    # Main menu screen
    if Main_menu == True:
        bullet_group.empty() # deletes the bullet
        gun_ammo = 5 # resets gun ammo
        Main_menu = Menu.main_menu() # calls the main menu class
        pygame.mixer.music.load(game_active_bg)
        pygame.mixer.music.play(-1)
        if Main_menu == "level1" or Main_menu == "play":
            current_level = 0
            level[current_level] = Level(level_map, screen)
        if Main_menu == "level2":
            current_level = 1
            level[current_level] = Level(level_map_1, screen)
        if Main_menu == "level3":
            current_level = 2
            level[current_level] = Level(level_map_2, screen)
        if current_level == 3:
            current_level = 0
    # when game starts
    else:
        # if player dies game pauses and only let player restarts
        if level[current_level].enemy_collision():
            Game_pause = True
        if level[current_level].player_pos.rect.y > screen_height:
            Game_pause = True
        # when player presses esc game pauses
        if Game_pause == True:
            Game_pause = Menu.pause_menu() #calls the pause menu
            if Game_pause == "restart":
                bullet_group.empty()  # deletes the bullet
                gun_ammo = 5 # reset guns ammo
                if current_level == 0:
                    level[current_level] = Level(level_map,screen)
                if current_level == 1:
                    level[current_level] = Level(level_map_1,screen)
                if current_level == 2:
                    level[current_level] = Level(level_map_2,screen)
            if Game_pause == "main_menu":
                Main_menu = True
        # when the game starts and game is not pause
        else:
            # puts the gun on player and track the mouse in current level
            gun = Gun(screen, level[current_level].player_pos)
            gun.track_mouse()
            # runs the level
            level[current_level].run()
            keys = pygame.mouse.get_pressed()
            # toggles to appear the gun on screen
            if toggle == True:
                gun.show_gun()
                if keys[2]:
                    current_time = pygame.time.get_ticks()  # Get the current time
                    if current_time - last_click_time >= click_cooldown:  # Check if enough time has passed
                        last_click_time = current_time
                        gun_sound_effect.play()
                        if gun_ammo > 0:
                            gun_ammo -= 1
                            bullet_group.add(gun.create_bullet())
            else:
                gun.hide_gun()
            #draws the bullet on screen
            bullet_group.update()
            bullet_group.draw(screen)
            #bullet collision with object
            level[current_level].Break_Object(bullet_group)
            #changes level when character enters the door
            if level[current_level].player_exit():
                current_level += 1 # increment the list
                bullet_group.empty()  # deletes the bullet
                gun_ammo = 5  # reset guns ammo
                if current_level == 0:
                    level[current_level] = Level(level_map, screen)
                if current_level == 1:
                    level[current_level] = Level(level_map_1, screen)
                if current_level == 2:
                    level[current_level] = Level(level_map_2, screen)
            if current_level == 3:
                current_level = 0
                Main_menu = True
    pygame.display.update()
    clock.tick(60)

