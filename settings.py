# the level layout for level 1
level_map = [
'                                       ',
'                                       ',
'                                       ',
'    1                                  ',
'            x        q                 ',
'                                       ',
'              x     xx                 ',
'  s      x         x                   ',
'xxxxxxxxx      xxxx xxxxxxxxxxxxxxxxxxx',]
# the level layout for level 2
level_map_1 = [
'                                   q   ',
'                1                      ',
'                                  xx   ',
'                              1        ',
'                                x      ',
'                e                      ',
'          xx    x                      ',
'  s                                    ',
'xxxxxxxxx            xxxxxxxxxxxxxxxxxx',]
# the level layout for level 3
level_map_2 = [
' q      e                              ',
'                1                      ',
' xx                   1                ',
'  e                           1        ',
'                                x      ',
'                e                      ',
'          xx    x                     q',
'  s                                    ',
'xxxxxxxxx            xxxxxxxx       xxx',]

# we put the screen settings size here to make our live easier
tile_size = 64 #this is our pixel to keep the screen adjust with game
screen_width = 1200
screen_height = tile_size * len(level_map) # this is to set the screen height relative to the level map

