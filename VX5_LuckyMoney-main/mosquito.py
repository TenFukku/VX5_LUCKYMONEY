#Đang chỉnh file này lại để điều chỉnh tần suất xuất hiện

import pygame
import math
import random
import time
import image
from settings import *

class Mosquito:
    def __init__(self):
        #size
        # random_size_value = random.uniform(MOSQUITO_SIZE_RANDOMIZE[0], MOSQUITO_SIZE_RANDOMIZE[1])
        # fix lại là kích thước nhân 2, không random
        random_size_value = 3
        size = (int(MOSQUITOS_SIZES[0] * random_size_value), int(MOSQUITOS_SIZES[1] * random_size_value))
        # moving
        moving_direction, start_pos = self.define_spawn_pos(size)
        # sprite
        self.rect = pygame.Rect(start_pos[0], start_pos[1], size[0]//1.4, size[1]//1.4)
        # self.images = [image.load("Assets/mosquito/baolixi1.png", size=size, flip=moving_direction=="right")]
        self.images = [image.load(f"Assets/bee6/{nb}.png", size=size, flip=moving_direction=="right") for nb in range(1, 11)]
        self.current_frame = 0
        self.animation_timer = 0

# Xác định hướng đi
    def define_spawn_pos(self, size): # define the start pos and moving vel of the mosquito
        vel = random.uniform(MOSQUITOS_MOVE_SPEED["min"], MOSQUITOS_MOVE_SPEED["max"])
        moving_direction = random.choice(("left", "right", "up", "down"))
        if moving_direction == "right":
            start_pos = (-size[0], random.randint(size[1], SCREEN_HEIGHT-size[1]))
            self.vel = [vel, 0]
        if moving_direction == "left":
            start_pos = (SCREEN_WIDTH + size[0], random.randint(size[1], SCREEN_HEIGHT-size[1]))
            self.vel = [-vel, 0]
        if moving_direction == "up":
            start_pos = (random.randint(size[0], SCREEN_WIDTH-size[0]), SCREEN_HEIGHT+size[1])
            self.vel = [0, -vel]
        if moving_direction == "down":
            start_pos = (random.randint(size[0], SCREEN_WIDTH-size[0]), -size[1])
            self.vel = [0, vel]
        return moving_direction, start_pos
    

    def move(self):
        self.rect.move_ip(self.vel)


    def animate(self): # change the frame of the insect when needed
        t = time.time()
        if t > self.animation_timer:
            self.animation_timer = t + ANIMATION_SPEED
            self.current_frame += 1
            if self.current_frame > len(self.images)-1:
                self.current_frame = 0

#xác  định hitbox
    def draw_hitbox(self, surface):
        # pygame.draw.rect(surface, (200, 60, 0), self.rect)
        # pygame.draw.rect(surface, (0, 0, 0), self.rect)

        
        hitbox_size_factor = 0.5  # Hệ số để làm nhỏ hitbox, bạn có thể điều chỉnh theo ý muốn
        hitbox_width = int(self.rect.width * hitbox_size_factor)
        hitbox_height = int(self.rect.height * hitbox_size_factor)

        # Xác định tọa độ cho hitbox nhỏ lại
        hitbox_x = self.rect.centerx - hitbox_width // 2
        hitbox_y = self.rect.centery - hitbox_height // 2

        # Vẽ hitbox
        hitbox_rect = pygame.Rect(hitbox_x, hitbox_y, hitbox_width, hitbox_height)
        pygame.draw.rect(surface, (200, 60, 0), hitbox_rect)



    def draw(self, surface):
        self.animate()
        image.draw(surface, self.images[self.current_frame], self.rect.center, pos_mode="center")
        if DRAW_HITBOX:
            self.draw_hitbox(surface)


    def kill(self, mosquitos): # remove the mosquito from the list
        mosquitos.remove(self)
        return 1

 