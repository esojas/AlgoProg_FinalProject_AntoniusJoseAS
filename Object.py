import pygame
from settings import screen_height

class Breakable_Object(pygame.sprite.Sprite):
    """
    this class is responsible in creating the breakable object

    Attributes:
        - self.image : load breakable_object(crate) image and transform it into size, size which is the tile size
        - self.rect : get rect of the breakable_object and use the pos parameter from Level class for initial position
    Methods:
        - update : using x_shift parameter so that if player move a certain distance the breakable_object will move
        with the level
    """
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.image.load('img/Object/crate.png')
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft=pos)
    def update(self, x_shift):
        self.rect.x += x_shift

class Interactive_Object(pygame.sprite.Sprite):
    """
    this class is responsible in creating the interactive object which is the one player can stand on

    Attributes:
        - self.image : load interactive_object(big rock) image and transform it into 64, 64
        - self.rect : get rect of the interactive_object and use the pos parameter from Level class for initial position
        - self.gravity : sets speed of the interactive_object falling
        - self.falling : is always set to true so that it always falls (because in level class there is collision
        detection that makes the object wont fall out of the screen this is fine)
    Methods:
        - update : using x_shift parameter so that if player move a certain distance the interactive_object will move
        with the level moreover it is used to check if object is put in a place where theres no collision then it will
        fall, lastly it will delete the object if put out of the level
        - draw : draws the the item on the self.rect
    """
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('img/Object/rocks1_6.png')
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(center=pos)
        self.gravity = 4.3
        self.falling = True
    def update(self, x_shift):
        self.rect.x += x_shift
        if self.falling:
            self.rect.y += self.gravity
        if self.rect.y >= screen_height:
            pygame.sprite.Sprite.kill(self)
    def draw(self, screen):
        screen.blit(self.image, self.rect)


