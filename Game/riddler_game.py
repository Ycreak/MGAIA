import pygame
from pygame.locals import *

import pandas as pd
import random

# TODO add guess the answer quiz
# TODO add question button
# TODO check answer
# TODO handler when there are no more questions


class App:
    def __init__(self):
        self._running = True
        self.display_surf = None
        self.size = self.width, self.height = 1000, 700
        self.colors = {"bg_color": (60, 25, 60), "color_light": (
            170, 170, 170), "color_dark": (100, 100, 100), "buttontext": (255, 255, 255), "questiontext": (0, 0, 0), "answertext": (60, 25, 60), "qabox": (255, 255, 255), "inputactive": pygame.Color('dodgerblue2'), "inputinactive": pygame.Color('lightskyblue3')}
        # x_left, x_right, y_top, y_bottom, width, height
        self.positions = {"quit_button": [[5, 145], [5, 45], [140, 40]], "questions": [
            [5, self.width-5], [55, 85], [self.width-10, 30]]}
        self.csv_name = '../NLP/dataframe.csv'

    def on_init(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        input_font = pygame.font.Font(None, 32)
        input_box1 = InputBox(
            10, self.height-10-32, 500, 32, self.colors["inputinactive"], self.colors["inputactive"], input_font)
        #input_box2 = InputBox(100, 300, 140, 32, COLOR_INACTIVE, COLOR_ACTIVE, FONT)
        self.input_boxes = [input_box1]

        self.smallfont = pygame.font.SysFont('Corbel', 35)
        self.display_surf = pygame.display.set_mode(
            self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.smallfont = pygame.font.SysFont('Corbel', 35)
        self.questionfont = pygame.font.SysFont('Corbel', 25)
        self.mouse = pygame.mouse.get_pos()
        self.questions_answers_database = pd.read_csv(self.csv_name, sep=',')
        self.questions_answers_displayed = []
        self.add_question()
        self.add_question()
        self._running = True
        return True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
            pygame.quit()

        # quit button
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.positions["quit_button"][0][0] <= self.mouse[0] <= self.positions["quit_button"][0][1] and self.positions["quit_button"][1][0] <= self.mouse[1] <= self.positions["quit_button"][1][1]:
                self._running = False
                pygame.quit()

    def on_loop(self):
        pass

    def render_questions(self, top_position):
        top_x = top_position[0][0]
        top_y = top_position[1][0]
        box_width = top_position[2][0]
        box_height = top_position[2][1]

        v_fill = 10

        for question, answer, _ in self.questions_answers_displayed:
            text = "--".join([question, answer])
            q = self.questionfont.render(
                question, True, self.colors["questiontext"])

            a = self.questionfont.render(
                answer, True, self.colors["answertext"])
            qa_rectangle = pygame.draw.rect(
                self.display_surf, self.colors["qabox"], [top_x, top_y, box_width, box_height], border_radius=5)
            a_rectangle = a.get_rect()
            a_rectangle.right = top_position[0][1]-5
            a_rectangle.top = top_y+2
            self.display_surf.blit(q, (top_x+5, top_y+2))
            self.display_surf.blit(a, a_rectangle)

            top_y += v_fill + box_height

    def add_question(self):
        # check how many questions there are
        # if all questions displayed, give option to quit if you don't know the answer
        if len(self.questions_answers_database.index) == 0:
            pass
        else:
            idx = random.randint(
                0, len(self.questions_answers_database.index)-1)
            self.questions_answers_displayed.append(
                self.questions_answers_database.loc[idx].tolist())
            self.questions_answers_database.drop([idx])
        pass

    def render_button(self, position_list, text, font, textcolor, text_offset, hover_color, color):
        if position_list[0][0] <= self.mouse[0] <= position_list[0][1] \
                and position_list[1][0] <= self.mouse[1] <= position_list[1][1]:
            pygame.draw.rect(self.display_surf, hover_color,
                             [position_list[0][0], position_list[1][0], position_list[2][0], position_list[2][1]])
        # no hover
        else:
            pygame.draw.rect(self.display_surf, color,
                             [position_list[0][0], position_list[1][0], position_list[2][0], position_list[2][1]])

        # superimposing the text onto our button
        button_text = font.render(text, True, textcolor)
        self.display_surf.blit(
            button_text, (position_list[0][0]+text_offset[0], position_list[1][0]+text_offset[1]))

    def on_render(self):
        self.display_surf.fill(self.colors["bg_color"])
        # quit button
        self.render_button(self.positions["quit_button"], "EXIT", self.smallfont, self.colors["buttontext"], [45, 5],
                           self.colors["color_light"], self.colors["color_dark"])

        title = self.smallfont.render(
            "GUESS THE SUBJECT", True, self.colors["buttontext"])
        title_rectangle = title.get_rect(center=(self.width/2, 20))
        self.display_surf.blit(title, title_rectangle)

        self.render_questions(self.positions["questions"])
        for box in self.input_boxes:
            box.draw(self.display_surf)
        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while(self._running):
            for event in pygame.event.get():
                self.on_event(event)
                for box in self.input_boxes:
                    box.handle_event(event)

            for box in self.input_boxes:
                box.update()

            self.display_surf.fill((30, 30, 30))

            self.mouse = pygame.mouse.get_pos()
            self.on_loop()
            self.on_render()
        self.on_cleanup()


class InputBox():

    def __init__(self, x, y, w, h, COLOR_INACTIVE, COLOR_ACTIVE, FONT, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = COLOR_INACTIVE
        self.bg_color = (100, 100, 100)
        self.inactivecolor = COLOR_INACTIVE
        self.activecolor = COLOR_ACTIVE
        self.font = FONT
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.activecolor if self.active else self.inactivecolor
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(
                    self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(self.w, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect)

        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))

# HEADER


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
