import pygame
import random
import image
from settings import *
from mosquito import Mosquito

class Bee(Mosquito):
    def __init__(self):
        #size
        random_size_value = 3
        size = (int(BEE_SIZES[0] * random_size_value), int(BEE_SIZES[1] * random_size_value))
        # moving
        moving_direction, start_pos = self.define_spawn_pos(size)
        # sprite
        self.rect = pygame.Rect(start_pos[0], start_pos[1], size[0]//5, size[1]//10)
        # self.images = [image.load(f"Assets/bee2/{nb}.png", size=size, flip=moving_direction=="right") for nb in range(1, 3)] # load the images
        self.images = [image.load("Assets/mosquito/baolixi5.png", size=size, flip=moving_direction=="right")]
        self.current_frame = 0
        self.animation_timer = 0

    def kill(self, mosquitos): # remove the mosquito from the list
        mosquitos.remove(self)
        return +BEE_PENALITY

    def define_spawn_pos(self, size): # define the start pos and moving vel of the bee
        # Sử dụng tốc độ riêng cho Bee
        vel = random.uniform(BEE_MOVE_SPEED["min"], BEE_MOVE_SPEED["max"])
        moving_direction = random.choice(("left", "right", "up", "down"))
        if moving_direction == "right":
            start_pos = (-size[0], random.randint(size[1], SCREEN_HEIGHT-size[1]))
            self.vel = [vel, 0]
        elif moving_direction == "left":
            start_pos = (SCREEN_WIDTH + size[0], random.randint(size[1], SCREEN_HEIGHT-size[1]))
            self.vel = [-vel, 0]
        elif moving_direction == "up":
            start_pos = (random.randint(size[0], SCREEN_WIDTH-size[0]), SCREEN_HEIGHT+size[1])
            self.vel = [0, -vel]
        elif moving_direction == "down":
            start_pos = (random.randint(size[0], SCREEN_WIDTH-size[0]), -size[1])
            self.vel = [0, vel]
        return moving_direction, start_pos
    