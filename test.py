import pygame
from src.App import App

# Constants
FPS = 60
WIDTH = 640
HEIGHT = 480

# Pygame Essentials
app = App(WIDTH, HEIGHT)
clock = pygame.time.Clock()
running = True
delta = 0

# Variables
rgb = [0, 128, 128, 255]
index = 0

# Main Loop
while running:
    # Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_a:
                index = (index + 1) % 3
            if event.key == pygame.K_d:
                index = index-1 if (index - 1 >= 0) else 2
            if event.key == pygame.K_1:
                app.set_window(WIDTH, HEIGHT)
            if event.key == pygame.K_2:
                app.set_fullscreen()
            if event.key == pygame.K_F12:
                app.make_screenshot()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        rgb[index] += 1
    if keys[pygame.K_s]:
        rgb[index] -= 1
    
    # Update
    rgb[index] = max(0, min(rgb[index], 255))

    # Render
    app.clear(rgb)
    app.render()

    delta = clock.tick(FPS) / 1000

# Clean Up
app.close()
