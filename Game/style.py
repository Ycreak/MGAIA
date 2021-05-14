colors = {"bg_color": (92, 219, 148),  # (60, 25, 60),
          "color_light": (170, 170, 170),
          "color_dark": (5, 57, 107),  # Button
          "buttontext": (255, 255, 255),
          "questiontext": (0, 0, 0),
          "answertext": (60, 25, 60),
          "qabox": (255, 255, 255),
          "warningtext": (255, 255, 255),
          "warningbox": (179, 58, 58),
          "victorytext": (255, 255, 255),
          "victorybox": (0, 183, 0),
          "green": (124,252,0),
          "red": (255,0,0),
          # pygame.Color('dodgerblue2'),  # Text box
          "inputactive": (246, 134, 133),
          # pygame.Color('lightskyblue3')}
          "inputinactive": (246, 134, 133),
          }


def _positions(state):
    button_width = 200
    button_height = 40
    option_width = 600
    option_height = 40
    option_position_x = 60
    button_position_x = option_position_x + option_width + 10

    return {"quit_button": [[5, 145], [5, 45], [140, 40]],
            "questions": [[5, state.width-5], [55, 85], [state.width-10, 30]],
            "menu_button": [[150, 150+140], [5, 45], [140, 40]],
            "giveup_button": [[state.width-150, state.width-10], [state.height-20-32-40, state.height-20-32], [140, 40]],
            
            "search_button":        [[button_position_x,  button_position_x + button_width], [150, 150 + button_height], [button_width, button_height]],
            "play_button":          [[button_position_x,  button_position_x + button_width], [200, 200 + button_height], [button_width, button_height]],

            "topic_input_box":      [[option_position_x,  option_position_x + option_width], [150, 150 + button_height], [option_width, option_height]],
            "topic_option_button0": [[option_position_x,  option_position_x + option_width], [200, 200 + button_height], [option_width, option_height]],
            "topic_option_button1": [[option_position_x,  option_position_x + option_width], [250, 250 + button_height], [option_width, option_height]],
            "topic_option_button2": [[option_position_x,  option_position_x + option_width], [300, 300 + button_height], [option_width, option_height]],
            "topic_option_button3": [[option_position_x,  option_position_x + option_width], [350, 350 + button_height], [option_width, option_height]],
            "topic_option_button4": [[option_position_x,  option_position_x + option_width], [400, 400 + button_height], [option_width, option_height]],
            "topic_option_button5": [[option_position_x,  option_position_x + option_width], [450, 450 + button_height], [option_width, option_height]],
            "topic_option_button6": [[option_position_x,  option_position_x + option_width], [500, 500 + button_height], [option_width, option_height]],
            "topic_option_button7": [[option_position_x,  option_position_x + option_width], [550, 550 + button_height], [option_width, option_height]],
            "topic_option_button8": [[option_position_x,  option_position_x + option_width], [600, 600 + button_height], [option_width, option_height]],
            "topic_option_button9": [[option_position_x,  option_position_x + option_width], [650, 650 + button_height], [option_width, option_height]],

            "input_box": [[state.width-510, state.width-10], [state.height-10-32, state.height-10], [500, 32]],
            "question_button": [[10, 410], [state.height-20-32-50, state.height-20-32], [400, 50]],
            "answer_button": [[430, 830], [state.height-20-32-50, state.height-20-32], [400, 50]],
            "score": [[state.width-250, state.width-50], [5, 45], [140, 40]]
            }
