import pygame
from pygame.locals import *
from inputbox import InputBox
import pandas as pd
import random
import subprocess
import os
import math

import threading

from answer_validation import answerIsValid
from NLP.question_generator import Question_Generator
import NLP.topic_finder as tf

# TODO resetting game when going to menu?
# TODO: reset game when giving up?
# TODO: check answer (rem) (also, what part should be acceptable? [string comparison]) SEE ANSWER_VALIDATION
# TODO: find wikipedia URLs from a given topic (in the NLP code)
# TODO: handler for topic input box (i mean what to do with the input of the textbox)
# TODO: pressing enter for topic input maybe redundant?

class MySprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y, w, h):
        super(MySprite, self).__init__()
        #adding all the images to sprite array
        self.images = self.load_images(image)
        
        #index value to get the image from the array
        #initially it is 0 
        self.index = 0

        #now the image that we will display will be the index from the image array 
        self.image = self.images[math.floor(self.index)]

        #creating a rect at position x,y (5,5) of size (150,198) which is the size of sprite 
        self.rect = pygame.Rect(x,y,w,h)

    def load_images(self, path):
        """
        Loads all images in directory. The directory must only contain images.

        Args:
            path: The relative or absolute path to the directory to load images from.

        Returns:
            List of images.
        """
        images = []
        temp_list = []
        for file_name in os.listdir(path):
            temp_list.append(file_name)

        temp_list = sorted(temp_list)

        for file_name in temp_list:
            image = pygame.image.load(path + os.sep + file_name)
            image = pygame.transform.scale(image, (120, 150))
            images.append(image)

        return images

    def update(self):
        #when the update method is called, we will increment the index
        self.index += 0.02

        #if the index is larger than the total images
        if self.index >= len(self.images):
            #we will make the index to 0 again
            self.index = 0
        
        #finally we will update the image that will be displayed
        self.image = self.images[math.floor(self.index)]


class App:
    def __init__(self):
        self._running = True
        self.display_surf = None

        self.menupage = True
        self.gamepage = False

        self.size = self.width, self.height = 1000, 700
        self.colors = {"bg_color": (92, 219, 148),#(60, 25, 60),
                       "color_light": (170, 170, 170),
                       "color_dark": (5, 57, 107), # Button
                       "buttontext": (255, 255, 255),
                       "questiontext": (0, 0, 0),
                       "answertext": (60, 25, 60),
                       "qabox": (255, 255, 255),
                       "warningtext": (255, 255, 255),
                       "warningbox": (179, 58, 58),
                       "victorytext": (255, 255, 255),
                       "victorybox": (0, 183, 0),
                       "inputactive": (246, 134, 133), # pygame.Color('dodgerblue2'),  # Text box
                       "inputinactive": (246, 134, 133),# pygame.Color('lightskyblue3')}
                       } 
        # x_left, x_right, y_top, y_bottom, width, height
        self.positions = {"quit_button": [[5, 145], [5, 45], [140, 40]],
                          "questions": [[5, self.width-5], [55, 85], [self.width-10, 30]],
                          "menu_button": [[150, 150+140], [5, 45], [140, 40]],
                          "giveup_button": [[self.width-150, self.width-10], [self.height-20-32-40, self.height-20-32], [140, 40]],
                          "play_button": [[self.width-250, self.width-50], [self.height/3 - 50,  self.height/3 - 10], [200, 40]],
                          "search_button": [[self.width-250, self.width-50], [self.height/3 - 100, self.height/3 - 60], [200, 40]],

                          "topic_input_box":      [[self.width/2-440, self.width/2-240], [self.height/3 - 100, self.height/3 - 60],  [600, 40]],
                          "topic_option_button0": [[self.width/2-440, self.width/2-240], [self.height/3 - 50,  self.height/3 - 10],  [600, 40]],
                          "topic_option_button1": [[self.width/2-440, self.width/2-240], [self.height/3 - 0,   self.height/3 + 40],  [600, 40]],
                          "topic_option_button2": [[self.width/2-440, self.width/2-240], [self.height/3 + 50,  self.height/3 + 90],  [600, 40]],
                          "topic_option_button3": [[self.width/2-440, self.width/2-240], [self.height/3 + 100, self.height/3 + 140], [600, 40]],
                          "topic_option_button4": [[self.width/2-440, self.width/2-240], [self.height/3 + 150, self.height/3 + 190], [600, 40]],
                          "topic_option_button5": [[self.width/2-440, self.width/2-240], [self.height/3 + 200, self.height/3 + 240], [600, 40]],
                          "topic_option_button6": [[self.width/2-440, self.width/2-240], [self.height/3 + 250, self.height/3 + 290], [600, 40]],
                          "topic_option_button7": [[self.width/2-440, self.width/2-240], [self.height/3 + 300, self.height/3 + 340], [600, 40]],
                          "topic_option_button8": [[self.width/2-440, self.width/2-240], [self.height/3 + 350, self.height/3 + 390], [600, 40]],
                          "topic_option_button9": [[self.width/2-440, self.width/2-240], [self.height/3 + 400, self.height/3 + 440], [600, 40]],

                          "input_box": [[self.width-510, self.width-10], [self.height-10-32, self.height-10], [500, 32]],
                          "question_button": [[10, 410], [self.height-20-32-50, self.height-20-32], [400, 50]],
                          "score": [[self.width-250, self.width-50], [5, 45], [140, 40]]
                          }

        self.csv_name = './NLP/dataframe.csv'

        self.sprite_riddler = MySprite('img/riddler', 30, 440, 10, 10)
        self.sprit_group_riddler = pygame.sprite.Group(self.sprite_riddler)

        self.sprite_menu_riddler = MySprite('img/riddler', 700, 525, 10, 10)
        self.sprit_group_menu_riddler = pygame.sprite.Group(self.sprite_menu_riddler)

        self.logo = pygame.image.load("img/icon.png")
        
        self.show_bubble = True
        self.img_bubble = pygame.image.load("img/bubble.png")
        
        self.topic_options = []

    def on_init(self):
        pygame.init()
        pygame.display.set_caption('Riddler Game')
        pygame.display.set_icon(self.logo)
        self.clock = pygame.time.Clock()

        input_font = pygame.font.Font(None, 32)
        self.answer_input_box = InputBox(self.positions["input_box"],
                                         self.colors["inputinactive"],
                                         self.colors["inputactive"],
                                         input_font)

        self.topic_input_box = InputBox(self.positions["topic_input_box"],
                                        self.colors["inputinactive"],
                                        self.colors["inputactive"],
                                        input_font)

        self.smallfont = pygame.font.SysFont('Corbel', 35)
        self.display_surf = pygame.display.set_mode(
            self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.smallfont = pygame.font.SysFont('Corbel', 35)
        self.questionfont = pygame.font.SysFont('Corbel', 25)
        self.bigfont = pygame.font.SysFont('Corbel', 70)

        self.tinyfont = pygame.font.SysFont('Corbel', 30)
        self.mousefont = pygame.font.SysFont('Corbel', 20)

        self.mouse = pygame.mouse.get_pos()

        self.no_more_questions = False
        self.questions_answers_database = pd.read_csv(self.csv_name, sep=',')
        self.game_answer = self.questions_answers_database['topic'].iloc[0]
        self.questions_answers_displayed = []

        self.score = 6
        self.topic = ''
        self.status = 'welcome'


        self.add_question()

        self.player_won = False
        self.given_up = False
        self._running = True
        return True

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

                self.add_question()
                self.on_render()
            if self.positions["menu_button"][0][0] <= self.mouse[0] <= self.positions["menu_button"][0][1] and self.positions["menu_button"][1][0] <= self.mouse[1] <= self.positions["menu_button"][1][1]:
                print('inside menu')
                self.gamepage = False
                self.menupage = True
                self.on_render()

            # giveup
            if self.positions["giveup_button"][0][0] <= self.mouse[0] <= self.positions["giveup_button"][0][1] and\
                    self.positions["giveup_button"][1][0] <= self.mouse[1] <= self.positions["giveup_button"][1][1]:
                self.given_up = True
                self.on_render()
            # play button
            if self.positions["play_button"][0][0] <= self.mouse[0] <= self.positions["play_button"][0][1] and\
                    self.positions["play_button"][1][0] <= self.mouse[1] <= self.positions["play_button"][1][1]:
                self.gamepage = True
                self.menupage = False
                self.questions_answers_database = pd.read_csv(self.csv_name, sep=',')

                self.on_render()
            # search button
            if self.positions["search_button"][0][0] <= self.mouse[0] <= self.positions["search_button"][0][1] and\
                    self.positions["search_button"][1][0] <= self.mouse[1] <= self.positions["search_button"][1][1]:
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
            for i in range(0, len(self.topic_options)):
                button_name = "topic_option_button" + str(i)
                if self.positions[button_name][0][0] <= self.mouse[0] <= self.positions[button_name][0][1] and\
                        self.positions[button_name][1][0] <= self.mouse[1] <= self.positions[button_name][1][1]:
                    chosen_topic = self.topic_options[i]

                    # We now pressed a topic. Find a related topic to ask questions about
                    print("Topic ", chosen_topic, " button pressed. You chose wisely!")
                    self.status = "topic_chosen"

                    self.subtopics = tf.find_subtopics(chosen_topic)

                    print(self.subtopics)

                    random.shuffle(self.subtopics)

                    current_subtopic = self.subtopics.pop()

                    print("Selected subtopic: ", current_subtopic)
                    
                    # TODO: Now everything is Python3, this can just be an import
                    self.quest_gen = subprocess.Popen(['python3', 'q2.py', current_subtopic], cwd="NLP/")

                    self.on_render()

    def on_loop(self):
        pass

    # def my_inline_function(self, current_subtopic):
    #     # do some stuff
    #     download_thread = threading.Thread(target=Question_Generator(current_subtopic), name="Downloader", args=current_subtopic)
    #     download_thread.start()

    ####################################
    # PRINTING & HANDLING OF QUESTIONS #
    ####################################
    def render_questions(self, top_position):
        top_x = top_position[0][0]
        top_y = top_position[1][0]
        box_width = top_position[2][0]
        box_height = top_position[2][1]

        v_fill = 10

        for topic, question, answer, penalty in self.questions_answers_displayed:
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

    def no_more_questions_handler(self):
        warning = self.bigfont.render(
            "NO MORE QUESTIONS LEFT", True, self.colors["warningtext"])
        warning_rectangle = warning.get_rect()
        warning_rectangle.width = 800
        warning_rectangle.height = 200
        warning_rectangle.center = (self.width/2, self.height/2)
        warning_border = pygame.Rect(0, 0, 750, 150)
        warning_border.center = warning_rectangle.center
        pygame.draw.rect(self.display_surf,
                         self.colors["warningbox"], warning_rectangle)
        pygame.draw.rect(self.display_surf,
                         self.colors["warningtext"], warning_border, 4)
        self.display_surf.blit(warning, warning.get_rect(
            center=(self.width/2, self.height/2)))

    def add_question(self):
        # check how many questions there are
        if len(self.questions_answers_database.index) == 0:
            self.no_more_questions = True
            return
        else:
            idx = random.randint(
                0, len(self.questions_answers_database.index)-1)
            self.questions_answers_displayed.append(
                self.questions_answers_database.iloc[0].tolist())  # Always pick the top question
            self.questions_answers_database.drop(
                [self.questions_answers_database.index[0]], inplace=True)
            self.score = self.score - 1

    def player_won_handler(self):
        text = "VICTORY: " + self.game_answer.upper()
        victory = self.bigfont.render(
            text, True, self.colors["victorytext"])
        victory_rectangle = victory.get_rect()
        victory_rectangle.width = 800
        victory_rectangle.height = 200
        victory_rectangle.center = (self.width/2, self.height/2)
        victory_border = pygame.Rect(0, 0, 750, 150)
        victory_border.center = victory_rectangle.center
        pygame.draw.rect(self.display_surf,
                         self.colors["victorybox"], victory_rectangle)
        pygame.draw.rect(self.display_surf,
                         self.colors["victorytext"], victory_border, 4)
        self.display_surf.blit(victory, victory.get_rect(
            center=(self.width/2, self.height/2)))

    def give_up_handler(self):
        answer_1 = self.bigfont.render(
            "YOU LOST! ANSWER WAS: ", True, self.colors["warningtext"])
        answer_2 = self.bigfont.render(
            self.game_answer.upper(), True, self.colors["warningtext"])
        answer_rectangle = answer_1.get_rect()
        answer_rectangle.width = 900
        answer_rectangle.height = 400
        answer_rectangle.center = (self.width/2, self.height/2)
        answer_border = pygame.Rect(0, 0, 850, 350)
        answer_border.center = answer_rectangle.center
        pygame.draw.rect(self.display_surf,
                         self.colors["warningbox"], answer_rectangle)
        pygame.draw.rect(self.display_surf,
                         self.colors["warningtext"], answer_border, 4)
        self.display_surf.blit(answer_1, answer_1.get_rect(
            center=(self.width/2, self.height/2-40)))
        self.display_surf.blit(answer_2, answer_2.get_rect(
            center=(self.width/2, self.height/2+40)))

    ###################################
    # SEARCHING AND DISPLAYING TOPICS #
    ###################################

    def render_topic_options(self):
        i = 0

        for option in self.topic_options:
            buttonpos = "topic_option_button" + str(i)

            if len(option) > 44:
                option = option[:45] + "..."

            self.render_button(self.positions[buttonpos],
                               option, 
                               self.smallfont,
                               self.colors["buttontext"],
                               [10, 10],
                               self.colors["color_light"],
                               self.colors["color_dark"])

            i = i + 1


    ######################
    # ANIMATION HANDLING #
    ######################

    #####################
    # GENERAL RENDERING #
    #####################

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
            # button play game
            self.render_button(self.positions["play_button"],
                               "PLAY GAME!", self.smallfont,
                               self.colors["buttontext"],
                               [25, 10],
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

                self.display_surf.blit(self.img_bubble, (775, 425))

                self.render_text(self.riddler_text_string1, 850, 470, self.colors["buttontext"])
                self.render_text(self.riddler_text_string2, 850, 490, self.colors["buttontext"])
            
        # update display
        pygame.display.update()

    def render_text(self, string, x, y, colour): #self.colors["buttontext"]
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
                # TODO handler for input of this box
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
