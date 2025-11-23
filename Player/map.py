import pygame, random
from mySprites import *

TILE_SIZE = 48

#0-100
UNB_PROP_DATA = {
    1: {"file": "Assets/Props/UnP_1.png", "scale": 1.6, "col_w": 48, "col_h": 96, "offset": (0, 0), "name": "Bench Side"},              #Bench Side
    2: {"file": "Assets/Props/UnP_2.png", "scale": 1.8, "col_w": 48, "col_h": 48, "offset": (0, 0), "name": "BStone rect Column"},      #Stone rect Column
    3: {"file": "Assets/Props/UnP_3.png", "scale": 2.6, "col_w": 96, "col_h": 48, "offset": (0, -4), "name": "Statue"},                 #Statue
    4: {"file": "Assets/Props/UnP_4.png", "scale": 1.6, "col_w": 96, "col_h": 48, "offset": (3, -10), "name": "Bench Front"},           #Bench Front
    5: {"file": "Assets/Props/UnP_5.png", "scale": 1.5, "col_w": 48, "col_h": 48, "offset": (0, 0), "name": "Stone Ancient Column"},    #Stone Ancient Column
    6: {"file": "Assets/Props/UnP_6.png", "scale": 1.5, "col_w": 48, "col_h": 48, "offset": (0, 0), "name": "Stone Box"},               #Stone Box
    7: {"file": "Assets/Props/UnP_7.png", "scale": 1.0, "col_w": 48, "col_h": 48, "offset": (-30, -24), "name": "tree"},                #Tree
}

#101-200
BR_PROP_DATA = {
    101: {"file": "Assets/Props/BrP_1.png", "scale": 1.5, "col_w": 48, "col_h": 48, "offset": (0, 0), "name": "Wooden Box"},            #Wooden Box
    102: {"file": "Assets/Props/BrP_2.png", "scale": 1.6, "col_w": 48, "col_h": 48, "offset": (3, -5), "name": "Wooden Barrel"},        #Wooden Barrel
}


class Tile(pygame.sprite.Sprite):

    def __init__(self, x, y, group):
        super().__init__()
        
        self.image = load_random_image("tiles/Tiles",TILE_SIZE)
        group.add(self)

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)



class UnbreakableProps(pygame.sprite.Sprite):

    def __init__(self, x, y, prop_type, screen, group=""):
        super().__init__()        
        if prop_type in UNB_PROP_DATA: 
            self.screen = screen           
            self.data = UNB_PROP_DATA[prop_type]

            # --- LOAD & SCALE SPRITE ---
            self.image = pygame.image.load(self.data["file"]).convert_alpha()
            self.image = pygame.transform.scale(
                self.image,
                (int(self.image.get_width() * self.data["scale"]),
                int(self.image.get_height() * self.data["scale"]))
            )

            # --- RENDER RECT (where sprite is drawn) ---
            self.render_rect = self.image.get_rect()
            ox, oy = self.data["offset"]
            self.render_rect.bottomleft = (x + ox, y + TILE_SIZE + oy)

            # --- COLLISION RECT (logic only) ---
            self.collision_rect = pygame.Rect(0, 0, self.data["col_w"], self.data["col_h"])
            self.collision_rect.bottomleft = (x, y + TILE_SIZE)

            # Add to group
            if group != "":
                group.add(self)

    def draw(self):
        self.screen.blit(self.image, self.render_rect)
        # DEBUG
        #pygame.draw.rect(self.screen, (255,0,0), self.collision_rect,2)
        #pygame.draw.rect(self.screen, (0,255,0), self.render_rect, 2)


class BreakableProps(pygame.sprite.Sprite):

    def __init__(self, x, y, prop_type, screen, group=""):
        super().__init__()
        if prop_type in BR_PROP_DATA:
            self.screen = screen

            self.data = BR_PROP_DATA[prop_type]

            # --- LOAD & SCALE SPRITE ---
            self.image = pygame.image.load(self.data["file"]).convert_alpha()
            self.image = pygame.transform.scale(
                self.image,
                (int(self.image.get_width() * self.data["scale"]),
                int(self.image.get_height() * self.data["scale"]))
            )

            # --- RENDER RECT (where sprite is drawn) ---
            self.render_rect = self.image.get_rect()
            ox, oy = self.data["offset"]
            self.render_rect.bottomleft = (x + ox, y + TILE_SIZE + oy)

            # --- COLLISION RECT (logic only) ---
            self.collision_rect = pygame.Rect(0, 0, self.data["col_w"], self.data["col_h"])
            self.collision_rect.bottomleft = (x, y + TILE_SIZE)

            # Add to group
            if group != "":
                group.add(self)

    def draw(self):
        self.screen.blit(self.image, self.render_rect)
        # DEBUG
        pygame.draw.rect(self.screen, (255,0,0), self.collision_rect,2)
        pygame.draw.rect(self.screen, (0,255,0), self.render_rect, 2)


class Map():
    def __init__(self, screen, map_pos_x, map_pos_y, tiles_group, unb_props_group, brk_props_group):

        self.tiles = tiles_group
        self.unb_props = unb_props_group
        self.brk_props = brk_props_group
        self.screen = screen

        self.map_pos_x = map_pos_x
        self.map_pos_y = map_pos_y

        self.map = [
            [2,0,7,0,4,0,8,7,0,2],
            [0,0,0,0,0,0,50,0,0,0],
            [0,0,0,0,6,0,0,0,0,1],
            [0,0,0,6,101,0,0,0,0,5],
            [0,0,0,6,0,0,101,101,0,0],
            [0,0,0,0,3,0,101,0,0,0],
            [5,0,102,0,0,0,6,6,102,0],
            [0,0,0,0,0,0,0,6,102,0],
            [0,0,0,0,0,0,0,0,0,0],
            [2,0,0,0,0,0,0,0,0,2],
        ]

        for i in range(len(self.map)):
            for j in range(len(self.map[i])):

                world_x = self.map_pos_x * TILE_SIZE + j * TILE_SIZE
                world_y = self.map_pos_y * TILE_SIZE + i * TILE_SIZE

                Tile(world_x, world_y, self.tiles)

                if self.map[i][j] != 0:
                    UnbreakableProps(world_x, world_y, self.map[i][j], self.screen, self.unb_props)
                    BreakableProps(world_x, world_y, self.map[i][j], self.screen, self.brk_props)


    def update(self):
        pass



#Ταξινομει τα αντικειμενα με βαση το y στα ποδια τους
class YAwareGroup(pygame.sprite.Group):
    def by_y(self, spr):
        return spr.render_rect.bottom  # sorting based on feet

    def draw(self, surface):
        sprites = sorted(self.sprites(), key=self.by_y)
        for spr in sprites:
            surface.blit(spr.image, spr.render_rect)











#--------------Testing Map script--------------------------
def main():


    display_surface = pygame.display.set_mode((1000,800))



    main_tile_group = pygame.sprite.Group()
    unbreakable_props_group = pygame.sprite.Group()
    breakble = pygame.sprite.Group()




    clock = pygame.time.Clock()
    
    map = Map(display_surface,6,4,main_tile_group,unbreakable_props_group, breakble)
   

    running =True
    while running:
        #Check to see if the user wants to quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #Blit the background
        display_surface.fill((0,0,0))
        map.update()
        #Draw tiles
        main_tile_group.draw(display_surface)

        unbreakable_props_group.update()
        for prop in unbreakable_props_group:
            prop.draw()


        #Update display and tick clock
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()