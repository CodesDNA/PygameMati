# ----- SETUP: create a 20x20 map -----

import pygame
from Map_test import *

pygame.init()
pygame.mixer.init()

# ----- WINDOW -----
draw_width = 400
draw_height = 400
screen = pygame.display.set_mode((draw_width, draw_height))



explosion_fire_image = pygame.image.load(
    r"Images\ExplosionFire.png"
)




# Explosion sound
explosion_sound = pygame.mixer.Sound(
    r"Sounds\SoundEffects\Bomb.wav"
)

# ----- LOAD PRE-EXPLOSION ANIMATION FRAMES -----
# These will be shown BEFORE the bomb explodes
pre_explosion_frames = [
    pygame.image.load(r"Images\preExplosion1.png"),
    pygame.image.load(r"Images\preExplosion2.png"),
    pygame.image.load(r"Images\preExplosion3.png"),
    pygame.image.load(r"Images\preExplosion4.png")
]




# ----- BOMB CLASS -----
class Bomb:
    def __init__(self, currentPos , x, y, reducedTimer, radius): # x,y = tile coordinates, reducedTimer = seconds to reduce from base time, radius = explosion radius in tiles ( we can add from power ups later )
       
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
     
        self.exploded = False 

        # ----- START THE FIRE/FUSE SOUND HERE -----
        explosion_sound.play()     # ← plays BEFORE the explosion

        # ----- PRE-EXPLOSION ANIMATION SETTINGS -----
        self.animation_frames = pre_explosion_frames # we save the list in the animation frames
        self.current_frame = 0 # current frame index
        self.frame_duration = 1.0 
        self.frame_timer = self.frame_duration
        self.show_animation = True

         # after explision image
        self.explosion_image = explosion_fire_image
        self.show_explosion_fire = False  # initially hidden


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

        # Mark explosion on the map
        # CENTER

        self.show_explosion_fire = True


        # explosion path

        for direction in [(1,0), (-1,0), (0,1), (0,-1)]: # right, left, down, up
            for step in range(1, self.radius + 1):
                new_x = self.x + direction[0] * step
                new_y = self.y + direction[1] * step
                # Here we would mark the explosion on the map
                # For this example, we just print the coordinates
                print(f"Explosion at ({new_x}, {new_y})")



   

    

# -----  USAGE WITH deltaTime -----

clock = pygame.time.Clock()

bomb1 = Bomb(currentPos=0, x=1, y=5, reducedTimer=0, radius=0)   # explodes in 4 sec







# ----- GAME LOOP -----
run = True
while run:
    dt = clock.tick(60) / 1000.0  # delta time in seconds

    # ----- HANDLE EVENTS -----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # ----- UPDATE BOMB -----
    bomb1.tick(dt)

    # ----- DRAW -----
    screen.fill((255, 255, 255))  # white background

    # draw pre-explosion animation
    if bomb1.show_animation:
        frame_image = bomb1.animation_frames[bomb1.current_frame]
        frame_image = pygame.transform.scale(frame_image, (draw_width, draw_height))
        screen.blit(frame_image, (0, 0))

    # draw explosion fire AFTER explosion
    if bomb1.exploded and bomb1.show_explosion_fire:
        fire_image = pygame.transform.scale(bomb1.explosion_image, (draw_width, draw_height))
        screen.blit(fire_image, (0, 0))

    pygame.display.flip()  # update screen


pygame.quit()




