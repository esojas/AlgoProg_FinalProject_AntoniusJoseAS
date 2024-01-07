import math
import pygame
from settings import screen_width,screen_height
class Gun(pygame.sprite.Sprite):
    """
    this class is responsible for the gun creation such as it having to track the mouse,show,hide gun and give bullet
    initial position

    Attributes:
        - self.player_pos : takes the parameter which is the player position
        - self.display : takes the parameter which is the screen so gun can be drawn
        - self.gun : image of the gun
        - self.angle_degrees : initialize angle_degrees (to store the calculated angle and convert it to degree)
        - self.bullet_speed : sets the bullet speed
    Methods:
        - track_mouse : tracks the position of the mouse by calculating the angle using the mouse_pos and subtracting it
        with the gun.rect x and y position then give the calculated angle to negative because in pygame its the opposite
        - show_gun : display gun on screen with the rotated image and its rect
        - hide_gun : display gun on screen in a position where its not visible to the player
        - create_bullet : gives the position of the x and y position of the gun so that can be use for the bullet class
    """
    def __init__(self,display,player_pos):
        super().__init__()
        self.player_pos = player_pos
        self.display = display
        self.gun = pygame.image.load('img/Gun/Gun.png').convert_alpha()
        self.angle_degrees = 0
        self.bullet_speed = 5

    def track_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        gun_rect = self.gun.get_rect(center=(self.player_pos.rect.center))
        angle = math.atan2(mouse_pos[1] - gun_rect.y, mouse_pos[0] - gun_rect.x)
        self.angle_degrees = math.degrees(angle)
        self.transformed_gun = pygame.transform.rotate(self.gun, -self.angle_degrees)
        self.gun_rect = self.transformed_gun.get_rect(center=gun_rect.center)
        return self.transformed_gun, self.gun_rect

    def show_gun(self):
        self.display.blit(self.transformed_gun, self.gun_rect)

    def hide_gun(self):
        self.display.blit(self.transformed_gun, (1200, 900))

    def create_bullet(self):
        angle = math.radians(self.angle_degrees)
        bullet_x = self.gun_rect.x
        bullet_y = self.gun_rect.y
        return Bullet(bullet_x, bullet_y, angle)  # add to the bullet class

class Bullet(pygame.sprite.Sprite):
    """
    this class is responsible in creating the bullet

    Attributes:
        - self.image : load bullet image
        - self.rect : get rect of the bullet by using the pos_x and pos_y parameter from create_bullet method
        - self.speed : sets speed of the bullet
        - self.angle : use angle from the parameter from create_bullet method
    Methods:
        - update : using x_shift parameter so that if player move a certain distance the bullet will move with the level
    """
    def __init__(self, pos_x, pos_y, angle):
        super().__init__()
        self.image = pygame.image.load('img/Gun/Bullet.png')
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.speed = 5
        self.angle = angle

    def update(self):
        # make bullet path the same
        self.rect.x += self.speed * math.cos(self.angle)
        self.rect.y += self.speed * math.sin(self.angle)
        if self.rect.x >= screen_width or self.rect.x <= 0:  # remove bullet when out of the boundary
            pygame.sprite.Sprite.kill(self)
        elif self.rect.y >= screen_height or self.rect.y <= 0:
            pygame.sprite.Sprite.kill(self)

