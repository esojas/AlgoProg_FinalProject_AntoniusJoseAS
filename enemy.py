import pygame
from settings import screen_width
from support import import_folder

class Enemy(pygame.sprite.Sprite):
    """
    this class is responsible in creating the enemy which is the trap in this case

    Attributes:
        - self.size : get the tile size to transform the enemy into the tile size
        - self.import_enemy_assets() : to take the image
        - self.frame_index : for the counter to go through the image to create animation
        - self.animation_speed : set animation speed
        - self.image : load enemy image by using a list so that it can create an animation
        - self.rect : get rect of the enemy and use the pos parameter from Level class for initial position
        - self.direction : sets the direction of where the enemy go
    Methods:
        - update : bounces the enemy(trap) back and forth after hitting the boundary and also animates the enemy
        - import_enemy_assets : import the images
        - animate : iterates the frame_index and goes through each image inside the list
    """
    def __init__(self, pos, size):
        super().__init__()
        self.size = size
        self.import_enemy_assets()
        self.frame_index = 0  # will take one of the picture from the keys inside dict
        self.animation_speed = 0.35
        self.image = self.animation[self.frame_index]
        self.rect = self.image.get_rect(midtop=pos)
        self.direction = 5

    def update(self):
        if self.rect.x < -64 or self.rect.x > screen_width:
            self.direction *= -1  # Reverse direction when hitting a boundary because initially its positive then after it goes out of the screen it reverse the direction
        self.rect.x += self.direction   # Move in the direction
        self.animate()
    def import_enemy_assets(self):
        full_path = 'img/Trap/'
        self.animation = import_folder(full_path)
        self.animation = [pygame.transform.scale(img, (self.size, self.size)) for img in self.animation]
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animation):
            self.frame_index = 0
        self.image = self.animation[int(self.frame_index)]
