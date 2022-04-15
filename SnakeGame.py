'''Game Title : Snake Game
   Game Developer : Sanjyot Panure
   Language Used: Python
   Modules used: Pygame, random '''

import pygame
import random
import os
# from pygame import mixer
pygame.mixer.init()

# Initializing the game
pygame.init()
clock = pygame.time.Clock()

# defining colours
white = (255, 255, 255)
red = (241, 42, 74)
purple = (178, 58, 164)

# creating window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))
pygame.display.update()
# game title
pygame.display.set_caption("Snake Game")

# Loading required images
gameScreen = pygame.image.load("images/game_screen.png")           # main game screen
gameScreen = pygame.transform.scale(gameScreen, (screen_width, screen_height)).convert_alpha()

gameOver = pygame.image.load("images/gameover.png")                # Game Over screen
gameOver = pygame.transform.scale(gameOver, (screen_width, screen_height)).convert_alpha()

food = pygame.image.load("images/apple.png")                       # food
food = pygame.transform.scale(food, (35, 35)).convert_alpha()

snakeimg = pygame.image.load("images/snake.png")                   # loading snake image
snakeimg = pygame.transform.scale(snakeimg, (35, 45)).convert_alpha()

font = pygame.font.SysFont(None, 55, bold=True)

# defining funtions
def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])                           # updates screen

def plot_snake(gameWindow, snk_list, snake_size):
    for x,y in snk_list:
        gameWindow.blit(snakeimg, [x, y])  

def welcome():
    exit_game = False
    while not exit_game:
        welcomeScreen = pygame.image.load("images/welcome_screen.png")
        welcomeScreen = pygame.transform.scale(welcomeScreen, (screen_width, screen_height)).convert_alpha()
        gameWindow.blit(welcomeScreen, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load("sounds/click.mp3")
                    pygame.mixer.music.play()
                    gameloop()           
        pygame.display.update()
        clock.tick(60)

# creating Game loop
def gameloop():
    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 55
    snake_y = 75
    velocity_x = 0
    velocity_y = 0
    init_velocity = 3
    food_x = random.randint(15, 850)
    food_y = random.randint(40, 550)
    score = 0
    snake_size = 40
    fps = 60
    snk_list = []
    snk_length = 1

    if (not os.path.exists("highscore.txt")):
        with open("highscore.txt", "w") as f:
            f.write(str(0))

    with open("highscore.txt", "r") as f:
        highscore = f.read()

    while not exit_game:
        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))
            gameWindow.blit(gameOver, (0,0))
            text_screen(""+ str(highscore), red, 705, 29)
            text_screen(""+ str(score), purple, 290, 28)

            for event in pygame.event.get():         # Handling events   
                if event.type == pygame.QUIT:
                    exit_game =  True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.music.load("sounds/click.mp3")
                        pygame.mixer.music.play()
                        welcome()
        else:
            for event in pygame.event.get():         # Handling events   
                if event.type == pygame.QUIT:
                    exit_game =  True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0
                
            snake_x += velocity_x
            snake_y += velocity_y
            
            if abs(snake_x-food_x)<12 and abs(snake_y-food_y)<12:
                pygame.mixer.music.load("sounds/eat.mp3")
                pygame.mixer.music.play()
                score += 1
                food_x = random.randint(15, 850)
                food_y = random.randint(40, 550)
                snk_length += 5
                if score>int(highscore):
                    highscore = score

            gameWindow.fill(white)
            gameWindow.blit(gameScreen, (0 , 0))
            text_screen(""+ str(highscore), red, 705, 29)
            text_screen(""+ str(score), purple, 290, 28)
            gameWindow.blit(food, (food_x, food_y))

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]
                
            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load("sounds/gameover.mp3")       # play gameover sound when snake hits his body
                pygame.mixer.music.play()
            if snake_x<10 or snake_x>(screen_width-15) or snake_y<10 or snake_y>(screen_height-15):
                game_over = True
                pygame.mixer.music.load("sounds/gameover.mp3")       # play gameover sound when snake hits side walls
                pygame.mixer.music.play()

            plot_snake(gameWindow, snk_list, snake_size)           
        
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

welcome()