import pygame
import re

# Text variables
M_ADV_X = 4
COLOR_TRANS = pygame.Color(0, 80, 0, 128)
shadow = 2

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
        self.text_surf_rect = font.get_rect(self.text)
        if size is None:
            self.text_surf_rect.w += shadow
            self.text_surf_rect.h += shadow
        else:
            self.text_surf_rect.w = size[0]
            self.text_surf_rect.h = size[1]
        super().__init__(self.text_surf_rect.size)
        self.fill(COLOR_TRANS)
        self.set_colorkey(COLOR_TRANS)
        # position
        self.x = self.text_surf_rect.x
        self.y = self.text_surf_rect.y
        self.text_surf_rect.topleft = position

    def re_color(self, m: re.Match):
        """RegEx helper function to change color values"""
        self.data_color[m.start() - len(self.data_color) * 11] = m.group(1)
        return ''

    def process_control_characters(self, text):
        """Scans the text for control characters and replaces then"""
        text = re.sub(r"\\V\[(\d+)\]", lambda m: str(data_vars[int(m.group(1))]), text)
        text = re.sub(r"\\V\[(\d+)\]", lambda m: str(data_vars[int(m.group(1))]), text)
        text = re.sub(r"\\N\[(\d+)\]", lambda m: data_heroes[int(m.group(1))]["name"], text)
        # extract color conversions
        text = re.sub(r"\\C\[(#[A-F0-9]{6})\]", self.re_color, text)
        return text
    
    def update(self):
        """Draw one character each update, or display them instantly"""
        if self.instant:
            while self.letter_idx < len(self.text):
                self.draw_letter()
        elif self.letter_idx < len(self.text):
            self.draw_letter()
    
    def draw_letter(self):
        """Handles drawing of a single letter"""
        # check for color change
        if self.letter_idx in self.data_color:
            self.color = self.data_color[self.letter_idx]
        # render the single letter
        letter = self.text[self.letter_idx]
        self.font.render_to(self, (self.x + shadow, self.y + shadow), letter, 'black')
        self.font.render_to(self, (self.x, self.y), letter, self.color)
        # and move the start position
        self.x += self.metrics[self.letter_idx][M_ADV_X]
        self.letter_idx += 1
        # check for end of line
        if letter == ' ':
            self.word_idx += 1
            self.word_wrap()

    def word_wrap(self):
        """Moves to the next line if the next word won't fit"""
        bounds = self.font.get_rect(self.words[self.word_idx])
        if self.x + bounds.width > self.text_surf_rect.width:
            self.new_line()

    def new_line(self):
        """Return x to start, while moves y to next line"""
        self.x, self.y = 0, self.y + self.font.get_sized_height() + 2
