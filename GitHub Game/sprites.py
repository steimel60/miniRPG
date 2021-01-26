import pygame as pg
from settings import *




class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect.x = x
        self.rect.y = y


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.user_group
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = game.player_img [0][0]
        self.rect = self.image.get_rect()
        self.stand_index = 0
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.moving = False
        self.hit_box_x = x + TILESIZE
        self.hit_box_y = y + TILESIZE
        self.walk_count = 0



    def move(self):
        if self.walk_count + 1 > 23:
            self.walk_count = 0
        if self.moving and not self.collides():
            if self.target_x > self.x: #rightt
                self.x += WALK_SPEED
                self.walk_count += 1
                self.image = self.game.player_img[3][self.walk_count // 6]
            elif self.target_x < self.x: #left
                self.x -= WALK_SPEED
                self.walk_count += 1
                self.image = self.game.player_img[2] [self.walk_count // 6]
            elif self.target_y > self.y: #down
                self.y += WALK_SPEED
                self.walk_count += 1
                self.image = self.game.player_img[0] [self.walk_count // 6]
            elif self.target_y < self.y: #up
                self.y -= WALK_SPEED
                self.walk_count += 1
                self.image = self.game.player_img[1] [self.walk_count // 6]
        else:
            self.target_x = self.x
            self.target_y = self.y
            self.walk_count = 0
            self.image = self.game.player_img[self.stand_index][self.walk_count]
        if self.target_x == self.x and self.target_y == self.y:
            self.moving = False

    def get_keys(self):
        keys = pg.key.get_pressed()
        if (keys[pg.K_LEFT] or keys[pg.K_a]) and self.moving == False:
            self.target_x -= TILESIZE
            self.stand_index = 2
            self.moving = True

        elif (keys[pg.K_RIGHT] or keys[pg.K_d]) and self.moving == False:
            self.target_x += TILESIZE
            self.stand_index = 3
            self.moving = True

        elif (keys[pg.K_UP] or keys[pg.K_w]) and self.moving == False:
            self.target_y -= TILESIZE
            self.stand_index = 1
            self.moving = True

        elif (keys[pg.K_DOWN] or keys[pg.K_s]) and self.moving == False:
            self.target_y += TILESIZE
            self.stand_index = 0
            self.moving = True


    def collide_with_walls(self):
        for wall in self.game.walls:
            if wall.x <= self.target_x <= (wall.x + wall.w - TILESIZE) and wall.y <= self.target_y + 32 <= (wall.y + wall.h - TILESIZE):
                return True
        return False

    def collide_with_npc(self):
        for npc in self.game.npcs:
            if abs(self.target_x - npc.x) < TILESIZE and abs(self.target_y - npc.y) < TILESIZE:
                return True
        return False

    def collides(self):
        if self.collide_with_npc() or self.collide_with_walls():
            return True
        return False

    def update(self):
        self.get_keys()
        self.collides()
        self.move()
        self.rect.x = self.x
        self.rect.y = self.y



class NPC(pg.sprite.Sprite):
    def __init__(self, game, x, y, path_id):
        self.groups = game.all_sprites, game.npcs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = game.npc_img [0][0]
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.moving = False
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False
        self.walk_count = 0
        self.stand_index = 0
        self.path_id = path_id
        self.initial_collide = False
        self.collide_wait = False
        self.time = pg.time.get_ticks()

    def move(self):
        if self.walk_count + 1 > 23:
            self.walk_count = 0
        if self.moving:
            """
            move by 4 pixles until reaching target x,y
            """
            self.initial_collide = False
            self.collide_wait = True  ## Player has moved since first colliding
            if self.target_x > self.x: #right
                self.x += WALK_SPEED
                self.walk_count += 1
                self.image = self.game.npc_img[3][self.walk_count // 6]
            if self.target_x < self.x: #left
                self.x -= WALK_SPEED
                self.walk_count += 1
                self.image = self.game.npc_img[2] [self.walk_count // 6]
            if self.target_y > self.y: #down
                self.y += WALK_SPEED
                self.walk_count += 1
                self.image = self.game.npc_img[0] [self.walk_count // 6]
            if self.target_y < self.y: #up
                self.y -= WALK_SPEED
                self.walk_count += 1
                self.image = self.game.npc_img[1] [self.walk_count // 6]

        else:
            if self.moving_up:
                self.image = self.game.npc_img[1] [self.walk_count // 6]
            if self.moving_down:
                self.image = self.game.npc_img[0] [self.walk_count // 6]
            if self.moving_left:
                self.image = self.game.npc_img[2] [self.walk_count // 6]
            if self.moving_right:
                self.image = self.game.npc_img[3] [self.walk_count // 6]



    def find_path(self):
        for path in self.game.walk_paths:
            if path.path_id == self.path_id:
                current_path = path

            """
            Check if path is vertical or horizontal, npc is width of tile that's why we compare width and height to tile size
            right now path is either 1 tile wide or tall, then extended in other direction
            """
        if current_path.w > TILESIZE:
            if self.x == current_path.x: #if at left of path move right
                self.target_x = current_path.x + current_path.w
                self.moving_right = True
                self.moving_left = False
            if self.x == current_path.x + current_path.w: #if at right of path move left
                self.target_x = current_path.x
                self.moving_left = True
                self.moving_right = False
        if current_path.h > TILESIZE:
            if self.y == current_path.y: #when at top of path move down
                self.target_y = current_path.y + current_path.h
                self.moving_down = True
                self.moving_up = False
            if self.y == current_path.y + current_path.h: #when at bottom of path move up
                self.target_y = current_path.y
                self.moving_up = True
                self.moving_down = False

        if not self.moving:
            self.moving = True
            if self.moving_up:
                self.target_y = current_path.y
            elif self.moving_down:
                self.target_y = current_path.y + current_path.h
            elif self.moving_left:
                self.target_x = current_path.x
            elif self.moving_right:
                self.target_x = current_path.x + current_path.w
            else:
                self.target_x = current_path.x
                self.target_y = current_path.y

    def collides(self):
        for player in self.game.user_group:
            if player.target_x == self.x and player.target_y == self.y + TILESIZE and self.moving_down:
                self.moving = False
                self.walk_count = 0
                player.stand_index = 1
                self.initial_collide = True
            if player.target_x == self.x and player.target_y == self.y - TILESIZE and self.moving_up:
                self.moving = False
                self.walk_count = 0
                player.stand_index = 0
                self.initial_collide = True
            if player.target_x == self.x - TILESIZE and player.target_y == self.y and self.moving_left:
                self.moving = False
                self.walk_count = 0
                player.stand_index = 3
                self.initial_collide = True
            if player.target_x == self.x + TILESIZE and player.target_y == self.y and self.moving_right:
                self.moving = False
                self.walk_count = 0
                player.stand_index = 2
                self.initial_collide = True

    def update(self):
        self.find_path()
        self.collides()
        self.move()
        self.rect.x = self.x
        self.rect.y = self.y



class Walk_Path(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, path_id):
        self.groups = game.walk_paths
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect.x = x
        self.rect.y = y
        self.path_id = path_id
