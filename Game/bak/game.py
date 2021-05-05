# import pygame module in this program
import pygame
import pandas as pd
# activate the pygame library .
# initiate pygame and give permission
# to use pygame's functionality.
pygame.init()

# assigning values to X and Y variable
X = 800
Y = 400

# define the RGB value
# for white colour
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (0,0,0)

df = pd.read_csv('../NLP/dataframe.csv', sep=',')

# print(df['question'].iloc[1])

# exit(0)

dialog = ('He who crosses this bridge must answer these questions three', df['question'].iloc[1])

font = pygame.font.Font('freesansbold.ttf', 14)
text = font.render('GeeksForGeeks', True, black, white)
# create a rectangular object for the
# text surface object
textRect = text.get_rect()
# set the center of the rectangular object.
# textRect.center = (0, Y / 2)
 
# create the display surface object
# of specific dimension..e(X, Y).
display_surface = pygame.display.set_mode((X, Y ))
  
# set the pygame window name
pygame.display.set_caption('The Riddler')
  
# create a surface object, image is drawn on it.
riddler_img = pygame.image.load('img/riddler.png')
computer_img = pygame.image.load('img/computer.png')
players_img = pygame.image.load('img/players.png')

dialog_key = 0

# TODO: list of responses, should select at random
dialog_incorrect = 'Nope! That is not correct!'
dialog_correct = 'Yes! Very good!'

dialog_response = ''

# infinite loop
while True :
  
    # completely fill the surface object
    # with white colour
    display_surface.fill(white)
  
    # copying the image surface object
    # to the display surface object at
    # (0, 0) coordinate.
    display_surface.blit(riddler_img, (20, 300))
    display_surface.blit(computer_img, (120, 300))
    display_surface.blit(players_img, (250, 300))

    display_surface.blit(font.render(dialog[dialog_key], True, black, white), (20, 280))
    display_surface.blit(font.render(dialog_response, True, black, white), (20, 250))

    # iterate over the list of Event objects
    # that was returned by pygame.event.get() method.
    # print(dialog_response)
    
    for event in pygame.event.get() :
  
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_BACKSPACE:
                # TODO: why cant i remove text?
                dialog_response = dialog_response[:-1]
                print(dialog_response)


            try:
                if event.key < 127:
                    dialog_response += chr(event.key)
            except:
                pass

            if event.key == pygame.K_RIGHT:
                
                # Check if answer is correct
                
                
                dialog_key += 1
  
            if event.key == pygame.K_RETURN:
                if dialog_response == 'druif':
                    pass

        # if event object type is QUIT
        # then quitting the pygame
        # and program both.
        if event.type == pygame.QUIT :
  
            # deactivates the pygame library
            pygame.quit()
  
            # quit the program.
            quit()
  
        # Draws the surface object to the screen.  
        pygame.display.update() 