# ----- SETUP: create a 20x20 map -----

import pygame
 

pygame.init()
pygame.mixer.init()

# Map size
WIDTH = HEIGHT = 20

# Create the 20x20 tile map
game_map = []             
for y in range(HEIGHT):
    row = []
    for x in range(WIDTH):
        row.append(0)      # 0 = empty tile
    game_map.append(row)

# Explosion sound
explosion_sound = pygame.mixer.Sound(
    r"C:\Users\giorg\Documents\GitHub\PygameMati\Sounds\SoundEffects\Bomb.wav"
)

# ----- LOAD PRE-EXPLOSION ANIMATION FRAMES -----
# These will be shown BEFORE the bomb explodes
pre_explosion_frames = [
    pygame.image.load(r"C:\Users\giorg\Documents\GitHub\PygameMati\Images\preExplosion1.png"),
    pygame.image.load(r"C:\Users\giorg\Documents\GitHub\PygameMati\Images\preExplosion2.png"),
    pygame.image.load(r"C:\Users\giorg\Documents\GitHub\PygameMati\Images\preExplosion3.png"),
    pygame.image.load(r"C:\Users\giorg\Documents\GitHub\PygameMati\Images\preExplosion4.png")
]


# ----- BOMB CLASS -----
class Bomb:
    def __init__(self, x, y, reducedTimer, radius, game_map): # x,y = tile coordinates, reducedTimer = seconds to reduce from base time, radius = explosion radius in tiles ( we can add from power ups later )
       
        """
        reducedTimer = how many SECONDS the player reduces from the bomb.
        """

        # ----- TIMER SETTINGS -----
        self.baseExplosionTime = 4.0 # base time before explosion in seconds
        self.timeBeforeExplosion = max(1.5, self.baseExplosionTime - reducedTimer) # dont go below 1.5 sec so the player has time to react
        self.timer = self.timeBeforeExplosion # countdown timer

        # ----- COORDINATES -----
        self.x = x 
        self.y = y 
        self.radius = radius # explosion radius in tiles
        self.game_map = game_map # reference to the game map
        self.exploded = False

        # ----- START THE FIRE/FUSE SOUND HERE -----
        explosion_sound.play()     # ← plays BEFORE the explosion

        # ----- PRE-EXPLOSION ANIMATION SETTINGS -----
        self.animation_frames = pre_explosion_frames # we save the list in the animation frames
        self.current_frame = 0 # current frame index
        self.frame_duration = 1.0 
        self.frame_timer = self.frame_duration
        self.show_animation = True


    def tick(self, dt):
        # Pre-explosion animation
        if not self.exploded and self.show_animation:
            self.frame_timer -= dt

            if self.frame_timer <= 0: # time to switch frame
                self.current_frame += 1 # go to next frame
                self.frame_timer = self.frame_duration # reset timer

              

        # Countdown to explosion
        if not self.exploded:
            self.timer -= dt
            if self.timer <= 0:
                self.explode()


    def explode(self):
        """Runs when the countdown hits zero."""
        self.exploded = True
        self.show_animation = False


        

        self.game_map[self.y][self.x] = 2

        # UP
        for dy in range(1, self.radius + 1):
            ty = self.y - dy
            if 0 <= ty < HEIGHT:
                self.game_map[ty][self.x] = 2

        # DOWN
        for dy in range(1, self.radius + 1):
            ty = self.y + dy
            if 0 <= ty < HEIGHT:
                self.game_map[ty][self.x] = 2

        # LEFT
        for dx in range(1, self.radius + 1):
            tx = self.x - dx
            if 0 <= tx < WIDTH:
                self.game_map[self.y][tx] = 2

        # RIGHT
        for dx in range(1, self.radius + 1):
            tx = self.x + dx
            if 0 <= tx < WIDTH:
                self.game_map[self.y][tx] = 2

    

   

    

# ----- EXAMPLE USAGE WITH deltaTime -----

clock = pygame.time.Clock()

bomb1 = Bomb(x=1, y=5, reducedTimer=0, radius=0, game_map=game_map)   # explodes in 4 sec


for _ in range(300):       # simulate ~5 seconds at 60 FPS
    dt = clock.tick(60) / 1000.0   # deltaTime in seconds

    bomb1.tick(dt)
   

# Print map to show explosions
for row in game_map:
    print(row)
