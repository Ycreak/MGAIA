import pygame
from pygame.locals import *


class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 640, 400
        self.colors = {"color_light": (
            170, 170, 170), "color_dark": (100, 100, 100)}
        self.smallfont = pygame.font.SysFont('Corbel', 35)
        self.user_text = ''
        self.color_active =  pygame.Color('lightskyblue3') 
        self.color_passive = pygame.Color('chartreuse4')
        self.color = color_passive
        self.active = False
        self.mouse = pygame.mouse.get_pos()
        # x_left, x_right, y_top, y_bottom, width, height
        self.positions = {"quit_button": [[5, 145], [5, 45], [140, 40]]}

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(
            self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
            pygame.quit()

        # quit button
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.positions["quit_button"][0][0] <= self.mouse[0] <= self.positions["quit_button"][0][1] and self.positions["quit_button"][1][0] <= self.mouse[1] <= self.positions["quit_button"][1][1]:
                self._running = False
                pytame.quit()

    def on_loop(self):
        pass

    def render_button(self, position_list, text, hover_color, color):
        if position_list[0][0] <= self.mouse[0] <= position_list[0][1] \
                and position_list[1][0] <= self.mouse[1] <= position_list[1][1]:
            pygame.draw.rect(self.display_surf, hover_color,
                             [position_list[0][0], position_list[1][0], position_list[2][0], position_list[2][1]])
        # no hover
        else:
            pygame.draw.rect(self.display_surf, color,
                             [position_list[0][0], position_list[1][0], position_list[2][0], position_list[2][1]])

        # superimposing the text onto our button
        self.display_surf.blit(text, (position_list[0][0], height/2))

    def on_render(self):

        # quit button
        # hover
        if self.positions["quit_button"][0][0] <= self.mouse[0] <= self.positions["quit_button"][0][1] \
                and self.positions["quit_button"][1][0] <= self.mouse[1] <= self.positions["quit_button"][1][1]:
            pygame.draw.rect(self.display_surf, self.colors["color_light"],
                             [self.positions["quit_button"][0][0], self.positions["quit_button"][1][0], self.positions["quit_button"][2][0], self.positions["quit_button"][2][1]])
        # no hover
        else:
            pygame.draw.rect(self.display_surfs, self.colors["color_light"],
                             [self.positions["quit_button"][0][0], self.positions["quit_button"][1][0], self.positions["quit_button"][2][0], self.positions["quit_button"][2][1]])

        # superimposing the text onto our button
        screen.blit(text, (width/2+50, height/2))
        pass

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while(self._running):
            for event in pygame.event.get():
                self.on_event(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_rect.collidepoint(event.pos):
                        active = True
                    else:
                        active = False
                if event.type == pygame.KEYDOWN:
                    # Check for backspace
                    if event.key == pygame.K_BACKSPACE:
                        # get text input from 0 to -1 i.e. end.
                        user_text = user_text[:-1]
 
                    # Unicode standard is used for string
                    # formation
                    else:
                        user_text += event.unicode
                if active:
                    color = color_active
                else:
                    color = color_passive
                # draw rectangle and argument passed which should
                # be on screen
                pygame.draw.rect(self.display_surf, color, input_rect)
                text_surface = base_font.render(user_text, True, (255, 255, 255))
                # render at position stated in arguments
                screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))
      
                # set width of textfield so that text cannot get
                # outside of user's text input
                input_rect.w = max(100, text_surface.get_width()+10)
      
                # display.flip() will update only a portion of the
                # screen to updated, not full area
                pygame.display.flip()     
               
            self.mouse = pygame.mouse.get_pos()
            self.on_loop()
            self.on_render()
        self.on_cleanup()

# HEADER


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
