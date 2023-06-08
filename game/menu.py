import pygame
import sys
import constants as c
from Game import Game# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


class Menu:
    def __init__(self):
        pygame.init()
        self.screen_size = (c.SCREEN_WIDTH, c.SCREEN_HEIGHT)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Labirinto - Menu")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 40)
        self.input_x_rect = pygame.Rect(0, 0, 300, 50)
        self.input_y_rect = pygame.Rect(0, 0, 300, 50)
        self.start_button = pygame.Rect(0, 0, 300, 70)
        self.input_str_x = ""
        self.input_str_y = ""
        self.running = True
        self.active_input = "x"

    def draw(self):
        # Definindo imagem de fundo
        background_img = pygame.image.load("assets/img/menu_background (4).jpg")
        screen_size = self.screen.get_size()
        background_img_scaled = pygame.transform.scale(background_img, screen_size)
        self.screen.blit(background_img_scaled, (0, 0))

        # Centralizando labels e inputs
        label_x = self.font.render("Tamanho X do tabuleiro:", True, BLACK)
        label_y = self.font.render("Tamanho Y do tabuleiro:", True, BLACK)
        input_x_text = self.font.render(self.input_str_x, True, BLACK)
        input_y_text = self.font.render(self.input_str_y, True, BLACK)
        label_x_rect = label_x.get_rect(midright=(self.screen_size[0] // 2, self.screen_size[1] // 2))
        label_y_rect = label_y.get_rect(midright=(self.screen_size[0] // 2, self.screen_size[1] // 2 - 80))
        input_x_rect = input_x_text.get_rect(midleft=(self.screen_size[0] // 2 + 40, self.screen_size[1] // 2))
        input_y_rect = input_y_text.get_rect(midleft=(self.screen_size[0] // 2 + 40, self.screen_size[1] // 2 - 80))

        # Posicionando o botão
        self.start_button.center = (self.screen_size[0] // 2, self.screen_size[1] // 2 + 100)

        # Destacar campo de entrada ativo
        if self.active_input == "x":
            pygame.draw.rect(self.screen, RED, self.input_x_rect, 2)
        else:
            pygame.draw.rect(self.screen, BLACK, self.input_x_rect, 2)
        if self.active_input == "y":
            pygame.draw.rect(self.screen, RED, self.input_y_rect, 2)
        else:
            pygame.draw.rect(self.screen, BLACK, self.input_y_rect, 2)

        # Desenhar texto
        self.screen.blit(label_x, label_x_rect)
        self.screen.blit(label_y, label_y_rect)
        self.screen.blit(input_x_text, input_x_rect)
        self.screen.blit(input_y_text, input_y_rect)

        # Atualizar coordenadas iniciais dos retângulos de desenho
        self.input_x_rect.topleft = input_x_rect.topleft
        self.input_y_rect.topleft = input_y_rect.topleft

        pygame.draw.rect(self.screen, BLACK, self.start_button)
        label_start = self.font.render("Iniciar", True, WHITE)
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
                    if self.input_x_rect.collidepoint(mouse_pos):
                        self.active_input = "x"
                    elif self.input_y_rect.collidepoint(mouse_pos):
                        self.active_input = "y"
                    elif self.start_button.collidepoint(mouse_pos):  # Check if the mouse clicked on the "Start" button.
                        self.start_game()
                    else:
                        self.active_input = None
            elif event.type == pygame.KEYDOWN:
                if self.active_input == "x":
                    if event.key == pygame.K_BACKSPACE:
                        self.input_str_x = self.input_str_x[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.active_input = "y"
                    else:
                        if event.unicode.isnumeric() and len(self.input_str_x) < 3:
                            self.input_str_x += event.unicode
                elif self.active_input == "y":
                    if event.key == pygame.K_BACKSPACE:
                        self.input_str_y = self.input_str_y[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.start_game()
                    else:
                        if event.unicode.isnumeric() and len(self.input_str_y) < 3:
                            self.input_str_y += event.unicode

    def start_game(self):
        if self.input_str_x and self.input_str_y:
            print("Start game with board size: {} x {}".format(self.input_str_x, self.input_str_y))
            game = Game(int(self.input_str_x), int(self.input_str_y))
            game.run_game()


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
