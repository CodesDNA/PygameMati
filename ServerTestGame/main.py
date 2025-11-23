import pygame
from networkClass import Network
from settings import *

pygame.init() # Init pygame

win = pygame.display.set_mode((W, H))
pygame.display.set_caption("Test Game")

class Player:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.move_speed = 3

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

    def update_position(self, x, y):
        self.x = x
        self.y = y

    def update_color(self, color):
        self.color = color

    def move(self):
        # Paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.move_speed
        if keys[pygame.K_RIGHT]:
            self.x += self.move_speed
        if keys[pygame.K_UP]:
            self.y -= self.move_speed
        if keys[pygame.K_DOWN]:
            self.y += self.move_speed

conn = Network("192.168.1.250", 5555) # Network instance
data = conn.resive()  # Receive initial data from server

player1 = Player(data["position"][0], data["position"][1], RectW, RectH, data["color"]) # Player instance

player2 = Player(0, 0, RectW, RectH, BLK) # Player2 instance

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    win.fill(BLK)
    player1.move() # Update player position
    data = conn.send((player1.x, player1.y)) # Initial position send
    player2.update_position(data["position"][0], data["position"][1]) # Update player2 position
    player2.update_color(data["color"]) # Update player2 color
    player1.draw(win) # Draw player
    player2.draw(win) # Draw player2

    pygame.display.flip()

    clock.tick(60) # Frame rate 60 FPS

# Quit Pygame
pygame.quit()