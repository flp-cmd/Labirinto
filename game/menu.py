import pygame
import sys
import constants as c


class Menu:
    def __init__(self):
        pygame.init()
        self.screen_size = (c.SCREEN_WIDTH, c.SCREEN_HEIGHT)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 40)
        self.input_width = ""
        self.input_height = ""
        self.input_width_rect = pygame.Rect(0, 0, 200, 50)
        self.input_height_rect = pygame.Rect(0, 0, 200, 50)
        self.start_button = pygame.Rect(0, 0, 300, 70)
        self.running = True
        self.active_input = None

    def draw(self):
        self.screen.fill(c.WHITE)

        # Posicionamento centralizado
        label_width = self.font.render("Tamanho X do tabuleiro:", True, c.BLACK)
        label_height = self.font.render("Tamanho Y do tabuleiro:", True, c.BLACK)
        input_width_text = self.font.render(self.input_width, True, c.BLACK)
        input_height_text = self.font.render(self.input_height, True, c.BLACK)
        label_width_rect = label_width.get_rect(midright=(self.screen_size[0] // 2 - 10, self.screen_size[1] // 2))
        label_height_rect = label_height.get_rect(midright=(self.screen_size[0] // 2 - 10, self.screen_size[1] // 2 + 60))
        input_width_rect = input_width_text.get_rect(midleft=(self.screen_size[0] // 2 + 10, self.screen_size[1] // 2 + 30))
        input_height_rect = input_height_text.get_rect(midleft=(self.screen_size[0] // 2 + 10, self.screen_size[1] // 2 + 90))
        self.screen.blit(label_width, label_width_rect)
        self.screen.blit(label_height, label_height_rect)
        self.screen.blit(input_width_text, input_width_rect)
        self.screen.blit(input_height_text, input_height_rect)

        # Desenhar retângulos dos inputs
        self.input_width_rect.center = input_width_rect.center
        self.input_height_rect.center = input_height_rect.center
        pygame.draw.rect(self.screen, c.BLACK, self.input_width_rect, 2)
        pygame.draw.rect(self.screen, c.BLACK, self.input_height_rect, 2)

        # Posicionamento do botão
        self.start_button.center = (self.screen_size[0] // 2, self.screen_size[1] // 2 + 180)

        pygame.draw.rect(self.screen, c.BLACK, self.start_button)
        label_start = self.font.render("Start", True, c.WHITE)
        label_start_rect = label_start.get_rect(center=self.start_button.center)
        self.screen.blit(label_start, label_start_rect)

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos
                    if self.start_button.collidepoint(mouse_pos):
                        if self.input_width and self.input_height:
                            print("Start game with board size: {} x {}".format(self.input_width, self.input_height))
                    elif self.input_width_rect.collidepoint(mouse_pos):
                        self.active_input = self.input_width_rect
                    elif self.input_height_rect.collidepoint(mouse_pos):
                        self.active_input = self.input_height_rect
                    else:
                        self.active_input = None
            elif event.type == pygame.KEYDOWN:
                if self.active_input is not None:
                    if event.key == pygame.K_BACKSPACE:
                        if self.active_input == self.input_width_rect:
                            self.input_width = self.input_width[:-1]
                        elif self.active_input == self.input_height_rect:
                            self.input_height = self.input_height[:-1]
                    elif event.key == pygame.K_RETURN:
                        if self.input_width and self.input_height:
                            print("Start game with board size: {} x {}".format(self.input_width, self.input_height))
                    else:
                        if self.active_input == self.input_width_rect:
                            self.input_width += event.unicode
                        elif self.active_input == self.input_height_rect:
                            self.input_height += event.unicode

    def run_menu(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    menu = Menu()
    menu.run_menu()
