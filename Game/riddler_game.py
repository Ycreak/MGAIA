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
            self.mouse = pygame.mouse.get_pos()
            self.on_loop()
            self.on_render()
        self.on_cleanup()

# HEADER


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
