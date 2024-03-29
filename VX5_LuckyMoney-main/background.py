import pygame
import image
from settings import *

# dùng để vẽ background, chỉnh lại kích thước của background
class Background:
    def __init__(self):
        self.image = image.load("Assets/background3.png", size=(SCREEN_WIDTH, SCREEN_HEIGHT), 
                                convert="default")


    def draw(self, surface):
        image.draw(surface, self.image, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), pos_mode="center")

# chia 2 để canh chỉnh ở giữa