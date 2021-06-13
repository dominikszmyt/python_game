import pygame
import random
import time
import os
import pickle
fps = pygame.time.Clock()
#colors
white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)
green = pygame.Color(85,182,91)
yellow = pygame.Color(222,222,89)
#window config
window_width=int(900)
window_height=int(600)
#initializing game
pygame.init()
#game window
game_window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("SSSnake")
#sounds
path = os.path.abspath("SSSnake.py")
head, tail = os.path.split(path)
egs_file = head + "\\Sounds\\end_game_sound.mp3"
sn_file = head + "\\Sounds\\snake_sound.mp3"
fs_file = head + "\\Sounds\\fruit_sound.mp3"
end_game_sound = pygame.mixer.Sound(egs_file)
snake_sound = pygame.mixer.Sound(sn_file)
fruit_sound = pygame.mixer.Sound(fs_file)
#menu buttons
font_tnn = pygame.font.SysFont ("Times New Norman", 25)
start = font_tnn.render("START", True, white)
start_rect = pygame.Rect(window_width/2-50,window_height/4,100,40)
quit = font_tnn.render("QUIT", True, white)
quit_rect = pygame.Rect(window_width/2-50,window_height*0.8,100,40)
#title text
font_tnn_title = pygame.font.SysFont ("Times New Norman", 75)
title = font_tnn_title.render("SSSnake", True, white)
instruction_ttn = pygame.font.SysFont("Times New Norman", 45)
#instruction/leaderboard text
instruction_one = instruction_ttn.render("Your goal is to collect fruits" , True, white)
instruction_two = instruction_ttn.render("withour crashing into edge", True, white)
instruction_three = instruction_ttn.render("or your own body", True, white)
instruction_four = instruction_ttn.render("Move using arrow keys", True, white)
leaderboard_ttn = pygame.font.SysFont("Times New Norman", 35)
leaderboard = leaderboard_ttn.render("Leaderboard", True, white)
#variables
#high scores
path = os.path.abspath("SSSnake.py")
head, tail = os.path.split(path)
hs_file = head + "\\high_scores.txt"
try:
    with open(hs_file, "rb") as tab:
        high_scores = pickle.load(tab)
except:
    high_scores = [0,0,0,0,0,0,0,0,0]
#functions used by game
def dot_amount(text):
    """Function retuns amount of spaces to allign highscores"""
    if len(text) == 3:
        return ". "
    elif len(text) == 2:
        return ".  "
    elif len(text) == 1:
        return ".   "
def snake_game():
    """Game loop"""
    game_logic = True
    while game_logic:   
        #score
        current_score = 0
        #fruit
        fruit_position = [[random.randrange(0,(window_width/15))*15,random.randrange(0,(window_height/15))*15]]
        fruit_spawn_logic = True
        #snake
        snake_position=[450,300]
        snake_body=[[450,300],[435,300],[420,300],[405,300]]
        snake_speed = 15 
        side = "UP"
        #some variables
        truth_table = []
        #handling events
        while True:      
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    pygame.mixer.Sound.play(snake_sound)
                    if event.key == pygame.K_UP:
                        side = "UP"
                    if event.key == pygame.K_DOWN:
                        side = "DOWN"
                    if event.key == pygame.K_RIGHT:
                        side = "RIGHT"
                    if event.key == pygame.K_LEFT:
                        side = "LEFT"
            if side == "UP":
                snake_position[1] -= 15
            if side == "DOWN":
                snake_position[1] += 15
            if side == "RIGHT":
                snake_position[0] += 15
            if side == "LEFT":
                snake_position[0] -= 15
            #snake growth
            snake_body.insert(0,list(snake_position))
            #fruit check
            for i in range(len(fruit_position)):
                if snake_position[0] == fruit_position[i][0] and snake_position[1] == fruit_position[i][1]:
                    pygame.mixer.Sound.play(fruit_sound)
                    current_score += 1
                    fruit_spawn_logic = False
                    truth_table.append(True) 
                    if current_score % 10 == 0 and current_score != 0 :
                        fruit_position.append([random.randrange(0,(window_width/15))*15,random.randrange(0,(window_height/15))*15])    
                else:
                    truth_table.append(False)
                if len(truth_table) == len(fruit_position) and True not in truth_table:
                    snake_body.pop()
            truth_table = []
            if not fruit_spawn_logic:
                fruit_position.remove([snake_position[0],snake_position[1]])
                fruit_position.append([random.randrange(0,(window_width/15))*15,random.randrange(0,(window_height/15))*15])
            fruit_spawn_logic = True
            game_window.fill(black)
            #drawing snake/fruit
            for position in snake_body:
                pygame.draw.rect(game_window,green,pygame.Rect(position[0],position[1], 15, 15))
            for fruit in fruit_position:
                pygame.draw.rect(game_window,white,pygame.Rect(fruit[0],fruit[1], 15 ,15))
            #end_game conditions
            for body in snake_body[1:]:
                if snake_position[0] == body[0] and snake_position[1] == body[1]:
                    end_game(current_score)
            if snake_position[0] < 0 or snake_position[0] > window_width - 15 > 0:
                end_game(current_score)
            if snake_position[1] < 0 or snake_position[1] > window_height - 15 > 0:
                end_game(current_score)  
            #refreshing game 
            show_score(current_score)
            pygame.display.update()
            fps.tick(snake_speed)
def main_menu():
    """Main Menu of the game"""
    main_menu_logic = True
    game_window.fill(black)
    high_score_open()
    while main_menu_logic:
        #start button
        pygame.draw.rect(game_window, yellow, start_rect)
        game_window.blit(start, (window_width/2-27,window_height/4+12))
        #quit button
        pygame.draw.rect(game_window, yellow, quit_rect)
        game_window.blit(quit, (window_width/2-20,window_height*0.8+12))
        #menu text
        game_window.blit(title, (window_width/2-120,window_height*0.1))
        game_window.blit(instruction_one, (window_width/4,window_height*0.40))
        game_window.blit(instruction_two, (window_width/4+10,window_height*0.40+45))
        game_window.blit(instruction_three, (window_width/4+80,window_height*0.40+90))
        game_window.blit(instruction_four, (window_width/2-190,window_height*0.40+135))
        game_window.blit(leaderboard, (window_width*0.8-70, window_height*0.15))
        #high_scores list
        for i in range(9):
            high_scores_font = pygame.font.SysFont("times new roman",35)
            high_scores_surface = high_scores_font.render(str(i+1) + dot_amount(str(high_scores[i])) + str(high_scores[i]),True,white)
            high_scores_rect = high_scores_surface.get_rect()
            high_scores_rect.midtop = (window_width*0.8,(window_height*0.2)+35*i)
            game_window.blit(high_scores_surface,high_scores_rect)
        pygame.display.update()
        #event handling    
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                cursor_position = pygame.mouse.get_pos()
                if (window_width/2)-50 <= cursor_position[0] <= (window_width/2)+50 and (window_height/4) <= cursor_position[1] <= (window_height/4)+40:
                    main_menu_logic = False
                    snake_game()
                    main_menu_logic = True
                if window_width/2-50 <= cursor_position[0] <= (window_width/2)+50 and window_height*0.8 <= cursor_position[1] <= (window_height*0.8)+40:
                    time.sleep(2)
                    pygame.quit()
                    #quit()
def high_scores_save():
    """Function saves high scores in file"""
    high_scores.sort()
    high_scores.reverse()
    while len(high_scores) < 9:
        high_scores.append(0)
    while len(high_scores) > 9:
        high_scores.remove(high_scores[-1])
    with open(hs_file, "wb") as tab:
        pickle.dump(high_scores, tab)
def high_score_open():
    """Function opens/reads and update high score file"""
    try:
        with open(hs_file, "rb") as tab:
            high_scores = pickle.load(tab)
    except:
        pass
def show_score(score):
    """Function displays score"""
    score_font = pygame.font.SysFont("times new roman",22)
    score_surface = score_font.render("Score: " + str(score),True,white)
    score_rect = score_surface.get_rect()
    game_window.blit(score_surface, score_rect)
def end_game(score):
    """Function ends current game"""
    pygame.mixer.Sound.play(end_game_sound)
    high_scores.append(score)
    high_scores_save()
    end_game_font = pygame.font.SysFont("times new roman",70)
    end_game_surface = end_game_font.render("Your end score is " + str(score),True,white)
    end_game_rect = end_game_surface.get_rect()
    end_game_rect.midtop = (window_width/2,window_height/2)
    game_window.blit(end_game_surface,end_game_rect)
    pygame.display.flip()
    time.sleep(3)
    game_logic = False
    main_menu()
main_menu()
#snake_game()
pygame.quit()
quit()