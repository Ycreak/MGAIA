import pygame
from pygame.locals import *
import pandas as pd
import random


####################################
# PRINTING & HANDLING OF QUESTIONS #
####################################
def _render_questions(state, top_position):
    top_x = top_position[0][0]
    top_y = top_position[1][0]
    box_width = top_position[2][0]
    box_height = top_position[2][1]

    v_fill = 10

    for topic, question, answer, penalty in state.questions_answers_displayed:
        text = "--".join([question, answer])
        q = state.questionfont.render(
            question, True, state.colors["questiontext"])

        if state.status == "buy_answer":
            # TODO print score/price of answer
            a = state.questionfont.render(
            str(penalty), True, state.colors["answertext"])
        else: 
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
