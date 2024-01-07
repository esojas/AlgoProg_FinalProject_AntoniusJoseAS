import pygame

class Door(pygame.sprite.Sprite):
    """
    this class is responsible in creating the door for the next level

    Attributes:
        - self.image : load door image and transform it into size(tilesize), 128
        - self.rect : get rect of the door and use the pos parameter from Level class for initial position
    Methods:
        - update : using x_shift parameter so that if player move a certain distance the door will move with the level
    """
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.image.load('img/Object/door.png')
        self.image = pygame.transform.scale(self.image, (size, 128))
        self.rect = self.image.get_rect(topleft=pos)
    def update(self, x_shift):
        self.rect.x += x_shift