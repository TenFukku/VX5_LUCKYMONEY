import pygame
import image
from settings import *
from hand_tracking import HandTracking
import cv2

class Hand:
    def __init__(self):
        self.orig_image = image.load("Assets/hand-open.png", size=(HAND_SIZE, HAND_SIZE))
        self.image = self.orig_image.copy()
        self.image_smaller = image.load("Assets/hand-close.png", size=(HAND_SIZE - 50, HAND_SIZE - 50))
        self.rect = pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, HAND_HITBOX_SIZE[0], HAND_HITBOX_SIZE[1])
        self.left_click = False
        self.isOpen = True
        #self.hand_tracking = HandTracking()


    def follow_mouse(self): # change the hand pos center at the mouse pos
        self.rect.center = pygame.mouse.get_pos()
        #self.hand_tracking.display_hand()

    def follow_mediapipe_hand(self, x, y):
        self.rect.center = (x, y)

    def draw_hitbox(self, surface):
        pygame.draw.rect(surface, (200, 60, 0), self.rect)


    def draw(self, surface):
        image.draw(surface, self.image, self.rect.center, pos_mode="center")

        if DRAW_HITBOX:
            self.draw_hitbox(surface)

    # lấy ra những con vật được cộng điểm
    def on_insect(self, insects): # return a list with all insects that collide with the hand hitbox
        return [insect for insect in insects if self.rect.colliderect(insect.rect)]

    # lấy ra những con vật làm mất điểm
    def kill_insects(self, insects, score, sounds): # will kill the insects that collide with the hand when the left mouse button is pressed
        if self.left_click:
            # Check if the hand was open in the previous frame
            if self.isOpen:
                for insect in self.on_insect(insects):
                    insect_score = insect.kill(insects)
                    score += insect_score
                    sounds["slap"].play()
                    if insect_score < 0:
                        sounds["screaming"].play()

                # Update the hand state to indicate it's closed
                self.isOpen = False
        else:
            # Update the hand state to indicate it's open
            self.isOpen = True

        return score

# ý tưởng đổi lại thành có nhiều loại bao lì xì với các mức điểm khác nhau
# không trừ điểm, chỉnh lại 1 âm thanh nền
# bắt trúng bao lì xì thì sẽ có âm thanh khác