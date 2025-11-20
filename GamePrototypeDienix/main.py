import os
import pygame


def load_sprite_sheet(path, spritesheet_file, num_frames, scale_to_height=None, flipped=False):
    """ 
    Load image frames and return image object
    
    Args:
        path (str): Path to the spritesheet directory
        spritesheet_file (str): Filename of the spritesheet
        num_frames (int): Number of frames in the spritesheet
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

    except FileNotFoundError:
        print(f"Cannot load image: {fullname}")
        raise SystemExit
    
    return frames

class Reaper(pygame.sprite.Sprite):
    """
    Reaper character class with movement and animation
    1. Movement with arrow keys
    2. Animation states: idle and running
    3. Direction facing: left and right
    4. Animation speed control

    Args:
        path (str): Path to the spritesheet directory   
        fps (int, optional): Animation frames per second. Defaults to 10.
    Returns: pygame.sprite.Sprite object
    """

    def __init__(self, path, fps=10):
        pygame.sprite.Sprite.__init__(self)
        """
        We use Sprite class from pygame to manage our character
        we do that in  order to be able to use the inherited Sprite methods
        to manage all our game sprites in a group

        Mandatory arguments:
            self.image : pygame.Surface object representing the current frame
            self.rect : pygame.Rect object representing the position and size of the sprite
        Mandatory methods:
            update(args) : method to update the sprite's state each frame

        then we add the sprite to a pygame.sprite.Group() to manage it easily
        1. we can call all_sprites.update(args) to update all sprites in the group
            passed args will be forwarded to each sprite's update method
        2. we can call all_sprites.draw(screen) to draw all sprites in the group
        """
        self.spritesheet_list_path = path
        # Load spritesheets for different states and directions using the helper function
        # to a dictionary for easy access
        self.spritesheets_dict = {
            "right":
                {
                    "idle": load_sprite_sheet(self.spritesheet_list_path, "idle.png", 18, scale_to_height=100),
                    "running": load_sprite_sheet(self.spritesheet_list_path, "running.png", 12, scale_to_height=100)
                },
            "left":
                {
                    "idle": load_sprite_sheet(self.spritesheet_list_path, "idle.png", 18, scale_to_height=100, flipped=True),
                    "running": load_sprite_sheet(self.spritesheet_list_path, "running.png", 12, scale_to_height=100, flipped=True)
                },
        }

        self.current_frame = 0
        self.face_direction = "right"
        self.state = "idle"
        self.image = self.spritesheets_dict[self.face_direction][self.state][self.current_frame]
        self.rect = self.image.get_rect()

        # Set initial position to center of the screen
        # So we need to get the screen size to check for collisions with screen borders
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
    
        # we want pixels per second, and will use dt to scale movement
        self.speed =  200 

        # Animation speed in frames per second
        self.fps = fps
        self.time_per_frame = 1 / fps  # seconds per frame
        self.dt_accumulator = 0     # store elapsed time
                                    # to manage frame updates


    def update(self, dt, keys):
        """
        the update method to be called each frame to update the sprite state
        Args:
            dt (float): Delta time in seconds since last frame
                The dt basicaly is the elapsed time since last frame
                faster will run the loop more times per second than slower computers
                so we use dt to scale movement and animation speed

                For example about movement, if we want to move 200 pixels per second
                a pc that runs at 60 fps will have dt = 1/60 = 0.0167 seconds
                so each frame we move 200 * 0.0167 = 3.33
                while a pc that runs at 30 fps will have dt = 1/30 = 0.0333 seconds
                so each frame we move 200 * 0.0333 = 6.66

                So every second both pcs will move 200 pixels

                For animation speed, we want to change frames every fixed time interval
                so we accumulate dt each frame and when it exceeds a fixed time per frame e.g 1 second
                we change the frame and reset the accumulator

                So for the above example the first pc will change frames every 60 frames
                while the second pc will change frames every 30 frames
                both will change frames every second
                
            keys (list): List of pressed keys from pygame.key.get_pressed()
        """

        # we use this to store movement in x and y direction
        movepos = [0, 0]
        # Flag to check if the character is moving (for idle/running state)
        moving = False
        
        if keys[pygame.K_LEFT]:
            movepos[0] = movepos[0] - self.speed * dt
            self.face_direction = "left"
            if self.state != "running":
                self.state = "running"
                self.current_frame = 0
            moving = True
        if keys[pygame.K_RIGHT]:
            movepos[0] = movepos[0] + self.speed * dt
            self.face_direction = "right"
            if self.state != "running":
                self.state = "running"
                self.current_frame = 0
            moving = True
        if keys[pygame.K_UP]:
            movepos[1] = movepos[1] - self.speed * dt
            if self.state != "running":
                self.state = "running"
                self.current_frame = 0
            moving = True
        if keys[pygame.K_DOWN]:
            movepos[1] = movepos[1] + self.speed * dt
            if self.state != "running":
                self.state = "running"
                self.current_frame = 0
            moving = True

        if not moving:
            if self.state != "idle":
                self.state = "idle"
                self.current_frame = 0

        # Update position with collision detection against screen borders
        # we create a new rect with the proposed new position
        newpos = self.rect.move(movepos)
        # check if the new position is within the screen area
        if self.area.contains(newpos):
            # if yes, update the rect position
            # else we ignore the movement
            self.rect = newpos

        # Update animation frame
        self.dt_accumulator += dt
        if self.dt_accumulator >= self.time_per_frame:
            self.dt_accumulator = 0
            self.current_frame += 1
            frames = self.spritesheets_dict[self.face_direction][self.state]
            if self.current_frame >= len(frames):
                self.current_frame = 0
            self.image = frames[self.current_frame]
        


def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Dienix Game Prototype")

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    # Initialise players
    sprite_seet_path = r"GamePrototypeDienix\spritesheets"
    player1 = Reaper(sprite_seet_path, fps=20)

    # Initialise sprites
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player1)

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Initialise clock
    clock = pygame.time.Clock()

    # Game loop
    running = True
    while running:
        dt_ms = clock.tick(60)  # cap at 60 FPS
        dt = dt_ms / 1000       # dt in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(background, (0, 0))

        keys = pygame.key.get_pressed()
        
        all_sprites.update(dt, keys)
        all_sprites.draw(screen)

        pygame.display.flip()

    pygame.quit()
    

if __name__ == "__main__":
    main()