import pygame
from src.App import App
from src.Config import *

# Config
config = Config()

# Variables
rgb = [0, 128, 128, 255]
index = 0
input_map = config.get(section_keys)
settings = config.get(section_common)

# Pygame Essentials
app = App(settings['width'], settings['height'], fullscreen=settings['fullscreen'])
clock = pygame.time.Clock()
running = True
focused = True
delta = 0.0
main_dir = os.path.split(os.path.abspath(__file__))[0]

# Main Loop
while running:
    # Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.WINDOWFOCUSGAINED:
            focused = True
        if event.type == pygame.WINDOWFOCUSLOST:
            focused = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == input_map['right']:
                index = (index + 1) % 3
            if event.key == input_map['left']:
                index = index-1 if (index - 1 >= 0) else 2
            if event.key == pygame.K_1:
                app.set_window(settings['width'], settings['height'])
            if event.key == pygame.K_2:
                app.set_fullscreen()
            if event.key == pygame.K_F12:
                app.make_screenshot()
    if focused:
        keys = pygame.key.get_pressed()
        if keys[input_map['up']]:
            rgb[index] += 1
        if keys[input_map['down']]:
            rgb[index] -= 1
        
        # Update
        rgb[index] = max(0, min(rgb[index], 255))

        # Render
        app.clear(rgb)
        app.render()
    delta = clock.tick(settings['fps']) / 1000

# Clean Up
app.close()
