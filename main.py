import pygame
import sys
import random
import pandas as pd
import openpyxl
from datetime import datetime

pygame.init()

button_sound = pygame.mixer.Sound('button.wav')
current_lock = 0
Score = 0
Last_Score = 0
tail_segments = []

screen = pygame.display.set_mode((1200, 800))

excel_data_df = pd.read_excel('results.xlsx')
DateTime = excel_data_df['DateTime'].tolist()
Game_Results = excel_data_df['Result'].tolist()


def set_current_lock(a: int):
    global current_lock
    global Last_Score
    current_lock = a
    if a == 4:
        Last_Score = Score
        current_datetime = datetime.now()
        DateTime.append(
            str(current_datetime.date()) + " " + str(current_datetime.hour) + ":" + str(current_datetime.minute) +
            ":" + str(current_datetime.second))
        Game_Results.append(Last_Score)
        df = pd.DataFrame({'DateTime': DateTime,
                           'Result': Game_Results})
        df.to_excel('./results.xlsx')


def score_up():
    global Score
    Score += 10


def print_text(message: str, x: int, y: int, font_color='black', font_type='pixelfont.ttf', font_size=80):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


class Apple:
    def __init__(self):
        self.width = 15
        self.height = 15
        self.color = 'Red'
        self.x = random.randint(220, 980)
        self.y = random.randint(250, 710)

    def draw(self):
        if screen.get_at((self.x, self.y)) == (0, 0, 0, 255):
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def update(self):
        self.x = random.randint(220, 980)
        self.y = random.randint(250, 710)


apple = Apple()


class Segment:
    def __init__(self, x: int, y: int):
        self.width = 10
        self.height = 10
        self.x = x
        self.y = y
        self.color = (13, 162, 58)

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self, x: int, y: int):
        self.x = x
        self.y = y


class Snake:
    def __init__(self):
        self.width = 10
        self.height = 10
        self.x = 597
        self.y = 397
        self.color = (13, 162, 58)

    def draw(self):
        global tail_segments
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            if len(tail_segments) != 0:
                for i in range(len(tail_segments) - 1, -1, -1):
                    if i == 0:
                        tail_segments[i].move(self.x, self.y)
                    else:
                        tail_segments[i].move(tail_segments[i - 1].x, tail_segments[i - 1].y)
            if screen.get_at((self.x, self.y - 10)) == (13, 162, 58, 255):
                set_current_lock(4)
            self.y -= 10
        elif keys[pygame.K_s]:
            if len(tail_segments) != 0:
                for i in range(len(tail_segments) - 1, -1, -1):
                    if i == 0:
                        tail_segments[i].move(self.x, self.y)
                    else:
                        tail_segments[i].move(tail_segments[i - 1].x, tail_segments[i - 1].y)
            if screen.get_at((self.x, self.y + 20)) == (13, 162, 58, 255):
                set_current_lock(4)
            self.y += 10
        elif keys[pygame.K_a]:
            if len(tail_segments) != 0:
                for i in range(len(tail_segments) - 1, -1, -1):
                    if i == 0:
                        tail_segments[i].move(self.x, self.y)
                    else:
                        tail_segments[i].move(tail_segments[i - 1].x, tail_segments[i - 1].y)
            if screen.get_at((self.x - 10, self.y)) == (13, 162, 58, 255):
                set_current_lock(4)
            self.x -= 10
        elif keys[pygame.K_d]:
            if len(tail_segments) != 0:
                for i in range(len(tail_segments) - 1, -1, -1):
                    if i == 0:
                        tail_segments[i].move(self.x, self.y)
                    else:
                        tail_segments[i].move(tail_segments[i - 1].x, tail_segments[i - 1].y)
            if screen.get_at((self.x + 20, self.y)) == (13, 162, 58, 255):
                set_current_lock(4)
            self.x += 10

        if self.x < 200 or self.x > 990 or self.y < 230 or self.y > 720:
            set_current_lock(4)
            self.x = 597
            self.y = 397
        if (apple.x <= self.x <= apple.x + 15 and apple.y <= self.y <= apple.y + 15) \
                or (apple.x <= self.x + 10 <= apple.x + 15 and apple.y <= self.y + 10 <= apple.y + 15):
            apple.update()
            score_up()
            if len(tail_segments) == 0:
                tail_segments.append(Segment(self.x + 10, self.y))
            else:
                tail_segments.append(
                    Segment(tail_segments[len(tail_segments) - 1].x + 10, tail_segments[len(tail_segments) - 1].y))

        pygame.time.delay(30)


class Button:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.inactive_color = (13, 162, 58)
        self.active_color = (23, 204, 58)

    def draw(self, x: int, y: int, text_x: int, text_y: int, text: str, i=-1):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        global tail_segments

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))
            if click[0] == 1:
                pygame.mixer.Sound.play(button_sound)
                pygame.time.delay(300)
                if i != -1:
                    set_current_lock(i)
                    if i == 0:
                        tail_segments = []

        else:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))

        print_text(text, x + text_x, y + text_y)


play_button = Button(400, 100)
results_button = Button(400, 100)
back_button = Button(100, 100)
exit_button = Button(400, 100)
player = Snake()
while True:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if current_lock == 0:
        print_text("Snake", 490, 100, font_color='white')
        play_button.draw(400, 235, 110, 15, "Play", 1)
        results_button.draw(400, 385, 50, 15, "Results", 2)
        exit_button.draw(400, 535, 110, 15, "Exit", 3)
        player = Snake()
        Score = 0
        excel_data_df = pd.read_excel('results.xlsx')
        DateTime = excel_data_df['DateTime'].tolist()
        Game_Results = excel_data_df['Result'].tolist()
    elif current_lock == 1:
        # game
        print_text("Game", 510, 100, font_color='white')
        back_button.draw(80, 80, 25, 15, "<", 0)
        pygame.draw.rect(screen, 'white', pygame.Rect(200, 230, 800, 500), 2)
        print_text(str(Score), 1000, 100, font_color='white')
        for segment in tail_segments:
            segment.draw()
        player.draw()
        apple.draw()
    elif current_lock == 2:
        # results
        print_text("Results", 450, 100, font_color='white')
        back_button.draw(80, 80, 25, 15, "<", 0)
        player = Snake()
        Score = 0
    elif current_lock == 3:
        # exit
        pygame.quit()
        sys.exit()
    elif current_lock == 4:
        # game over
        print_text("Game Over!", 350, 100, font_color='white')
        back_button.draw(80, 80, 25, 15, "<", 0)
        print_text(str(Last_Score), 600, 400, font_color='white')
        Score = 0
        player = Snake()
    pygame.display.flip()
