import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *
from blanks import *
import random




class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((screenWidth, screenHeight))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(250,100)
        self.load_data()
        self.player = None

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        map_folder = path.join(game_folder, 'maps')
        self.player_img = body_images.copy()
        self.npc_img = body_images.copy()
        self.map = TiledMap(path.join(map_folder, 'github_game.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.user_group = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.npcs = pg.sprite.Group()
        self.walk_paths = pg.sprite.Group()
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == "player":
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == "wall":
                self.wall = Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == "NPC":
                self.npc = NPC(self, tile_object.x, tile_object.y, tile_object.path_id)
            if tile_object.name == "walk_path":
                self.walk_path = Walk_Path(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, tile_object.path_id)

        self.camera = Camera(self.map.width, self.map.height)

###Game Loop
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()
    #Update
    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw_grid(self):
        for x in range(0, screenWidth, TILESIZE):
            pg.draw.line(self.screen, BLACK, (x,0), (x, screenHeight))
        for y in range(0, screenHeight, TILESIZE):
            pg.draw.line(self.screen, BLACK, (0, y), (screenWidth, y))

    def draw(self):
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
            keys = pg.key.get_pressed()
            if keys[pg.K_c]:
                skin_select(self)


    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
