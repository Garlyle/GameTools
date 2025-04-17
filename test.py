import pygame
from src.App import App
from src.Config import *
from src.Text import *
from src.Panorama import *

import pygame.freetype
import json

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

# JSON
json_path = os.path.join(main_dir, "resources", "data", "heroes.json")
data_heroes = []
with open(json_path) as f:
    data_heroes = json.load(f)
print(data_heroes)
print(data_heroes[0]["name"])

# Text Rendering
msg = "You've got \\C[#FFFF00]\\V[1] message\\C[#FFFFFF], \\N[0]"
font = pygame.freetype.Font(None, 32)
font.origin = True
font.antialiased = False
text = Text(font, msg, (0,0), instant=False, size=(320, 720))

# Panorama background
pan_file = os.path.join(main_dir, "resources", "water.png")
panorama = Panorama(pan_file, app.screen.size, (-20,-10))

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
                panorama.resize(app.screen.get_size())
            if event.key == pygame.K_2:
                app.set_fullscreen()
                panorama.resize(app.screen.get_size())
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
        panorama.update(delta)
        text.update()

        # Render
        app.clear(rgb)
        app.draw(panorama)
        app.draw(text)

        app.render()
    delta = clock.tick(settings['fps']) / 1000

# Clean Up
app.close()
