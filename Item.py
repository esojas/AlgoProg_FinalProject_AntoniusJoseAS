import pygame


class items(pygame.sprite.Sprite):
    """
    this class is responsible in creating the item(rock)

    Attributes:
        - self.image : load item(rock) image and transform it into the size of 28,25
        - self.rect : get rect of the item and use the pos parameter from Level class for initial position
        - self.gravity : sets speed of the item falling
        - self.falling : use to check if bullet has collide with crate which will make it fall but initially set to
        false so that it wont fall
    Methods:
        - update : using x_shift parameter so that if player move a certain distance the item will move with the level
        moreover it is used to check if bullet has collide with crate which will make it fall
        - draw : draws the the item on the self.rect
        - collision_bullet : check if crate has collide with bullet if so make self.falling True so that item will
        fall out of the crate
    """
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('img/Object/rocks1_4.png')
        self.image = pygame.transform.scale(self.image, (28, 25))
        self.rect = self.image.get_rect(topleft = pos)
        self.gravity = 1.6
        self.falling = False
    def update(self, x_shift):
        self.rect.x += x_shift
        if self.falling: # will only fall after bullet hits the crate
            self.rect.y += self.gravity
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def collision_bullet(self):
        self.falling = True  # propels the item to ground
