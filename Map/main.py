import pygame
import random
import os

#!!! Only odd numbers for MAP_TILES to ensure maze generation works properly !!!
MAP_TILES = 19

def load_sprite_sheet(path, spritesheet_file, num_frames = 1, scale_to_height=None, flipped=False):
    """ 
    Load image frames and return image object
    
    Args:
        path (str): Path to the spritesheet directory
        spritesheet_file (str): Filename of the spritesheet
        num_frames (int, optional): Number of frames in the spritesheet. Defaults to 1.
        scale_to_height (int, optional): Height to scale frames to. Defaults to None.
        flipped (bool, optional): Whether to flip frames horizontally. Defaults to False.
        Returns: List of pygame.Surface objects representing the frames
    """


    fullname = os.path.join(path, spritesheet_file)
    try:
        sheet = pygame.image.load(fullname)
        if sheet.get_alpha is None:
            sheet = sheet.convert()
        else:
            sheet = sheet.convert_alpha()
        
        sheet_width = sheet.get_width()
        sheet_height = sheet.get_height()

        frame_width = sheet_width // num_frames
        frame_height = sheet_height

        if num_frames > 1:
            # Extract frames
            frames = []
            for i in range(num_frames):
                frame = sheet.subsurface(
                    pygame.Rect(i * frame_width, 0, frame_width, frame_height)
                )

                # Optional scaling (keep aspect ratio)
                if scale_to_height is not None:
                    scale_factor = scale_to_height / frame_height
                    new_width = int(frame_width * scale_factor)
                    frame = pygame.transform.scale(frame, (new_width, scale_to_height))

                # Optional flipping
                if flipped:
                    frame = pygame.transform.flip(frame, True, False)

                frames.append(frame)

        else:
            # Single frame (no subsurfaces needed)
            frames = sheet

            # Optional scaling (keep aspect ratio)
            if scale_to_height is not None:
                scale_factor = scale_to_height / frame_height
                new_width = int(frame_width * scale_factor)
                frames = pygame.transform.scale(frames, (new_width, scale_to_height))

            # Optional flipping
            if flipped:
                frames = pygame.transform.flip(frames, True, False)

    except FileNotFoundError:
        print(f"Cannot load image: {fullname}")
        raise SystemExit
    
    return frames


class Map:
    """
    class to handle map generation and rendering
    Attributes:
        path (str): Path to the map tiles assets
        map_tiles (int): Number of tiles along one side of the map
    Methods:
        auto_generate_no_obstacles(): Auto-generate a map layout with no obstacles
        draw_map_background(): Draw the map background based on the layout
        generate_maze(): Generate a maze layout using recursive backtracking
        draw(): Print the map layout to the console
    """

    def __init__(self, path, map_tiles):
        # Get screen dimensions
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.map_tiles = map_tiles
        # we want a square map, so we take the smaller dimension
        if self.area.width <= self.area.height:
            self.width = self.area.width
        else:
            self.width = self.area.height
        self.height = self.width
        # Calculate tile dimensions
        self.tile_width = self.width // self.map_tiles
        self.tile_height = self.width // self.map_tiles
        
        self.image_path = path

        self.map_tiles_type ={
            "floor": load_sprite_sheet(path, "floor.png", scale_to_height=self.tile_height),
            "outside_corner": load_sprite_sheet(path, "outside_corner.png", scale_to_height=self.tile_height),
            "horizontal_outside_wall": load_sprite_sheet(path, "horizontal_outside_wall.png", scale_to_height=self.tile_height),
            "vertical_outside_wall": load_sprite_sheet(path, "vertical_outside_wall.png", scale_to_height=self.tile_height),
            "wall_sturdy":  load_sprite_sheet(path, "wall_sturdy.png", scale_to_height=self.tile_height),
            "wall_cracked":  load_sprite_sheet(path, "wall_cracked.png", scale_to_height=self.tile_height),
        }
        self.map_tiles_translation = {
            0: "floor",
            1: "outside_corner",
            2: "horizontal_outside_wall",
            3: "vertical_outside_wall",
            4: "wall_sturdy",
            5: "wall_cracked",
        }

        # Initialize layout
        self.layout = [[0 for i in range(self.map_tiles)] for i in range(self.map_tiles)]
        self.auto_generate_no_obstacles()

        # atributes for rendering
        self.image = self.draw_map_background()
        self.rect = self.image.get_rect()

        # Move to center
        self.rect.center = (self.area.width // 2, self.area.height // 2)
        # Shrink while keeping center the same
        # Negative values shrink and * 2 because inflate takes total amount to change
        self.collision_borders = self.rect.inflate(-(self.tile_width*2), -(self.tile_height*2))  


        # Generate random maze layout
        self.maze = self.generate_maze(self.map_tiles, self.map_tiles)
        # Update layout with maze walls
        # we only want to replace everything but the border
        # !!! SOS !!!   because the maze generation always leaves a border of walls
        #               and in a corner of walls there is always path
        #               the corners will always be empty for players to enter the map
        #               we ALWAYS give odd number of tiles for the map
        #               never even numbers
        for i in range(1, self.map_tiles-1):
            for j in range(1, self.map_tiles-1):
                if self.maze[i][j] != 0:
                    self.layout[i][j] = 4  # wall_sturdy

        # Generate wall sprites
        # we want to have sprites for walls to handle collisions
        # and for future animations (like breaking walls)
        self.sturdy_walls_sprites_group = pygame.sprite.Group()
        self.broken_walls_sprites_group = pygame.sprite.Group()
        self.generate_wall_sprites()

    def auto_generate_no_obstacles(self):
        """
        Auto-generate a map layout with no obstacles
        Creates a border of walls around the map with corners
        0: floor
        1: outside_corner
        2: horizontal_outside_wall
        3: vertical_outside_wall
        """

        for i in range(self.map_tiles):
            for j in (0, self.map_tiles-1):
                self.layout[i][j] = 3
        for i in (0, self.map_tiles-1):
            for j in range(self.map_tiles):
                self.layout[i][j] = 2
        self.layout[0][0] = 1
        self.layout[0][self.map_tiles-1] = 1
        self.layout[self.map_tiles-1][0] = 1
        self.layout[self.map_tiles-1][self.map_tiles-1] = 1

    def draw_map_background(self):
        """
        Draw the map background based on the layout
        Returns:
            pygame.Surface: Surface object representing the map background
            basically a big image made of tiles
        """

        background = pygame.Surface((self.width, self.height))
        background = background.convert()
        for i in range(self.map_tiles):
            for j in range(self.map_tiles):
                tile_type = self.map_tiles_translation[self.layout[i][j]]
                tile_image = self.map_tiles_type[tile_type]
                background.blit(tile_image, (j * self.tile_width, i * self.tile_height))

        return background
    
    def generate_maze(self, grid_width, grid_height):
        """
        Generate a maze layout using recursive backtracking
        Args:
            grid_width (int): Width of the maze grid
            grid_height (int): Height of the maze grid
        Returns:
            list: 2D list representing the maze layout
                0: path
                1: wall
        """

        # visited keeps track of which cells we have already carved paths from.
        visited = [[False]*grid_width for _ in range(grid_height)]
        # maze starts as all walls (1) and we’ll carve out paths (0) as we go.
        maze = [[1]*grid_width for _ in range(grid_height)]  # 1 = wall, 0 = path

        def carve(x, y):
            """
            Carve paths in the maze using recursive backtracking
            Args:
                x (int): Current x position
                y (int): Current y position
            """

            visited[y][x] = True
            maze[y][x] = 0

            # Possible directions: right, left, down, up
            directions = [(1,0), (-1,0), (0,1), (0,-1)]
            # random.shuffle ensures the maze is randomized each time
            random.shuffle(directions)

            #For each direction, it calculates two cells ahead (x + dx*2, y + dy*2)
            # Why two? Because we want walls between paths.
            # if the 2 cells ahead are within bounds and unvisited:
            # then we carve a path to that cell by removing the wall between
            # the current cell and the target cell.
            # else if the target cell is out of bounds or already visited, we skip it.
            # This continues recursively until all reachable cells are visited.
            # basically we always try to go 2 cells in a direction so we leave walls between paths

            for dx, dy in directions:
                nx, ny = x + dx*2, y + dy*2
                if 0 <= nx < grid_width and 0 <= ny < grid_height and not visited[ny][nx]:
                    maze[y + dy][x + dx] = 0
                    carve(nx, ny)

        # Start carving from (1, 1) to always have border outside walls
        carve(1, 1)

        return maze
    
    def generate_wall_sprites(self):
        """
        Generate wall sprites based on the layout
        """

        for i in range(self.map_tiles):
            for j in range(self.map_tiles):
                if self.layout[i][j] == 4:
                    image_sturdy = self.map_tiles_type[self.map_tiles_translation[4]]
                    image_broken = self.map_tiles_type[self.map_tiles_translation[5]]
                    rect = image_sturdy.get_rect()
                    rect.topleft = (self.rect.left + j * self.tile_width,
                                                self.rect.top + i * self.tile_height)
                    self.sturdy_walls_sprites_group.add(Wall(image_sturdy, rect.topleft))
                    self.broken_walls_sprites_group.add(Wall(image_broken, rect.topleft))


    def draw(self):
        """
        Print the map layout to the console
        """

        for i in self.layout:
            print(i)


class Wall(pygame.sprite.Sprite):
    """
    Class to represent a wall sprite
    Attributes:
        image (pygame.Surface): Image of the wall
        rect (pygame.Rect): Rect of the wall
    Methods:
        __init__(self, image, position): Initialize the wall sprite
    """

    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=position)

    def update(self):
        pass
        

if __name__ == "__main__":

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Map Test")
    width, height = screen.get_size()

    map = Map(r"Map\map_tiles_assets", MAP_TILES)
    sturdy_walls = map.sturdy_walls_sprites_group
    broken_walls = map.broken_walls_sprites_group
    screen.fill((0, 0, 0))

    screen.blit(map.image, map.rect)
    # map.draw()
    
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        broken_walls.draw(screen)
        sturdy_walls.draw(screen)

        pygame.display.flip()

    pygame.quit()

