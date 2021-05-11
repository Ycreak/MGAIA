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
          # pygame.Color('dodgerblue2'),  # Text box
          "inputactive": (246, 134, 133),
          # pygame.Color('lightskyblue3')}
          "inputinactive": (246, 134, 133),
          }


def _positions(state):
    return {"quit_button": [[5, 145], [5, 45], [140, 40]],
            "questions": [[5, state.width-5], [55, 85], [state.width-10, 30]],
            "menu_button": [[150, 150+140], [5, 45], [140, 40]],
            "giveup_button": [[state.width-150, state.width-10], [state.height-20-32-40, state.height-20-32], [140, 40]],
            "play_button": [[state.width-250, state.width-50], [state.height/3 - 50,  state.height/3 - 10], [200, 40]],
            "search_button": [[state.width-250, state.width-50], [state.height/3 - 100, state.height/3 - 60], [200, 40]],

            "topic_input_box":      [[state.width/2-440, state.width/2-240], [state.height/3 - 100, state.height/3 - 60],  [600, 40]],
            "topic_option_button0": [[state.width/2-440, state.width/2-240], [state.height/3 - 50,  state.height/3 - 10],  [600, 40]],
            "topic_option_button1": [[state.width/2-440, state.width/2-240], [state.height/3 - 0,   state.height/3 + 40],  [600, 40]],
            "topic_option_button2": [[state.width/2-440, state.width/2-240], [state.height/3 + 50,  state.height/3 + 90],  [600, 40]],
            "topic_option_button3": [[state.width/2-440, state.width/2-240], [state.height/3 + 100, state.height/3 + 140], [600, 40]],
            "topic_option_button4": [[state.width/2-440, state.width/2-240], [state.height/3 + 150, state.height/3 + 190], [600, 40]],
            "topic_option_button5": [[state.width/2-440, state.width/2-240], [state.height/3 + 200, state.height/3 + 240], [600, 40]],
            "topic_option_button6": [[state.width/2-440, state.width/2-240], [state.height/3 + 250, state.height/3 + 290], [600, 40]],
            "topic_option_button7": [[state.width/2-440, state.width/2-240], [state.height/3 + 300, state.height/3 + 340], [600, 40]],
            "topic_option_button8": [[state.width/2-440, state.width/2-240], [state.height/3 + 350, state.height/3 + 390], [600, 40]],
            "topic_option_button9": [[state.width/2-440, state.width/2-240], [state.height/3 + 400, state.height/3 + 440], [600, 40]],

            "input_box": [[state.width-510, state.width-10], [state.height-10-32, state.height-10], [500, 32]],
            "question_button": [[10, 410], [state.height-20-32-50, state.height-20-32], [400, 50]],
            "answer_button": [[430, 830], [state.height-20-32-50, state.height-20-32], [400, 50]],
            "score": [[state.width-250, state.width-50], [5, 45], [140, 40]]
            }
