import pygame
from pygame.locals import *
from inputbox import InputBox
import pandas as pd
import random
import subprocess
import os
import math
import wikipedia
import requests
import json
import urllib.parse

from answer_validation import answerIsValid



# TODO resetting game when going to menu?
# TODO: reset game when giving up?
# TODO: check answer (rem) (also, what part should be acceptable? [string comparison]) SEE ANSWER_VALIDATION
# TODO: find wikipedia URLs from a given topic (in the NLP code)
# TODO: handler for topic input box (i mean what to do with the input of the textbox)
# TODO: pressing enter for topic input maybe redundant?

class MySprite(pygame.sprite.Sprite):
    def __init__(self):
        super(MySprite, self).__init__()
        #adding all the images to sprite array
        self.images = self.load_images('img/riddler')
        
        #index value to get the image from the array
        #initially it is 0 
        self.index = 0

        #now the image that we will display will be the index from the image array 
        self.image = self.images[math.floor(self.index)]

        #creating a rect at position x,y (5,5) of size (150,198) which is the size of sprite 
        self.rect = pygame.Rect(30, 440, 10, 10)

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

        self.menupage = False
        self.gamepage = True

        self.size = self.width, self.height = 1000, 700
        self.colors = {"bg_color": (60, 25, 60),
                       "color_light": (170, 170, 170),
                       "color_dark": (100, 100, 100),
                       "buttontext": (255, 255, 255),
                       "questiontext": (0, 0, 0),
                       "answertext": (60, 25, 60),
                       "qabox": (255, 255, 255),
                       "warningtext": (255, 255, 255),
                       "warningbox": (179, 58, 58),
                       "victorytext": (255, 255, 255),
                       "victorybox": (0, 183, 0),
                       "inputactive": pygame.Color('dodgerblue2'),
                       "inputinactive": pygame.Color('lightskyblue3')}
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

        self.my_sprite = MySprite()
        self.my_group = pygame.sprite.Group(self.my_sprite)

        self.topic_options = []

    def on_init(self):
        pygame.init()
        pygame.display.set_caption('Riddler Game')
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

        self.mouse = pygame.mouse.get_pos()

        self.no_more_questions = False
        self.questions_answers_database = pd.read_csv(self.csv_name, sep=',')
        self.game_answer = self.questions_answers_database['topic'].iloc[0]
        self.questions_answers_displayed = []

        self.score = 6
        # self.topic = 'Netherlands'

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
                self.on_render()
            # search button
            if self.positions["search_button"][0][0] <= self.mouse[0] <= self.positions["search_button"][0][1] and\
                    self.positions["search_button"][1][0] <= self.mouse[1] <= self.positions["search_button"][1][1]:
                print("Search button pressed")
                self.topic_options = self.find_topic_options(self.topic)
                print("Topics found: ", self.topic_options)
                self.on_render()
            # toppic_option_buttons
            for i in range(0, len(self.topic_options)):
                button_name = "topic_option_button" + str(i)
                if self.positions[button_name][0][0] <= self.mouse[0] <= self.positions[button_name][0][1] and\
                        self.positions[button_name][1][0] <= self.mouse[1] <= self.positions[button_name][1][1]:
                    chosen_topic = self.topic_options[i]

                    print("Topic ", chosen_topic, " button pressed. You chose wisely!")
                    self.subtopics = self.find_subtopics(chosen_topic)

                    print(self.subtopics)

                    random.shuffle(self.subtopics)

                    current_subtopic = self.subtopics.pop()

                    print("Selected subtopic: ", current_subtopic)
                    
                    subprocess.call(['python3', 'main.py', current_subtopic], cwd="NLP/")
                    # TODO: loading process or maybe a bar? Animation?

                    print('all done!')
                    self.on_render()

    def on_loop(self):
        pass

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

    def find_topic_options(self, topic):
        possible_options = wikipedia.search(topic)
        options = []

        for option in possible_options:
            #Lists are not very usefull
            if "List of " in option:
                continue

            #Disambiguation pages are useless
            if "disambiguation" in option:
                continue

            options.append(option)

        return options

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

    def find_subtopics(self, chosen_topic):
        #The max number of pages for a certain topic 
        number_of_pages = 10

        #Get the url from the topic
        chosen_topic_ = chosen_topic.replace(" ", "_")
        chosen_topic_ = urllib.parse.quote(chosen_topic_)
        chosen_topic_url = "https://en.wikipedia.org/wiki/" + chosen_topic_

        #Get the first alinea from the Wikipedia page
        topic_wiki_response = requests.get(chosen_topic_url)
        topic_wiki_text = topic_wiki_response.text
        topic_wiki_text_begin = topic_wiki_text.split('<div id="siteSub" class="noprint">From Wikipedia, the free encyclopedia</div>')[1]
        topic_wiki_text_end = topic_wiki_text_begin.split('id="toc"')[0]

        #Get the links from the text
        topic_wiki_links_begin = topic_wiki_text_end.split('<a href="/wiki/')

        linked_pages = []

        #Check for every link if it is usable
        for link in topic_wiki_links_begin:
            page_name_parts = link.split('"')

            page_name = page_name_parts[0]

            #No loops
            if page_name == chosen_topic:
                continue

            #Wikipedia main page
            if page_name == "Main_Page":
                continue

            #Lists are not very usefull
            if "List_of_" in page_name:
                continue

            #Disambiguation pages are useless
            if "disambiguation" in page_name:
                continue

            #Not a page but an paragraph on a page
            if "#" in page_name:
                continue

            #Some Wikipedia specific pages
            if "Wikipedia" in page_name:
                continue

            if "File:" in page_name:
                continue

            if "Special:" in page_name:
                continue
            
            if "Category:" in page_name:
                continue

            if "Help:" in page_name:
                continue

            if "Talk:" in page_name:
                continue

            if "Portal:" in page_name:
                continue

            #The first part before any link is not a page
            if "<div id=" in page_name:
                continue
            
            linked_pages.append(page_name)

        linked_pages_views = {}
        relevant_pages = {}

        #Get the pageviews for the linked pages
        for linked_page in linked_pages[:200]:

            linked_url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/" + linked_page + "/monthly/20210401/20210430"

            pageviews = requests.get(linked_url, headers={"User-Agent":"TopicBot"})
            pageviews_text = json.loads(pageviews.text)

            if "items" in pageviews_text:
                linked_pages_views[linked_page] = pageviews_text["items"][0]["views"]

        #Order the pages by view count
        linked_pages_views_ordered = sorted(linked_pages_views.items(), key=lambda x: x[1], reverse=True)

        index = 0
        relevant_links = []

        #We only need to check untill we have the amount of relevant pages we need
        while len(relevant_pages) < number_of_pages and index < len(linked_pages_views_ordered):
            linked_page = linked_pages_views_ordered[index]
            linked_url = "https://en.wikipedia.org/wiki/" + linked_page[0]
            
            #Get the first alinea from the Wikipedia page
            linked_response = requests.get(linked_url)
            linked_text = linked_response.text
            linked_begin = linked_text.split('<div id="siteSub" class="noprint">From Wikipedia, the free encyclopedia</div>')[1]
            linked_end = linked_begin.split('id="toc"')[0]

            #If the topic is named in the text the page is really relevant
            if chosen_topic_ in linked_end or chosen_topic in linked_end:
                relevant_pages[linked_page[0]] = linked_page[1]
                relevant_links.append(linked_url)

            index = index + 1

        return relevant_links

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
            self.my_group.update()
            self.my_group.draw(self.display_surf)


        if self.menupage:

            self.display_surf.fill(self.colors["bg_color"])

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
                               "Search", self.smallfont,
                               self.colors["buttontext"],
                               [25, 10],
                               self.colors["color_light"],
                               self.colors["color_dark"])

            # INPUT BOX
            self.topic_input_box.draw(self.display_surf)

            if len(self.topic_options) > 0:
                self.render_topic_options()

        # update display
        pygame.display.update()

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
