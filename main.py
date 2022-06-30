import pygame
import sys
import random
import pandas as pd
import openpyxl
from datetime import datetime

pygame.init()

button_sound = pygame.mixer.Sound('button.wav')  # sound for button click
button_sound.set_volume(0.2)
lost_sound = pygame.mixer.Sound('lost.wav')  # sound for game lose
lost_sound.set_volume(0.1)
apple_sound = pygame.mixer.Sound('apple.wav')  # sound for eating apple
apple_sound.set_volume(0.1)
game_sound = pygame.mixer.Sound('gamemusic.wav')  # standard game music
current_lock = 0  # needed for choosing which menu is opened
Score = 0  # current score
Last_Score = 0  # last score
tail_segments = []  # arr of tail segments

screen = pygame.display.set_mode((1200, 800))  # screen

excel_data_df = pd.read_excel('results.xlsx')  # read info from save file
DateTime = excel_data_df['DateTime'].tolist()  # from save file get date's
Game_Results = excel_data_df['Result'].tolist()  # from save file get results


def set_current_lock(a: int):  # which menu is opened
    global current_lock
    global Last_Score
    current_lock = a
    if a == 0:  # if main menu
        game_sound.set_volume(0.1)
    if a == 4:  # if lose menu
        game_sound.set_volume(0)  # silence main music
        pygame.mixer.Sound.play(lost_sound)  # play lose sound
        Last_Score = Score  # last score = current score
        current_datetime = datetime.now()  # getting current date and time
        DateTime.append(
            str(current_datetime.date()) + " " + str(current_datetime.hour) + ":" + str(current_datetime.minute) +
            ":" + str(current_datetime.second))  # append DateTime list with new line
        Game_Results.append(Last_Score)  # append Game_Results list with new line
        df = pd.DataFrame({'DateTime': DateTime,
                           'Result': Game_Results})  # append table
        df.to_excel('./results.xlsx')  # save excel
        pygame.time.delay(1500)


def score_up():  # eating apple
    global Score
    Score += 10  # adding score
    pygame.mixer.Sound.play(apple_sound)  # playing eating apple sound


def print_text(message: str, x: int, y: int, font_color='black', font_type='pixelfont.ttf', font_size=80):  # text
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


class Apple:  # apple
    def __init__(self):  # constructor
        self.width = 15
        self.height = 15
        self.color = 'Red'
        self.x = random.randint(220, 980)  # random position
        self.y = random.randint(250, 710)

    def draw(self):  # draw apple on screen
        if screen.get_at((self.x, self.y)) == (0, 0, 0, 255):
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def update(self):  # move apple to other place
        self.x = random.randint(220, 980)
        self.y = random.randint(250, 710)


apple = Apple()  # apple create


class Segment:  # snake tale segment class
    def __init__(self, x: int, y: int):  # constructor
        self.width = 10
        self.height = 10
        self.x = x
        self.y = y
        self.color = (13, 162, 58)

    def draw(self):  # draw segment on screen
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self, x: int, y: int):  # move segment to other place
        self.x = x
        self.y = y


class Snake:  # snake class (head)
    def __init__(self):  # constructor
        self.width = 10
        self.height = 10
        self.x = 597
        self.y = 397
        self.color = (13, 162, 58)

    def draw(self):  # draw snake, moving
        global tail_segments
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))  # head
        keys = pygame.key.get_pressed()  # get pressed key

        if keys[pygame.K_w]:  # up
            if len(tail_segments) != 0:
                for i in range(len(tail_segments) - 1, -1, -1):
                    if i == 0:
                        tail_segments[i].move(self.x, self.y)
                    else:
                        tail_segments[i].move(tail_segments[i - 1].x, tail_segments[i - 1].y)
            if screen.get_at((self.x, self.y - 10)) == (13, 162, 58, 255):  # killed itself
                set_current_lock(4)
            self.y -= 10
        elif keys[pygame.K_s]:  # down
            if len(tail_segments) != 0:
                for i in range(len(tail_segments) - 1, -1, -1):
                    if i == 0:
                        tail_segments[i].move(self.x, self.y)
                    else:
                        tail_segments[i].move(tail_segments[i - 1].x, tail_segments[i - 1].y)
            if screen.get_at((self.x, self.y + 20)) == (13, 162, 58, 255):  # killed itself
                set_current_lock(4)
            self.y += 10
        elif keys[pygame.K_a]:  # left
            if len(tail_segments) != 0:
                for i in range(len(tail_segments) - 1, -1, -1):
                    if i == 0:
                        tail_segments[i].move(self.x, self.y)
                    else:
                        tail_segments[i].move(tail_segments[i - 1].x, tail_segments[i - 1].y)
            if screen.get_at((self.x - 10, self.y)) == (13, 162, 58, 255):  # killed itself
                set_current_lock(4)
            self.x -= 10
        elif keys[pygame.K_d]:  # right
            if len(tail_segments) != 0:
                for i in range(len(tail_segments) - 1, -1, -1):
                    if i == 0:
                        tail_segments[i].move(self.x, self.y)
                    else:
                        tail_segments[i].move(tail_segments[i - 1].x, tail_segments[i - 1].y)
            if screen.get_at((self.x + 20, self.y)) == (13, 162, 58, 255):  # killed itself
                set_current_lock(4)
            self.x += 10

        if self.x < 200 or self.x > 990 or self.y < 230 or self.y > 720:  # killed with wall
            set_current_lock(4)
            self.x = 597
            self.y = 397
        if (apple.x <= self.x <= apple.x + 15 and apple.y <= self.y <= apple.y + 15) \
                or (apple.x <= self.x + 10 <= apple.x + 15 and apple.y <= self.y + 10 <= apple.y + 15):  # eat apple
            apple.update()  # move apple to new place
            score_up()
            if len(tail_segments) == 0:
                tail_segments.append(Segment(self.x + 10, self.y))  # new segment to tail with 0 segments
            else:  # with more than 0 segments
                tail_segments.append(
                    Segment(tail_segments[len(tail_segments) - 1].x + 10, tail_segments[len(tail_segments) - 1].y))

        pygame.time.delay(30)  # time between frames


class Button:  # button class
    def __init__(self, width: int, height: int):  # constructor
        self.width = width
        self.height = height
        self.inactive_color = (13, 162, 58)
        self.active_color = (23, 204, 58)

    def draw(self, x: int, y: int, text_x: int, text_y: int, text: str, i=-1):  # draw button
        mouse = pygame.mouse.get_pos()  # get mouse pos
        click = pygame.mouse.get_pressed()  # get click or not
        global tail_segments

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:  # if mouse on button
            pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))  # change color to active
            if click[0] == 1:  # if clicked
                pygame.mixer.Sound.play(button_sound)  # play sound of click
                pygame.time.delay(300)
                if i != -1:  # to other menu
                    set_current_lock(i)
                    if i == 0:  # to main menu
                        tail_segments = []

        else:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))  # if mouse not on button

        print_text(text, x + text_x, y + text_y)  # text in button


def sort_key(datetime_item: str):  # function for sort of results
    # DateTime
    # Game_Results
    for i in range(len(DateTime)):
        if DateTime[i] == datetime_item:
            return Game_Results[i]


play_button = Button(400, 100)  # play
results_button = Button(400, 100)  # results
back_button = Button(100, 100)  # back
exit_button = Button(400, 100)  # exit
player = Snake()  # create snake
game_sound.set_volume(0.1)
pygame.mixer.Sound.play(game_sound, loops=-1)  # play game music
while True:
    screen.fill((0, 0, 0))  # reload
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if current_lock == 0:  # main menu
        print_text("Snake", 490, 100, font_color='white')  # label
        play_button.draw(400, 235, 110, 15, "Play", 1)  # play
        results_button.draw(400, 385, 50, 15, "Results", 2)  # results
        exit_button.draw(400, 535, 110, 15, "Exit", 3)  # exit
        player = Snake()  # update player
        Score = 0  # null score
        excel_data_df = pd.read_excel('results.xlsx')  # read from file
        DateTime = excel_data_df['DateTime'].tolist()
        Game_Results = excel_data_df['Result'].tolist()
    elif current_lock == 1:  # game
        print_text("Game", 510, 100, font_color='white')  # label
        back_button.draw(80, 80, 25, 15, "<", 0)  # back
        pygame.draw.rect(screen, 'white', pygame.Rect(200, 230, 800, 500), 2)  # game field
        print_text(str(Score), 1000, 100, font_color='white')  # score label
        for segment in tail_segments:  # snake segments
            segment.draw()
        player.draw()  # snake
        apple.draw()  # apple
    elif current_lock == 2:  # results
        print_text("Results", 450, 100, font_color='white')  # label
        back_button.draw(80, 80, 25, 15, "<", 0)  # back
        DateTime = sorted(DateTime, key=sort_key, reverse=True)  # sort results
        Game_Results = sorted(Game_Results, reverse=True)
        for i in range(0, 5):  # five best results
            if i < len(DateTime):
                print_text(str(i+1)+". "+DateTime[i]+"   "+str(Game_Results[i]), 150, 250+100*i,
                           font_color='white', font_size=60)
            else:
                print_text(str(i + 1) + ". ", 150, 250 + 100 * i,
                           font_color='white', font_size=60)
        player = Snake()  # update player
        Score = 0  # null score
    elif current_lock == 3:  # exit
        pygame.quit()
        sys.exit()
    elif current_lock == 4:  # game over
        print_text("Game Over!", 410, 100, font_color='white')  # label
        back_button.draw(80, 80, 25, 15, "<", 0)  # back
        print_text(str(Last_Score), 600, 400, font_color='white')  # score
        Score = 0  # null score
        player = Snake()  # update player
    pygame.display.flip()  # update frame
