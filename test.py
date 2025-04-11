import pygame
from src.App import App

app = App(640, 480)
clock = pygame.time.Clock()
running = True
delta = 0
rgb = [0, 128, 128, 255]
index = 0

while running:
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
                app.set_window(640, 480)
            if event.key == pygame.K_2:
                app.set_fullscreen()
            if event.key == pygame.K_F12:
                app.make_screenshot()

    # fill the screen with a color to wipe away anything from last frame
    app.clear(rgb)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        rgb[index] += 1
    if keys[pygame.K_s]:
        rgb[index] -= 1
    
    rgb[index] = max(0, min(rgb[index], 255))

    app.render()
    delta = clock.tick(60) / 1000

app.close()
