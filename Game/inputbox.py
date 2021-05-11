import pygame


class InputBox():

    def __init__(self, pos, COLOR_INACTIVE, COLOR_ACTIVE, FONT, text=''):
        self.x = pos[0][0]
        self.y = pos[1][0]
        self.w = pos[2][0]
        self.h = pos[2][1]
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.color = COLOR_INACTIVE
        self.bg_color = (100, 100, 100)
        self.inactivecolor = COLOR_INACTIVE
        self.activecolor = COLOR_ACTIVE
        self.font = FONT
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.activecolor if self.active else self.inactivecolor
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                    self.txt_surface = self.font.render(
                        self.text, True, self.color)
                    return self.text
                # Re-render the text.
                self.txt_surface = self.font.render(
                    self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(self.w, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect)

        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
