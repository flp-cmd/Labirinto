import pygame
import sys
import constants as c
from Game import Game

class Menu:
    def __init__(self):
        pygame.init()
        self.screen_size = (c.SCREEN_WIDTH, c.SCREEN_HEIGHT)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Labirinto - Menu")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 40)
        self.input_x = pygame.Rect(150, 350, 410, 50)
        self.input_y = pygame.Rect(150, 470, 410, 50)
        self.input_str_x = ""
        self.input_str_y = ""
        self.button_rect = pygame.Rect(250, 550, 200, 50)
        self.running = True
        self.active_input = "x"

    def draw(self):
        # Definindo imagem de fundo
        background_img = pygame.image.load("assets/img/menu_background.jpg")
        screen_size = self.screen.get_size()
        background_img_scaled = pygame.transform.scale(background_img, screen_size)
        self.screen.blit(background_img_scaled, (0, 0))

        # Cria os textos dos inputs e desenha na tela
        x_text = self.font.render("Escolha a dimensão do eixo X:", True, c.BLACK)
        self.screen.blit(x_text, (150, 310))
        y_text = self.font.render("Escolha a dimensão do eixo Y:", True, c.BLACK)
        self.screen.blit(y_text, (150, 435))

        # Cria as caixas de entrada e desenha na tela
        pygame.draw.rect(self.screen, c.BLACK, self.input_x, 2)
        pygame.draw.rect(self.screen, c.BLACK, self.input_y, 2)

        # Cria os textos das caixas de entrada e desenha na tela
        input_x_text = self.font.render(self.input_str_x, True, c.BLACK)
        self.screen.blit(input_x_text, (self.input_x.x + 15, self.input_x.y + 12))
        input_y_text = self.font.render(self.input_str_y, True, c.BLACK)
        self.screen.blit(input_y_text, (self.input_y.x + 15, self.input_y.y + 12))

        # Cria o botão "Iniciar" e desenha na tela
        pygame.draw.rect(self.screen, c.BLACK, self.button_rect)
        button_text = self.font.render("Iniciar", True, c.WHITE)
        self.screen.blit(button_text, (self.button_rect.x + 60, self.button_rect.y + 12))

        pygame.display.flip()

    # Define manipuladores para os inputs e para o botão
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos
                    if self.input_x.collidepoint(mouse_pos):
                        self.active_input = "x"
                    elif self.input_y.collidepoint(mouse_pos):
                        self.active_input = "y"
                    elif self.button_rect.collidepoint(mouse_pos):
                        self.start_game()
                    else:
                        self.active_input = None
            elif event.type == pygame.KEYDOWN:
                if self.active_input == "x":
                    # Remove espaços digitados
                    if event.key == pygame.K_BACKSPACE:
                        self.input_str_x = self.input_str_x[:-1]
                    # Ativa o próximo input caso ENTER seja pressionado
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
            print("Tabuleiro iniciado com dimensões {} x {}".format(self.input_str_x, self.input_str_y))
            game = Game(int(self.input_str_x), int(self.input_str_y))
            game.run_game()


    def run_menu(self):
        while self.running:
            self.handle_events()
            self.draw()
            # Taxa de atualzição definida em 60 frames por segundo
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    menu = Menu()
    menu.run_menu()
