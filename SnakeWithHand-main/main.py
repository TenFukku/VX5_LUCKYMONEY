# import the pygame module, so you can use it
import pygame
# import random to randomly place food
import random
# import time to wait before closing the game
import time
# import sys to exit
import sys
import mediapipe as mp
import os
import random

import cv2
import numpy as np
from model import keras_model
import tensorflow.keras

#Getting mediapipe: Hands ready
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

def new_food():
        foodx = round(random.randrange(10, screen_w - 10) / 10.0) * 10.0
        foody = round(random.randrange(10, screen_h - 10) / 10.0) * 10.0
        return (foodx, foody)

# current score display on screen 
def current_score(score):
    value = score_font.render("Score: " + str(score), True, red)
    screen.blit(value, [5, 0])
    return score

# save score in file ./data/score.txt
def save_score(score):
    final_score = ','+str(score)
    with open('./data/score.txt', 'a', encoding = 'utf-8') as file:
        file.write(f'{final_score}')
    return final_score

# read ./data/score.txt and select best score 
def get_best_score(file):
    with open('./data/score.txt', 'r+', encoding = 'utf-8') as file:
        for line in file:
            scores_best_score = line.strip().split(",")
        bs = list([int(x) for x in scores_best_score])
    if (len(bs) <=0):
        return '0'
    if (len(bs) > 0):
        bs.sort()
        return bs[-1]
    
# best score display on screen  
def display_best_score(file, score):
    best_score = str(get_best_score(file))
    if int(best_score) < int(score):
        best_score = int(score)
    value = score_font.render("Best Score: " + str(best_score), True, red)
    screen.blit(value, [330, 0])
    return

# message end game display on screen
def message(msg,color, font_style, x, y):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [x, y])

def button(screen, color, x, y, w, h, msg):
    # draw the button with the message
    pygame.draw.rect(screen, color, [x, y, w , h])
    message(msg, black, score_font, x+25, y+5)

def select_level():
    # get position of the mouse and every click
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # easy = 15f/s, hard = 25f/s
    level = 0 
    # adjust level depending on button clicked
    # run mainloop once level is chosen
    if ((205+110 > mouse[0] > 205) and (250+45 > mouse[1] > 45)):
        if (click[0] == 1 and mouse[1]<300):
            level = 10

    if  ((205+110 > mouse[0] > 205) and (350+45 > mouse[1] > 45)):
        if ((click[0] == 1) and (mouse[1]>300)): 
            level = 25
    
    return level       


def menu():
    menu = True
    clock = pygame.time.Clock()
    level = 0
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # change the value to False, to exit the loop
                menu = False
                pygame.display.quit()
                sys.exit()
           
            screen.fill(grey)
            message('Snake Game', green, font_style, screen_w//2-165, screen_h//2-200)
            message('by UIT', green, score_font, screen_w//2-50, screen_h//2-90)

            button(screen, (200,200,200), 205, 250, 110 , 45, 'EASY')
            button(screen, (120,120,120), 205, 350, 110 , 45, 'HARD') 

            level = select_level()
            if (level != 0):
                menu = False   
            pygame.display.update()
            clock.tick(15)

    return level

# define a main function
def game(level, model):
    print('===START GAME===')
    vid_capture = cv2.VideoCapture(0)

    # create the snake (centered) 
    x_head = screen_w//2
    y_head = screen_h//2
    
    x_change = 0
    y_change = 0
        
    # define a variable to control the main loop
    running = True
     
    clock = pygame.time.Clock()
    
    food = new_food()
    foodx = food[0]
    foody = food[1]

    score = 0

    # store the directions to get the previous direction and make reverse impossible
    directions = ['']

    snake_body = []
    snake_len = 0
    # main loop
    count = 0
    left_wait = 0
    right_wait = 0
    rotate_wait = 0
    down_wait = 0
    while running:
        #capture 1 image/frame par 2s
        vid_capture.set(cv2.CAP_PROP_POS_MSEC,(count*2000))    # added this line 
        
        #ouvre une fenetre avec la webcam
        cv2.namedWindow("Camera")
        
        #lit les images (frames)
        success,image = vid_capture.read()
        
        im_preview = cv2.flip(image, 1)
        cv2.imshow("Camera", im_preview)

        # save frame as JPEG file
        cv2.imwrite("frame.jpg", image)     
        
        count += 1
        frame = cv2.imread('frame.jpg')
        imgRGB = cv2.cvtColor(im_preview, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = im_preview.shape
                    if id == 0:
                        x = []
                        y = []
                    x.append(int((lm.x) * w))
                    y.append(int((1 - lm.y) * h))

                    #This will track the hand gestures
                    if len(y) > 20:
                        if (x[0] > x[3] > x[4]) and not(y[20] > y[17]):
                           left_wait += 1
                        if not(x[0] > x[3] > x[4]) and (y[20] > y[17]):
                            right_wait += 1
                        if (x[0] > x[3] > x[4]) and (y[20] > y[17]):
                            rotate_wait += 1


                mpDraw.draw_landmarks(im_preview, handLms, mpHands.HAND_CONNECTIONS)

        else:
            down_wait += 1

                #"if you gesture to ROTATE  for at least 4 frames, piece ROTATES"
        if rotate_wait >= 4:
            left_wait = 0
            right_wait = 0
            rotate_wait = 0
            down_wait = 0
            print('action up')
            x_change = 0
            y_change = -5
            directions.append('up') 
            cv2.putText(im_preview, "UP", (280,40), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 178, 102, 255), 3) 
            cv2.imshow("Camera", im_preview)

        #"if you gesture to the RIGHT for at least 4 frames, piece move RIGHT"
        if right_wait >= 4:
            left_wait = 0
            right_wait = 0
            rotate_wait = 0
            down_wait = 0
            print('action right')
            x_change = 5
            y_change =0
            directions.append('right') 
            cv2.putText(im_preview, "RIGHT", (535,240), cv2.FONT_HERSHEY_COMPLEX, 1, (178, 255, 102, 255), 3) 
            cv2.imshow("Camera", im_preview)

        if left_wait >= 4:
            left_wait = 0
            right_wait = 0
            rotate_wait = 0
            down_wait = 0
            print('action left')
            x_change = -5
            y_change = 0
            directions.append('left') 
            cv2.putText(im_preview, "LEFT", (10,240), cv2.FONT_HERSHEY_COMPLEX, 1, (51, 255, 255, 255), 3)  
            cv2.imshow("Camera", im_preview)


        #"if you gesture to go DOWN (no hand on the screen) for at least 5 frames, piece go DOWN (moves very fast)"
        if down_wait >= 5:
            left_wait = 0
            right_wait = 0
            rotate_wait = 0
            down_wait = 0
            print('action down')
            x_change = 0
            y_change = 5
            directions.append('down')
            cv2.putText(im_preview, "DOWN", (280,440), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 153, 153, 255), 3) 
            cv2.imshow("Camera", im_preview)

    
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
                pygame.display.quit()
                sys.exit()


        # position updated (move)
        x_head += x_change
        y_head += y_change
        
        # screen filled in black to display only the new position of the snake
        screen.fill(black)
        #pygame.draw.rect(screen, white, [x_head, y_head, 10, 10])

        # create bondaries
        width = 1
        boundaries = [(0-width, 0), (0, screen_h-width), (0 ,0), (screen_w, 0),
                    (screen_w-width, 0), (screen_w-width, screen_h-width), 
                    (0, screen_h-width), (screen_w-width, screen_h-width)]

        pygame.draw.lines(screen, red, False, boundaries, 1)
        
        # bondaries
        if (x_head<0 or x_head>screen_w or y_head<0 or y_head>screen_h):
            running = False
            save_score(score)
            message("WASTED",red, font_style, screen_w//2-140, screen_h//2-80)
        
        #food
        pygame.draw.rect(screen, green, [int(foodx), int(foody), 10, 10])

        # if food is eaten, create new food and increment score
        if (foodx-5<=x_head<=foodx+5 and foody-5<=y_head<=foody+5):
            food = new_food()
            foodx = food[0]
            foody = food[1]
            score += 1
            get_best_score('./data/score.txt')
            snake_len += 1
        
        # store position of snake_head every iteration
        snake_head = []
        snake_head.append(x_head)
        snake_head.append(y_head)
        
        # append ([x_head, y_head]) the position of the snake_head to the snake body
        snake_body.append(snake_head)
        
        # for each previous position of the snake, draw the body of the snake
        for xy in snake_body:
            pygame.draw.rect(screen, grey, [xy[0], xy[1], 10, 10])    
        
        # delete the old position to keep only a body of the good length
        if (len(snake_body) > snake_len):
            # delete the duplicated head so we start with only one snake block 
            del snake_body[0]
       
        # game over if head of snake touch its body
        # last block of body has same x,y than head when created
        for xy in snake_body[:-1]:   
            if (snake_head == xy):
                running = False
                save_score(score)
                message("WASTED",red, font_style, screen_w//2-140, screen_h//2-80)
                

        current_score(score)
        display_best_score('./data/score.txt', score)
        # update the entire screen with a timeframe of 5 frames per secondes 
        pygame.display.update()
        # increase frames per sec to increase difficulty
        clock.tick(level)
    end_game(level)
    return 

def end_game(level):
    model = tensorflow.keras.models.load_model('model/keras_model.h5', compile=False)
    wait = True
    while wait:
        message("SPACE  to  Replay",white, over_style, screen_w//2-70, screen_h//2+50)
        message("ENTER  to   MENU",white, over_style, screen_w//2-70, screen_h//2+90)
        message("  Q    to   QUIT",white, over_style, screen_w//2-70, screen_h//2+130)
        pygame.display.update()  
        
        time.sleep(0.1)
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_SPACE):
                    wait = False
                    game(level, model)

                elif (event.key == pygame.K_RETURN):
                    wait = False
                    main()

                elif (event.key == pygame.K_q):
                    wait = False
                    pygame.display.quit()
                    sys.exit()
            
            if (event.type == pygame.QUIT):
                # change the value to False, to exit the loop
                wait = False
                pygame.display.quit()
                sys.exit()

    return

def main():
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("./data/logo.jpg")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Snake game by UIT")
        
    # some colors for our game
    green = (50,205, 50)
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    grey = (128, 128, 128)

    # create a surface on screen that has the size of 500 x 500
    screen_w = 500
    screen_h = 500
    screen = pygame.display.set_mode((screen_w, screen_h))

    # font style for message and score
    font_style = pygame.font.SysFont("chiller", 100)
    score_font = pygame.font.SysFont("chiller", 35)
    over_style = pygame.font.SysFont("dejavusans", 25)

    scores = []
    bs = []
    model = tensorflow.keras.models.load_model('model/keras_model.h5', compile=False)
    level = menu() 
    game(level, model)
    return

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("./data/logo.jpg")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Snake game")
        
    # some colors for our game
    green = (50,205, 50)
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    grey = (128, 128, 128)

    # create a surface on screen that has the size of 500 x 500
    screen_w = 500
    screen_h = 500
    screen = pygame.display.set_mode((screen_w, screen_h))

    # font style for message and score
    font_style = pygame.font.SysFont("chiller", 100)
    score_font = pygame.font.SysFont("chiller", 35)
    over_style = pygame.font.SysFont("dejavusans", 25)

    scores = []
    bs = []
    
    main()
    