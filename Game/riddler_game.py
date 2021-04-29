import pygame
from pygame.locals import *


class App:
    def __init__(self):
        self._running = True
        self.display_surf = None
        self.size = self.weight, self.height = 640, 400
        self.colors = {"color_light": (
            170, 170, 170), "color_dark": (100, 100, 100)}


        self.colors = {"bg_color": (60, 25, 60), "color_light": (
            170, 170, 170), "color_dark": (100, 100, 100), "buttontext": (255, 255, 255)}

        # x_left, x_right, y_top, y_bottom, width, height
        self.positions = {"quit_button": [[5, 145], [5, 45], [140, 40]]}

    def on_init(self):
        print("init")
        pygame.init()
        self.smallfont = pygame.font.SysFont('Corbel', 35)
        self.display_surf = pygame.display.set_mode(
            self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.smallfont = pygame.font.SysFont('Corbel', 35)
        self.mouse = pygame.mouse.get_pos()
        self.mouse = pygame.mouse.get_pos()
        self._running = True
        return True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
            pygame.quit()

        # quit button
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.positions["quit_button"][0][0] <= self.mouse[0] <= self.positions["quit_button"][0][1] and self.positions["quit_button"][1][0] <= self.mouse[1] <= self.positions["quit_button"][1][1]:
                self._running = False
                pygame.quit()

    def on_loop(self):
        pass

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
            button_text, (position_list[0][0]+text_offset, position_list[1][0]))

    def on_render(self):
        self.display_surf.fill(self.colors["bg_color"])
        # quit button
        self.render_button(self.positions["quit_button"], "EXIT", self.smallfont, self.colors["buttontext"], 50,
                           self.colors["color_light"], self.colors["color_dark"])
        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        print("line 0")
        self.on_init()
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
    print("test")
    theApp.on_execute()
