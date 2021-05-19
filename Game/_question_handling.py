import pygame
from pygame.locals import *
import pandas as pd
import random


####################################
# PRINTING & HANDLING OF QUESTIONS #
####################################

def _answer_buying_event_handler(state, top_position):
    """Event handler used for handling clicks when buying answers: checks on which q&a card the user has clicked,
    if any. Returns the index of the q&a selected, the price and whether the answer has already been bought. 
    If the user did not click on a q&a card, -1 for all 3 is returned. """
    top_x = top_position[0][0]
    top_y = top_position[1][0]
    box_width = top_position[2][0]
    box_height = top_position[2][1]
    already_bought = -1
    v_fill = 10

    for box_id in range(len(state.questions_answers_displayed)):
        if top_x <= state.mouse[0] <= top_x+box_width and\
                top_y <= state.mouse[1] <= box_height+top_y:
            price = state.questions_answers_displayed[box_id][3]
            if state.questions_answers_displayed[box_id][2] != '':
                already_bougth = True
            else:
                already_bought = False
            if price <= state.score:
                return box_id, price, already_bought

        top_y += v_fill + box_height
    return -1, -1, -1


def _buy_answer(state):
    """ handler called when player enters answer buying screen. Checks whether the user has clicked on a q&a card,
    and shows the answer if the chosen q&a card is a valid purchase"""
    answer_id, price, question_already_bought = _answer_buying_event_handler(
        state, state.positions["questions"])
    price = 1
    if answer_id != -1:
        if not question_already_bought:
            # bought a question
            state.score -= price
            state.questions_answers_displayed[answer_id][2] = state.answers_displayed_questions[answer_id]
            state.question_status = "default"


def _render_questions(state, top_position):
    """ Renders the q&a boxes, displaying the questions and answers that have been bought. In the answer buying menu,
    the colors of the cards will be adjusted based on whether the answer of the card can be bought: green if the answer
    is available for purchase (i.e. is not already bought and player has enough score points), red if it cannot be bought """
    top_x = top_position[0][0]
    top_y = top_position[1][0]
    box_width = top_position[2][0]
    box_height = top_position[2][1]

    v_fill = 10

    for topic, question, answer, penalty in state.questions_answers_displayed:
        text = "--".join([question, answer])
        q = state.questionfont.render(
            question, True, state.colors["questiontext"])

        if state.buying_answer:  # if we are in the 'buy answer' mode

            if answer != '':  # this has to be: if question is already bought
                # +str(penalty), True, state.colors["answertext"])
                a = state.questionfont.render(
                    answer, True, state.colors["answertext"])
                qa_rectangle = pygame.draw.rect(
                    state.display_surf, state.colors["red"], [top_x, top_y, box_width, box_height], border_radius=5)
                a_rectangle = a.get_rect()
                a_rectangle.right = top_position[0][1]-5
                a_rectangle.top = top_y+2
                state.display_surf.blit(q, (top_x+5, top_y+2))
                state.display_surf.blit(a, a_rectangle)

            # player has not bought this question and he can buy it because score is high enough
            elif answer == '' and state.score > 1:
                a = state.questionfont.render(
                    "PRICE = 1", True, state.colors["answertext"])
                qa_rectangle = pygame.draw.rect(
                    state.display_surf, state.colors["green"], [top_x, top_y, box_width, box_height], border_radius=5)
                a_rectangle = a.get_rect()
                a_rectangle.right = top_position[0][1]-5
                a_rectangle.top = top_y+2
                state.display_surf.blit(q, (top_x+5, top_y+2))
                state.display_surf.blit(a, a_rectangle)

            else:  # answer is not bought yet but player has no money
                a = state.questionfont.render(
                    "PRICE = 1", True, state.colors["answertext"])
                qa_rectangle = pygame.draw.rect(
                    state.display_surf, state.colors["red"], [top_x, top_y, box_width, box_height], border_radius=5)
                a_rectangle = a.get_rect()
                a_rectangle.right = top_position[0][1]-5
                a_rectangle.top = top_y+2
                state.display_surf.blit(q, (top_x+5, top_y+2))
                state.display_surf.blit(a, a_rectangle)

        else:  # if we are just looking at the questions and answers
            a = state.questionfont.render(
                answer, True, state.colors["answertext"])
            qa_rectangle = pygame.draw.rect(
                state.display_surf, state.colors["qabox"], [top_x, top_y, box_width, box_height], border_radius=5)
            a_rectangle = a.get_rect()
            a_rectangle.right = top_position[0][1]-5
            a_rectangle.top = top_y+2
            state.display_surf.blit(q, (top_x+5, top_y+2))
            state.display_surf.blit(a, a_rectangle)

        top_y += v_fill + box_height


def _no_more_questions_handler(state):
    """ Handler for when there are no more questions left: shows a popup in the screen notifying the user 
    that no more questions can be displayed. The popup disappears if the player decides to buy an answer"""
    warning = state.bigfont.render(
        "NO MORE QUESTIONS LEFT", True, state.colors["warningtext"])
    warning_rectangle = warning.get_rect()
    warning_rectangle.width = 800
    warning_rectangle.height = 200
    warning_rectangle.center = (state.width/2, state.height/2)
    warning_border = pygame.Rect(0, 0, 750, 150)
    warning_border.center = warning_rectangle.center
    pygame.draw.rect(state.display_surf,
                     state.colors["warningbox"], warning_rectangle)
    pygame.draw.rect(state.display_surf,
                     state.colors["warningtext"], warning_border, 4)
    state.display_surf.blit(warning, warning.get_rect(
        center=(state.width/2, state.height/2)))


def _add_question(state):
    """ buy/add a question: a question is selected from the question database and is
    rendered on the screen """
    # check how many questions there are
    if len(state.questions_answers_database.index) == 0:
        state.no_more_questions = True
        return
    else:
        idx = random.randint(
            0, len(state.questions_answers_database.index)-1)
        q_and_a = state.questions_answers_database.iloc[0].tolist()

        # add question to displayed, empty string for answer until bought
        state.questions_answers_displayed.append(
            q_and_a[:2]+[""]+[q_and_a[3]])  # Always pick the top question
        state.answers_displayed_questions.append(q_and_a[2])

        state.questions_answers_database.drop(
            [state.questions_answers_database.index[0]], inplace=True)
        state.score = state.score - 1


def _player_won_handler(state):
    """ Handler called when the player has guessed the correct topic. 
    Displays popup indicating victory and shows the correct answer. Everything is hidden
    except the exit and menu buttons and the score. Player can go to the menu to restart game. """

    hide_background = pygame.Rect(0, 55, state.width, state.height-55)
    pygame.draw.rect(state.display_surf,
                     state.colors["bg_color"], hide_background)
    text = "VICTORY: " + state.game_answer.upper()
    victory = state.bigfont.render(
        text, True, state.colors["victorytext"])
    victory_rectangle = victory.get_rect()
    victory_rectangle.width = 800
    victory_rectangle.height = 200
    victory_rectangle.center = (state.width/2, state.height/2)
    victory_border = pygame.Rect(0, 0, 750, 150)
    victory_border.center = victory_rectangle.center
    pygame.draw.rect(state.display_surf,
                     state.colors["victorybox"], victory_rectangle)
    pygame.draw.rect(state.display_surf,
                     state.colors["victorytext"], victory_border, 4)
    state.display_surf.blit(victory, victory.get_rect(
        center=(state.width/2, state.height/2)))


def _give_up_handler(state):
    """ Renders the popup message for when a player decides to give up.
    The correct answer will be shown on screen. Everything is hidden
    except the exit and menu buttons and the score. Player can go to the menu to restart game. """

    hide_background = pygame.Rect(0, 55, state.width, state.height-55)
    pygame.draw.rect(state.display_surf,
                     state.colors["bg_color"], hide_background)

    answer_1 = state.bigfont.render(
        "YOU LOST! ANSWER WAS: ", True, state.colors["warningtext"])
    answer_2 = state.bigfont.render(
        state.game_answer.upper(), True, state.colors["warningtext"])
    answer_rectangle = answer_1.get_rect()
    answer_rectangle.width = 900
    answer_rectangle.height = 400
    answer_rectangle.center = (state.width/2, state.height/2)
    answer_border = pygame.Rect(0, 0, 850, 350)
    answer_border.center = answer_rectangle.center
    pygame.draw.rect(state.display_surf,
                     state.colors["warningbox"], answer_rectangle)
    pygame.draw.rect(state.display_surf,
                     state.colors["warningtext"], answer_border, 4)
    state.display_surf.blit(answer_1, answer_1.get_rect(
        center=(state.width/2, state.height/2-40)))
    state.display_surf.blit(answer_2, answer_2.get_rect(
        center=(state.width/2, state.height/2+40)))
