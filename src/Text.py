import pygame
import re

# Text variables
M_ADV_X = 4
COLOR_TRANS = pygame.Color(0, 80, 0, 128)
shadow = 2


""" Usage example
    font = pygame.freetype.Font(None, 32)
    font.origin = True
    font.antialiased = False
    msg = "You've got \\C[#FFFF00]\\V[1] message\\C[#FFFFFF], \\N[0]"
    text = Text(font, msg, (0,0), instant=False, size=(320, 720))

    text.update()
    app.draw(text)
"""

# Temp
data_vars = [1, 2]
data_heroes = [{'name': 'Bearr'}, {'name': 'NiiQ'}, {'name': 'Garlyle'}]

class Text(pygame.Surface):
    def __init__(self, font, text, position, instant=True, size=None):
        """Initialize a surface for text rendering"""
        self.font = font
        self.letter_idx = 0
        self.word_idx = 0
        self.data_color = {}
        self.color = 'white'
        self.text = self.process_control_characters(text)
        self.words = self.text.split(' ')
        self.metrics = font.get_metrics(self.text)
        self.instant = instant
        # size
        self.rect = font.get_rect(self.text)
        if size is None:
            self.rect.w += shadow
            self.rect.h += shadow
        else:
            self.rect = pygame.Rect(self.rect.topleft, size)
        super().__init__(self.rect.size)
        self.fill(COLOR_TRANS)
        self.set_colorkey(COLOR_TRANS)
        # position
        self.x = self.rect.x
        self.y = self.rect.y
        self.rect.topleft = position

    def re_color(self, m: re.Match):
        """RegEx helper function to change color values"""
        self.data_color[m.start() - len(self.data_color) * 11] = m.group(1)
        return ''

    def process_control_characters(self, text):
        """Scans the text for control characters and replaces then"""
        text = re.sub(r"\\V\[(\d+)\]", lambda m: str(data_vars[int(m.group(1))]), text)
        text = re.sub(r"\\V\[(\d+)\]", lambda m: str(data_vars[int(m.group(1))]), text)
        text = re.sub(r"\\N\[(\d+)\]", lambda m: data_heroes[int(m.group(1))]["name"], text)
        text = re.sub(r"\\C\[(#[A-F0-9]{6})\]", self.re_color, text)
        return text
    
    def update(self):
        """Draw one character each update, or display them instantly"""
        if self.instant:
            while self.letter_idx < len(self.text):
                self.draw_next_letter()
        elif self.letter_idx < len(self.text):
            self.draw_next_letter()
    
    def draw_next_letter(self):
        """Handles drawing of a single letter"""
        letter = self.text[self.letter_idx]
        self.check_color_change()
        self.draw_letter(letter)
        self.advance_letter(letter)

    def check_color_change(self):
        """set text color if color conversion was scanned for position"""
        if self.letter_idx in self.data_color:
            self.color = self.data_color[self.letter_idx]
    
    def draw_letter(self, letter):
        """draw a single letter with shadow"""
        self.font.render_to(self, (self.x + shadow, self.y + shadow), letter, 'black')
        self.font.render_to(self, (self.x, self.y), letter, self.color)

    def advance_letter(self, letter):
        """moves to next letter and check if next word can fit in the same line"""
        self.x += self.metrics[self.letter_idx][M_ADV_X]
        self.letter_idx += 1
        if letter == ' ':
            self.word_idx += 1
            self.word_wrap()

    def word_wrap(self):
        """Moves to the next line if the next word won't fit"""
        bounds = self.font.get_rect(self.words[self.word_idx])
        if self.x + bounds.width > self.rect.width:
            self.new_line()

    def new_line(self):
        """Return x to start, while moves y to next line"""
        self.x, self.y = 0, self.y + self.font.get_sized_height() + 2
