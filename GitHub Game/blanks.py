import pygame as pg
import numpy as np
from os import path



##Load Folders
game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, 'img')

#####Body Images
walk_down_img = [pg.image.load(path.join(img_folder, 'f1.png')), pg.image.load(path.join(img_folder, 'f2.png')), pg.image.load(path.join(img_folder, 'f3.png')), pg.image.load(path.join(img_folder, 'f4.png'))]
walk_up_img = [pg.image.load(path.join(img_folder, 'b1.png')), pg.image.load(path.join(img_folder, 'b2.png')), pg.image.load(path.join(img_folder, 'b3.png')), pg.image.load(path.join(img_folder, 'b4.png'))]
walk_left_img = [pg.image.load(path.join(img_folder, 'l1.png')), pg.image.load(path.join(img_folder, 'l2.png')), pg.image.load(path.join(img_folder, 'l3.png')), pg.image.load(path.join(img_folder, 'l4.png'))]
walk_right_img = [pg.image.load(path.join(img_folder, 'r1.png')), pg.image.load(path.join(img_folder, 'r2.png')), pg.image.load(path.join(img_folder, 'r3.png')), pg.image.load(path.join(img_folder, 'r4.png'))]

body_images = [walk_down_img, walk_up_img, walk_left_img, walk_right_img]
user_skin_color = (255, 255, 255)

####Hair images



### Skin Select
def skin_select(game):
    menuCount = 0
    game = game
    global user_skin_color
    original_color = user_skin_color
    color_selection = True
    while color_selection:
        pg.time.delay(150)
        pg.event.get()
        keys = pg.key.get_pressed()
        skin_colors = [(245,185,158),(234,154,95),(127,67,41)]

        if keys[pg.K_RIGHT]:
            menuCount += 1
            new_color = skin_colors[menuCount % 3]
            change_color(game.player_img, user_skin_color, new_color)
            user_skin_color = new_color
            game.draw()

        if keys[pg.K_LEFT]:
            menuCount -= 1
            new_color = skin_colors[menuCount % 3]
            change_color(game.player_img, user_skin_color, new_color)
            user_skin_color = new_color
            game.draw()

        if keys[pg.K_RETURN]:
            color_selection = False
        if keys[pg.K_ESCAPE]:
            change_color(game.player_img, user_skin_color, original_color)
            color_selection = False




###Color Change Func

def change_color(img_list, old_color, new_color):
    flat_list = flatten(img_list)
    for img in flat_list:
        img_arr = pg.PixelArray(img)
        img_arr.replace (old_color, new_color)
        del img_arr


## Flatten image lists
def flatten(L):
    if len(L) == 1:
        if isinstance(L[0], list):
            result = flatten(L[0])
        else:
            result = L
    elif isinstance(L[0], list):
        result = flatten(L[0]) +flatten(L[1:])
    else:
        result = [L[0]] + flatten(L[1:])
    return result
