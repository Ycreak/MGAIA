import pygame
from pygame.locals import *
from inputbox import InputBox
import pandas as pd
import random
import subprocess
import os
import math

import threading

# class methods, moved to external files for clarity
import _question_handling

# colors, positions etc
import style

from answer_validation import answerIsValid
from NLP.question_generator import Question_Generator
from mysprite import MySprite

import NLP.topic_finder as tf


class App:
    def __init__(self):
        self._running = True
        self.display_surf = None

        self.menupage = True
        self.gamepage = False

        self.size = self.width, self.height = 1000, 700
        self.colors = style.colors

        # x_left, x_right, y_top, y_bottom, width, height
        self.positions = style._positions(self)

        self.csv_name = './NLP/dataframe.csv'

        self.sprite_riddler = MySprite('img/riddler', 30, 440, 10, 10)
        self.sprit_group_riddler = pygame.sprite.Group(self.sprite_riddler)

        self.sprite_menu_riddler = MySprite('img/riddler', 700, 525, 10, 10)
        self.sprit_group_menu_riddler = pygame.sprite.Group(
            self.sprite_menu_riddler)

        self.logo = pygame.image.load("img/icon.png")

        self.show_bubble = True
        self.img_bubble = pygame.image.load("img/bubble.png")

        self.topic_options = []
        self.small_options = []

    def on_init(self):
        pygame.init()
        pygame.display.set_caption('Riddler Game')
        pygame.display.set_icon(self.logo)

        # pygame internal state
        self.clock = pygame.time.Clock()
        self.mouse = pygame.mouse.get_pos()

        # fonts
        input_font = pygame.font.Font(None, 32)
        self.smallfont = pygame.font.SysFont('Corbel', 35)
        self.display_surf = pygame.display.set_mode(
            self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.smallfont = pygame.font.SysFont('Corbel', 35)
        self.questionfont = pygame.font.SysFont('Corbel', 25)
        self.bigfont = pygame.font.SysFont('Corbel', 70)
        self.tinyfont = pygame.font.SysFont('Corbel', 30)
        self.mousefont = pygame.font.SysFont('Corbel', 20)

        # input boxes
        self.answer_input_box = InputBox(self.positions["input_box"],
                                         self.colors["inputinactive"],
                                         self.colors["inputactive"],
                                         input_font)

        self.topic_input_box = InputBox(self.positions["topic_input_box"],
                                        self.colors["inputinactive"],
                                        self.colors["inputactive"],
                                        input_font)

        # q&a utility
        self.no_more_questions = False
        self.questions_answers_database = pd.read_csv(self.csv_name, sep=',')
        self.answers_displayed_questions = []
        self.game_answer = self.questions_answers_database['topic'].iloc[0]
        self.questions_answers_displayed = []

        # gamestate
        self.score = 20
        self.topic = ''
        self.status = 'welcome'
        self.question_status = "default"
        self.player_won = False
        self.given_up = False
        self._running = True

        self.add_question()

        return True

    def reload_question_database(self):
        self.questions_answers_database = pd.read_csv(
            self.csv_name, sep=',')

        self.answers_displayed_questions = []
        self.questions_answers_displayed = []
        self.game_answer = self.questions_answers_database['topic'].iloc[0]
        self.add_question()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
            pygame.quit()

        # quit button
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.positions["quit_button"][0][0] <= self.mouse[0] <= self.positions["quit_button"][0][1] and\
                    self.positions["quit_button"][1][0] <= self.mouse[1] <= self.positions["quit_button"][1][1]:
                self._running = False
                pygame.quit()
            if self.positions["question_button"][0][0] <= self.mouse[0] <= self.positions["question_button"][0][1] and\
                    self.positions["question_button"][1][0] <= self.mouse[1] <= self.positions["question_button"][1][1]:

                if self.score <= 0:
                    # TODO: how to handle this?
                    pass

                # only add question in default mode, not when buying answer
                if self.question_status == "default":
                    self.add_question()
                    self.on_render()

            # buy answer button
            if self.positions["answer_button"][0][0] <= self.mouse[0] <= self.positions["answer_button"][0][1] and\
                    self.positions["answer_button"][1][0] <= self.mouse[1] <= self.positions["answer_button"][1][1] and\
                    self.gamepage:

                # TODO buy question handler
                if self.question_status == "default":
                    self.question_status = "buy_answer"
                else:
                    self.question_status = "default"
                self.on_render()

            if self.question_status == "buy_answer":
                print("buying answer")
                _question_handling._buy_answer(self)
                self.on_render()

            if self.positions["menu_button"][0][0] <= self.mouse[0] <= self.positions["menu_button"][0][1] and\
                    self.positions["menu_button"][1][0] <= self.mouse[1] <= self.positions["menu_button"][1][1] and\
                    self.gamepage:
                print('inside menu')
                self.gamepage = False
                self.menupage = True
                self.on_render()

            # giveup
            if self.positions["giveup_button"][0][0] <= self.mouse[0] <= self.positions["giveup_button"][0][1] and\
                    self.positions["giveup_button"][1][0] <= self.mouse[1] <= self.positions["giveup_button"][1][1] and\
                    self.gamepage:
                self.given_up = True
                self.on_render()
            # play button
            if self.positions["play_button"][0][0] <= self.mouse[0] <= self.positions["play_button"][0][1] and\
                    self.positions["play_button"][1][0] <= self.mouse[1] <= self.positions["play_button"][1][1] and\
                    self.status == 'questions_generated' and\
                    self.menupage:
                self.gamepage = True
                self.menupage = False
                self.reload_question_database()

                self.on_render()
            # search button
            if self.positions["search_button"][0][0] <= self.mouse[0] <= self.positions["search_button"][0][1] and\
                    self.positions["search_button"][1][0] <= self.mouse[1] <= self.positions["search_button"][1][1] and\
                    self.menupage:
                print("Search button pressed")
                if self.topic == '':
                    print('No Topic selected, please press enter after typing')
                    self.status = 'press_enter'
                    # TODO: put this on screen, maybe grey out button if no topic has yet been entered?
                else:
                    self.status = 'searching_topic'
                    self.topic_options = tf.find_topic_options(self.topic)
                    print("Topics found: ", self.topic_options)

                    if self.topic_options == []:
                        self.status = "no_topics_found"

                self.on_render()
            # toppic_option_buttons
            if self.question_status == "default" and self.menupage:
                for i in range(0, len(self.topic_options)):
                    button_name = "topic_option_button" + str(i)
                    if self.positions[button_name][0][0] <= self.mouse[0] <= self.positions[button_name][0][1] and\
                            self.positions[button_name][1][0] <= self.mouse[1] <= self.positions[button_name][1][1] and\
                            self.topic_options[i] not in self.small_options:
                        chosen_topic = self.topic_options[i]

                        # We now pressed a topic. Find a related topic to ask questions about
                        print("Topic ", chosen_topic,
                              " button pressed.")

                        self.status = "topic_chosen"

                        self.subtopics = tf.find_subtopics(chosen_topic)

                        print(self.subtopics)

                        if len(self.subtopics) > 1:
                            print("Topic is large enough. You chose wisely!")

                            random.shuffle(self.subtopics)

                            current_subtopic = self.subtopics.pop()

                            print("Selected subtopic: ", current_subtopic)

                            # TODO: Now everything is Python3, this can just be an import
                            self.quest_gen = subprocess.Popen(
                                ['python3', 'q2.py', current_subtopic], cwd="NLP/")
                        else:
                            print("Topic is too small. You chose poorly!")
                            self.status = "searching_topic"
                            self.small_options.append(chosen_topic)
                        self.on_render()

    def on_loop(self):
        pass

    # ###################################
    # # SEARCHING AND DISPLAYING TOPICS #
    # ###################################
    # def find_topic_options(self, topic):
    #     return _search_topics._find_topic_options(self, topic)

    # def render_topic_options(self):
    #     _search_topics._render_topic_options(self)

    # def find_subtopics(self, chosen_topic):
    #     return _search_topics._find_subtopics(self, chosen_topic)

    ####################################
    # PRINTING & HANDLING OF QUESTIONS #
    ####################################
    def render_questions(self, top_position):
        _question_handling._render_questions(self, top_position)

    def no_more_questions_handler(self):
        _question_handling._no_more_questions_handler(self)

    def add_question(self):
        _question_handling._add_question(self)

    def player_won_handler(self):
        _question_handling._player_won_handler(self)

    def give_up_handler(self):
        _question_handling._give_up_handler(self)

    ######################
    # ANIMATION HANDLING #
    ######################

    #####################
    # GENERAL RENDERING #
    #####################

    def render_topic_options(self):
        i = 0

        for option in self.topic_options:

            color_light = "color_light"
            color_dark = "color_dark"
            name = option

            if option in self.small_options:
                color_light = "warningbox"
                color_dark = "warningbox"
                name = "This topic contains not enough subtopics."

            buttonpos = "topic_option_button" + str(i)

            if len(name) > 44:
                name = name[:45] + "..."

            self.render_button(self.positions[buttonpos],
                               name,
                               self.smallfont,
                               self.colors["buttontext"],
                               [10, 10],
                               self.colors[color_light],
                               self.colors[color_dark])

            i = i + 1

    def render_no_topic_found(self):
        self.render_button(self.positions["topic_option_button0"],
                           "No topics found. Try again with a different topic!",
                           self.smallfont,
                           self.colors["buttontext"],
                           [10, 10],
                           self.colors["warningbox"],
                           self.colors["warningbox"])


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
        if self.gamepage:
            # TITLE
            self.display_surf.fill(self.colors["bg_color"])
            title = self.smallfont.render(
                "GUESS THE SUBJECT", True, self.colors["buttontext"])
            title_rectangle = title.get_rect(center=(self.width/2, 20))
            self.display_surf.blit(title, title_rectangle)

            # BUTTONS
            # quit button
            self.render_button(self.positions["quit_button"],
                               "EXIT",
                               self.smallfont,
                               self.colors["buttontext"],
                               [40, 10],
                               self.colors["color_light"],
                               self.colors["color_dark"])
            # button menu
            self.render_button(self.positions["menu_button"],
                               "MENU", self.smallfont,
                               self.colors["buttontext"],
                               [40, 10],
                               self.colors["color_light"],
                               self.colors["color_dark"])
            # score TODO: should we show this in a button? quick hack
            self.render_button(self.positions["score"],
                               ("SCORE: "+str(self.score)), self.smallfont,
                               self.colors["buttontext"],
                               [40, 10],
                               self.colors["color_light"],
                               self.colors["color_dark"])

            # question button
            self.render_button(self.positions["question_button"],
                               "SHOW ANOTHER QUESTION",
                               self.smallfont,
                               self.colors["buttontext"],
                               [30, 15],
                               self.colors["color_light"],
                               self.colors["color_dark"])

            # buy answer button
            self.render_button(self.positions["answer_button"],
                               "BUY AN ANSWER",
                               self.smallfont,
                               self.colors["buttontext"],
                               [30, 15],
                               self.colors["color_light"],
                               self.colors["color_dark"])

            # Give up button
            self.render_button(self.positions["giveup_button"],
                               "GIVE UP", self.smallfont,
                               self.colors["buttontext"],
                               [20, 5],
                               self.colors["color_light"],
                               self.colors["color_dark"])

            # Q & A
            self.render_questions(self.positions["questions"])

            # INPUT BOX
            guess = self.smallfont.render(
                "GUESS THE SUBJECT:", True, self.colors["buttontext"])
            guess_rectangle = guess.get_rect()
            guess_rectangle.left = 100
            guess_rectangle.top = self.height-10-30
            self.display_surf.blit(guess, guess_rectangle)
            self.answer_input_box.draw(self.display_surf)

            # NO MORE QUESTIONS

            if self.no_more_questions:
                self.no_more_questions_handler()

            # VICTORY
            if self.player_won:
                self.player_won_handler()

            # GIVE UP
            if self.given_up:
                self.give_up_handler()

            # Animations
            self.sprit_group_riddler.update()
            self.sprit_group_riddler.draw(self.display_surf)

        if self.menupage:
            # TODO: this needs to be better
            # Check if the questions are generated
            try:
                poll = self.quest_gen.poll()
                if poll is not None:
                    self.status = 'questions_generated'
            except:
                # print('wrong')
                pass

            self.display_surf.fill(self.colors["bg_color"])

            title = self.bigfont.render(
                "THE RIDDLER GAME", True, self.colors["buttontext"])
            title_rectangle = title.get_rect(center=(self.width/2, 40))
            self.display_surf.blit(title, title_rectangle)

            subtext_string = "Type a topic in the search bar and press enter. Next, select one of the resulting Wikipedia Pages."
            subtext = self.tinyfont.render(
                subtext_string, True, self.colors["buttontext"])
            subtext_rectangle = subtext.get_rect(center=(self.width/2, 80))
            self.display_surf.blit(subtext, subtext_rectangle)

            subtext_string2 = "The Riddler will now find a related article and asks questions about it. Your task is to find its title!"
            subtext2 = self.tinyfont.render(
                subtext_string2, True, self.colors["buttontext"])
            subtext_rectangle2 = subtext2.get_rect(center=(self.width/2, 105))
            self.display_surf.blit(subtext2, subtext_rectangle2)

            # BUTTONS
            # exit button
            self.render_button(self.positions["quit_button"],
                               "EXIT", self.smallfont,
                               self.colors["buttontext"],
                               [40, 10],
                               self.colors["color_light"],
                               self.colors["color_dark"])
            
            # Topic button
            self.render_button(self.positions["search_button"],
                               "SEARCH", self.smallfont,
                               self.colors["buttontext"],
                               [25, 10],
                               self.colors["color_light"],
                               self.colors["color_dark"])

            # INPUT BOX
            self.topic_input_box.draw(self.display_surf)

            if len(self.topic_options) > 0:
                self.render_topic_options()
            if self.status == "no_topics_found":
                self.render_no_topic_found()

            # Draw the riddler
            self.sprit_group_menu_riddler.update()
            self.sprit_group_menu_riddler.draw(self.display_surf)

            # Draw its speech bubble
            if self.show_bubble:
                if self.status == 'welcome':

                    self.riddler_text_string1 = "Welcome!"
                    self.riddler_text_string2 = "Select a topic!"

                elif self.status == 'press_enter':
                    self.riddler_text_string1 = "Press enter in"
                    self.riddler_text_string2 = "that search bar!"

                elif self.status == 'topic_entered':
                    self.riddler_text_string1 = "OK, now press."
                    self.riddler_text_string2 = "the search button!"

                elif self.status == 'searching_topic':
                    self.riddler_text_string1 = "Select one of these"
                    self.riddler_text_string2 = "interesting topics!"

                elif self.status == 'topic_chosen':
                    self.riddler_text_string1 = "Let me think of"
                    self.riddler_text_string2 = "some questions!"

                elif self.status == 'no_topics_found':
                    self.riddler_text_string1 = "That's gibberish!"
                    self.riddler_text_string2 = "Try again!"

                elif self.status == 'questions_generated':
                    self.riddler_text_string1 = "I am ready!"
                    self.riddler_text_string2 = "Please press play."
                    # button play game
                    self.render_button(self.positions["play_button"],
                               "PLAY GAME!", self.smallfont,
                               self.colors["buttontext"],
                               [25, 10],
                               self.colors["color_light"],
                               self.colors["color_dark"])

                self.display_surf.blit(self.img_bubble, (775, 425))

                self.render_text(self.riddler_text_string1, 850,
                                 470, self.colors["buttontext"])
                self.render_text(self.riddler_text_string2, 850,
                                 490, self.colors["buttontext"])

        # update display
        pygame.display.update()

    def render_text(self, string, x, y, colour):  # self.colors["buttontext"]
        """Small function to render text on screen in pygame

        Args:
            string (string): text to be put on screen
            x (int): x coordinate
            y (int): y coordinate
            colour (dict entry): colour of the button/text
        """
        text = self.mousefont.render(
            string, True, colour)
        rect = text.get_rect(center=(x, y))
        self.display_surf.blit(text, rect)

        # return text, rect

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while(self._running):
            for event in pygame.event.get():
                self.on_event(event)

                # answer input box
                answer = self.answer_input_box.handle_event(event)
                if answer != None and answerIsValid(answer, self.game_answer):
                    self.player_won = True

                # topic input box
                topic_input = self.topic_input_box.handle_event(event)
                # print(topic_input)
                if topic_input != None:
                    print("topic input: ", topic_input)
                    self.topic = topic_input
                    self.status = "topic_entered"
            self.answer_input_box.update()
            self.topic_input_box.update()

            self.display_surf.fill((30, 30, 30))

            self.mouse = pygame.mouse.get_pos()
            self.on_loop()
            self.on_render()
        self.on_cleanup()


# HEADER


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
