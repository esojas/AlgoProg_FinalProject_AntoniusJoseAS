import pygame
from tiles import Tile
from settings import tile_size, screen_width
from player import player
from Object import Breakable_Object,Interactive_Object
from Item import items
from enemy import Enemy
from next_level import Door

class Level:
    """
    this class is responsible in creating the level and how it works most important class in the code

    Attributes:
        # level setup
        - self.display_surface : takes the screen from main
        - self.setup_level(level_data) : takes the level_data(the level list inside setting) and put it inside
        setup_level attribute
        - self.world_shift : initialize the world_shift to 0
        - self.current_x : to detect that if our x is positive or negative after colliding
        # player_pos
        - self.player_pos : initialize player_pos as an sprite object to be use in Main to track the gun pos
        - self.items_collected : initialize the amount of item collected as 0
        - self.putobject : make into group because there will be more than one object
        - self.last_click_time : initialize the last click time
        - self.click_cooldown : cooldown time in milliseconds
        Methods:
        - setup_level : this is responsible in creating the level. By taking the layout parameter which is the
        level_data from setting then for the stuff to appear on screen they are put in a group except for player
        because there will only be one player. A for loop is used to check the row and colum of the list and they will
        be replace.
        - put_object : responsible for when you left click it will put the object down and added a cooldown so no
        multiple object be put down immediately
        - put_object_onscreen : responsible for drawing object on screen
        - scroll_x : if player move a certain distance in left and right the whole level moves creating the image that
        camera is following where the player moves
        - item_collision : if player collides with the item it will add the amount of items collected by one and make
        the item dissapear giving the image that the player collected the item
        - enemy_collision : if player collides with enemy it returns a boolean that is use in main to pause the game
        - player_exit : if player collides with door it returns a boolean that is use in main to go to the next level
        - horizontal_movement_collision : responsible for all of the horizontal collision inside the level
        - vertical_movement_collision : responsible for all of the vertical collision inside the level
        - Break_Object : responsible if bullet collide with Breakable_object then object(crate) dissapear and so as the
        bullet then the item will drop down
        - run : responsible in running the whole method necessary for the level to work
    """
    def __init__(self,level_data,surface): # this is to pass new levels
        super().__init__()
        #level setup
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0
        self.current_x = 0 # to detect that if our x is positive or negative after colliding
        #player_pos
        self.player_pos = self.player.sprite
        self.items_collected = 0
        self.putobject = pygame.sprite.Group() # so that its called once
        self.last_click_time = 0  # Initialize the last click time
        self.click_cooldown = 1000  # Cooldown time in milliseconds

    def setup_level(self,layout): # we need to draw the level on the screen
        self.tiles = pygame.sprite.Group() # make it group because we are gonna handle more than one
        self.player = pygame.sprite.GroupSingle()# because only one player
        self.block = pygame.sprite.Group() # desctructible object
        self.items = pygame.sprite.Group() # item inside object
        self.enemy = pygame.sprite.Group() # enemy
        self.door = pygame.sprite.Group()

        for row_index,row in enumerate(layout): # this tells us what element consist in the position of list
            for col_index,cell in enumerate(row):
                x = col_index * tile_size  # its multiply by the tile size so if its 1x64 = 64 2x64=128
                y = row_index * tile_size
                if cell == "x": # if we find x inside the matrix change it into a cube
                    tile = Tile((x,y),tile_size)
                    self.tiles.add(tile) # basically where are putting this into the one in run
                if cell == "s":
                    Player = player((x,y))
                    self.player.add(Player)
                if cell == "1":
                    Block = Breakable_Object((x,y),tile_size)
                    Item = items((x,y))
                    self.items.add(Item)
                    self.block.add(Block)
                if cell == "e":
                    enemy = Enemy((x,y),tile_size)
                    self.enemy.add(enemy)
                if cell == "q":
                    exit_lvl = Door((x,y),tile_size)
                    self.door.add(exit_lvl)

    def put_object(self):
        buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if self.items_collected > 0:
            if buttons[0]:  # 0 represents the left mouse button
                current_time = pygame.time.get_ticks()  # Get the current time
                if current_time - self.last_click_time >= self.click_cooldown:  # Check if enough time has passed
                    putobject = Interactive_Object((mouse_pos))
                    self.putobject.add(putobject)
                    self.items_collected -= 1
                    self.last_click_time = current_time  # Update the last click time basically if 2 second has pass in current time it will be minus with 2 also making it zero and resets the timer

    def put_object_onscreen(self):
        self.putobject.draw(self.display_surface)
        self.putobject.update(self.world_shift)

    def scroll_x(self):
        player = self.player.sprite # getting the player
        player_x = player.rect.centerx
        direction_x = player.direction.x
        if player_x < screen_width/4 and direction_x < 0: # this basically means if our player is moving to the left and position of our player is below 300 the world will move
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width/4) and direction_x > 0: # screenwidth/4 makes it responsive or whenever we change the screen width we dont need to change manually
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def item_collision(self):
        player = self.player.sprite
        for Items in self.items.sprites():
            if Items.rect.colliderect(player.rect):
                pygame.sprite.Sprite.kill(Items)
                self.isobjectcollideitem = True
                self.items_collected += 1

    def enemy_collision(self):
        player = self.player.sprite
        for enemy in self.enemy.sprites():
            if enemy.rect.colliderect(player.rect):
                return True
        return False

    def player_exit(self):
        player = self.player.sprite
        for door in self.door.sprites():
            if door.rect.colliderect(player.rect):
                return True
        return False

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed  # we multiply so no need to change manually one by one
        for sprite in self.tiles.sprites(): # takes all of the tiles and put it inside sprite
            if sprite.rect.colliderect(player.rect): # checks collision if there is
                if player.direction.x < 0: # checks if player moving left
                    player.rect.left = sprite.rect.right # what this code does is set the player rect exactly right next to the right (sincce its left) of the object
                    self.current_x = player.rect.left # this will tell us if we are colliding with the wall
                elif player.direction.x > 0: # checks if player moving right
                    player.rect.right = sprite.rect.left
                    self.current_x = player.rect.right # this will tell us if we are colliding with the wall
            for InterObject in self.putobject.sprites():
                if InterObject.rect.colliderect(player.rect):
                    if player.direction.x < 0:
                        player.rect.left = InterObject.rect.right
                        self.current_x = player.rect.left
                    elif player.direction.x > 0:  # checks if player moving right
                        player.rect.right = InterObject.rect.left
                        self.current_x = player.rect.right

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity() # this will keep on incrementing making the player dissapear
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):  # we collide rect instead of sprite collision because we want to have access to each rectangle to the tiles
                if player.direction.y > 0: # player is not jumping
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0 # this statement fix the gravity issue and wont keep on increasing gravity making the player dissapear
                    player.on_ground = True # this alone wont be enough because no matter what even if the character is not jumping or falling it still detect if its on the groun
                elif player.direction.y < 0: # player is jumping
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0 # again fix the gravity issue so that the player wont get stuck as it hit a ceiling
                    player.on_ceiling = True
            for Item in self.items.sprites(): # collision with ground
                if sprite.rect.colliderect(Item.rect):
                    Item.rect.bottom = sprite.rect.top
            #collision with interactable object that falls down
            for InterObject in self.putobject.sprites():
                if sprite.rect.colliderect(InterObject.rect):
                    InterObject.falling = False
                if InterObject.falling == False:
                    if InterObject.rect.colliderect(player.rect):
                        if player.direction.y > 0:
                            player.rect.bottom = InterObject.rect.top
                            player.direction.y = 0  # this statement fix the gravity issue
                            player.on_ground = True  # this alone wont be enough because no matter what even if the character is not jumping or falling it still detect if its on the groun
                        elif player.direction.y < 0:
                            player.rect.top = InterObject.rect.bottom
                            player.direction.y = 0  # again fix the gravity issue so that the player wont get stuck as it hit a ceiling
                            player.on_ceiling = True
                for OtherObject in self.putobject.sprites():
                    if OtherObject != InterObject and InterObject.rect.colliderect(OtherObject.rect):
                        InterObject.falling = False
        # important so there will be no unlimited amount of jump and to fix rect issue of the player
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1: # if player is on the floor and jumping or falling
            player.on_ground = False

    #Object collision with bullet
    def Break_Object(self, Bullet):
        for Object in self.block.sprites():
            for bullet in Bullet.sprites():  # get the rect of bullet
                if Object.rect.colliderect(bullet.rect):
                    pygame.sprite.Sprite.kill(Object)
                    pygame.sprite.Sprite.kill(bullet)
                    for item in self.items.sprites():  # Iterate over all items
                        if Object.rect.colliderect(item.rect):  # Check if item is in the same location as the sprite
                            item.collision_bullet()  # Call collision_bullet on the item

    def run(self):
        #level tiles
        self.tiles.update(self.world_shift) # since self.tiles is one group it will move the entire cube
        self.tiles.draw(self.display_surface)
        self.scroll_x()

        #object and items
        self.block.update(self.world_shift)
        self.items.update(self.world_shift)
        self.items.draw(self.display_surface)
        self.block.draw(self.display_surface)
        self.scroll_x()
        self.Break_Object(pygame.sprite.Group())

        #enemy
        self.enemy.update()
        self.enemy.draw(self.display_surface)
        self.enemy_collision()

        #player
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)

        #player inventory
        self.put_object()
        self.item_collision()
        self.put_object_onscreen()

        #exit door
        self.door.update(self.world_shift)
        self.door.draw(self.display_surface)
