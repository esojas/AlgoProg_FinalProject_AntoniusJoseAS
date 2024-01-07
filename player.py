import pygame
from support import import_folder


class player(pygame.sprite.Sprite):
    """
    this class is responsible in creating the player

    Attributes:
        - self.import_character_assets() : to take the image
        - self.frame_index : for the counter to go through the image to create animation
        - self.animation_speed : set animation speed
        - self.image : load player image by using a dict and list so that it can create an animation
        - self.rect : get rect of the player and use the pos parameter from Level class for initial position
        # player movement
        - self.direction : use vector2 which is a list that contains x,y
        - self.speed : set the movement speed
        - self.gravity : set gravity
        - self.jump_speed : set the jump speed
        # player status
        - self.player_status : use to see the player status and is initially set to idle
        - self.face_right : seeing if player look left or right
        - self.on_ground : use to check if player is on ground
    Methods:
        - import_enemy_assets : import the images of player and by using dictionary so that we can use different state
        of animation depending on the input
        - animate : iterates the frame_index and goes through each image inside the list and flipped the image if
        facing left or right
        - get_input : gets the keyboard input for player movement
        - getstatus : gets the player status for correct animation displayed
        - apply_gravity : apply gravity on the player
        - jump : make the player jump and give sound effect of jump
        - update : updates the player state by taking all other methods
    """
    def __init__(self, pos):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0 # will take one of the picture from the keys inside dict
        self.animation_speed = 0.15
        self.image = self.animation['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        # player movement
        self.direction = pygame.math.Vector2(0,0) # we use vector2 is a list that contains x,y
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16
        # player status
        self.player_status = 'idle'
        self.face_right = True
        self.on_ground = False

    def import_character_assets(self):
        character_path = 'img/Player/'
        self.animation = {'idle':[],'run':[],'jump':[],'fall':[]} # these dicts keys name have to be the same

        for animation in self.animation.keys():
            full_path = character_path + animation # this loop access the key and attach it at the end of character path
            self.animation[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animation[self.player_status]
        #loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation): # this basically checks if the counter is more than the list
            self.frame_index = 0 # we reset the counter back to zero
        image = animation[int(self.frame_index)]
        if self.face_right: # makes the image flip
            self.image = image
        else:
            flipped_img = pygame.transform.flip(image,True,False)
            self.image = flipped_img

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.direction.x = 1
            self.face_right = True
            if keys[pygame.K_SPACE] and self.on_ground:
                self.jump()
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.face_right = False
            if keys[pygame.K_SPACE] and self.on_ground:
                self.jump()
        elif keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
        else:
            self.direction.x = 0

    def getstatus(self):
        #jumping
        if self.direction.y < 0:
            self.player_status = 'jump'
        #fall
        elif self.direction.y > 1: #make it bigger than gravity because our program keep cycling trhough gravity and 0 from the level setting
            self.player_status = 'fall'
        else: # because of that cycle the animation keep cycling through idle and fall even when not jump or falling
            if self.direction.x == 0:
                self.player_status = 'idle'
            else:
                self.player_status = 'run'

    def apply_gravity(self):
        self.direction.y += self.gravity # propels the player to ground
        self.rect.y += self.direction.y # using the rectangle player ensures a smooth vertical movement

    def jump(self):
        gun_sound_effect = pygame.mixer.Sound('Sound/boing_sound_effect.mp3')
        gun_sound_effect.play()
        self.direction.y = self.jump_speed

    def update(self):
        self.get_input()
        self.getstatus()
        self.animate()

