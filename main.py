import pygame
import sys

from pygame import display

pygame.init()

button_sound = pygame.mixer.Sound('button.wav')
current_lock = 0

screen = pygame.display.set_mode((1200, 800))


def set_current_lock(a: int):
    global current_lock
    current_lock = a


def print_text(message: str, x: int, y: int, font_color='black', font_type='pixelfont.ttf', font_size=80):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


class Button:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.inactive_color = (13, 162, 58)
        self.active_color = (23, 204, 58)

    def draw(self, x: int, y: int, text_x: int, text_y: int, text: str, i=-1):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))
            if click[0] == 1:
                pygame.mixer.Sound.play(button_sound)
                pygame.time.delay(300)
                if i != -1:
                    set_current_lock(i)

        else:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))

        print_text(text, x + text_x, y + text_y)


play_button = Button(400, 100)
results_button = Button(400, 100)
back_button = Button(100, 100)
exit_button = Button(400, 100)
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
    elif current_lock == 1:
        # game
        print_text("Game", 510, 100, font_color='white')
        back_button.draw(80, 80, 25, 15, "<", 0)
    elif current_lock == 2:
        # results
        print_text("Results", 450, 100, font_color='white')
        back_button.draw(80, 80, 25, 15, "<", 0)
    elif current_lock == 3:
        # exit
        pygame.quit()
        sys.exit()
    pygame.display.flip()
