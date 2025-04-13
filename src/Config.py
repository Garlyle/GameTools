import pygame
import os
import configparser

config_filename = 'config.ini'
section_keys = 'Bindings'
section_common = 'Settings'
class Config:
    def __init__(self):
        """Load saved config"""
        self.config = configparser.ConfigParser()
        if (os.path.isfile(config_filename)):
            self.config.read(config_filename)
        else:
            self.generate_default_config()
    
    def generate_default_config(self):
        """Generates a config file if doesn't exist"""
        settings = {
            'width': 640,
            'height': 480,
            'fps': 60,
            'fullscreen': False
        }
        self.set(section_common, settings)
        input_map = {
            'right': pygame.K_d, 
            'left': pygame.K_a,
            'up' : pygame.K_w,
            'down': pygame.K_s
        }
        self.set(section_keys, input_map)
        self.export()

    def get(self, name):
        """return a config section as a dictionary"""
        dict = {}
        for key in self.config[name]:
            dict[key] = self.config.get(name, key)
            if dict[key].isnumeric():
                dict[key] = int(dict[key])
            elif dict[key] in ('True', 'False'):
                dict[key] = (dict[key] == 'True')
        return dict
    
    def set(self, name, value):
        """updates a config section with a dictionary"""
        self.config[name] = value
    
    def export(self):
        """overwrite existing config file"""
        with open(config_filename, 'w') as configfile:
            self.config.write(configfile)
