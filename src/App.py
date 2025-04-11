import pygame

class App:
    def __init__(self, w, h, caption="Title", flags = 0):
        """Initialize PyGame window"""
        pygame.init()
        self.info = pygame.display.Info()
        self.screen = pygame.display.set_mode([w, h], flags)
        pygame.display.set_caption(caption)

    def set_window(self, w, h):
        """Change Window resolution"""
        self.screen = pygame.display.set_mode([w, h])
    
    def set_fullscreen(self):
        """Set window to full screen"""
        self.screen = pygame.display.set_mode((self.info.current_w, self.info.current_h), flags=pygame.SCALED | pygame.FULLSCREEN)

    def clear(self, color = (0, 0, 0)):
        """Clear the screen to color (default: black)"""
        self.screen.fill(color)

    def draw(self, sprite: pygame.sprite.Sprite, dest = None, area = None):
        """Draw a Sprite to screen"""
        self.screen.blit(source = sprite.image, 
            dest = dest,
            area = area)

    def render(self):
        """Render display surface to screen"""
        pygame.display.flip()
    
    def make_screenshot(self, filename="screenshot.png"):
        """save a screenshot"""
        pygame.image.save(self.screen, filename)

    def close(self):
        """exit the application"""
        pygame.quit()
