import pygame

class Tile(pygame.sprite.Sprite): #pygame.sprite.Sprite helps you by giving some shortcuts and grouping
    """
    this class is responsible in creating the door for the next level

    Attributes:
        - self.image : load floor image and transform it into size, size which is the tile size
        - self.rect : get rect of the floor and use the pos parameter from Level class for initial position
    Methods:
        - update : using x_shift parameter so that if player move a certain distance the door will move with the level
    """
    def __init__(self,pos,size):
        super().__init__()
        self.image = pygame.image.load('img/Object/tile32.png')
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft = pos)

    def update(self, x_shift):
        self.rect.x += x_shift #this will move the cube in x position