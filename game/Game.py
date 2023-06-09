import pygame
from main import *
from constants import *
import sys


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)



class Game:
    def __init__(self, width, height):
        pygame.init()
        self.board_size = (width, height)
        self.board = [[0]*width for _ in range(height)]  # Create a 2D matrix of zeros
        self.screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.board_dimensions = (600, 600)  # Fixed board size
        self.cell_size_x = self.board_dimensions[0] // self.board_size[0]
        self.cell_size_y = self.board_dimensions[1] // self.board_size[1]
        self.margin_x = (self.screen_size[0] - self.board_dimensions[0]) // 2
        self.margin_y = (self.screen_size[1] - self.board_dimensions[1]) // 2
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Labirinto - Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 40)
        self.running = True
        self.background_img = pygame.image.load("fundo_jogo.png")
        self.horse_img = pygame.image.load("horse_face.png")
        self.fence_img = pygame.image.load("assets/img/fence.png")
        self.feno_img = pygame.image.load("assets/img/feno.png")
        self.pegada_img = pygame.image.load("assets/img/pegada.png")
        self.move_timer = 0
        self.path = []
        self.path_index = 0
        self.images = {
            2: self.horse_img,  # Horse image
            1: self.fence_img,  # Fence image
            3: self.feno_img,
            4: self.pegada_img
        }
        # Buttons
        self.admissivel = True

        self.buttons = {
            "OBSTACULO": pygame.Rect(100, 50, 200, 50),
            "CAVALO": pygame.Rect(350, 50, 200, 50),
            "FENO": pygame.Rect(600, 50, 200, 50),
            "INICIAR": pygame.Rect(970, 790, 200, 50),
            "ADMISSIVEL": pygame.Rect(1050, 250, 200, 50),
            "NÃO ADMISSIVEL": pygame.Rect(1000, 320, 250, 50) 
        }
        self.button_values = {
            "OBSTACULO": 1,
            "CAVALO": 2,
            "FENO": 3,
            "PEGADA": 4
        }
        self.colors = {
            0: BLACK,  # Empty cell
            1: GRAY,  # Obstacle
            2: BLUE,  # Horse
            3: GREEN  # Hay
        }
        self.positions = {
            "OBSTACULO": [],
            "CAVALO": None,
            "FENO": None,
            "PEGADAS": []
        }
        self.active_button = "CAVALO"

    def draw_grid(self):
        self.screen.blit(self.background_img, (self.margin_x, self.margin_y))

        for i in range(self.board_size[0]):
            for j in range(self.board_size[1]):
                self.draw_cell(i, j)
        
    
    def draw_cell(self, i, j):
        cell_rect = pygame.Rect(self.margin_x + i * self.cell_size_x, self.margin_y + j * self.cell_size_y, self.cell_size_x, self.cell_size_y)
        if self.board[j][i] != 0:  # If cell is not empty, draw image
            img = pygame.transform.scale(self.images[self.board[j][i]], (self.cell_size_x, self.cell_size_y))
            self.screen.blit(img, cell_rect)

        if self.board[j][i] == 4:  # If cell contains a pegada
            pegada_img = pygame.transform.scale(self.pegada_img, (self.cell_size_x, self.cell_size_y))
            self.screen.blit(pegada_img, cell_rect)



    def draw_buttons(self):
            pygame.draw.rect(self.screen, WHITE, (50, 40, 800, 80), 2)  # Retângulo em volta dos botões do mapa
            pygame.draw.rect(self.screen, WHITE, (970, 230, 300, 170), 2)  # Retângulo em volta dos botões de heurística

            # Adicionando texto
            label_map = self.font.render("Coloque no mapa:", True, WHITE)
            self.screen.blit(label_map, (50, 10))

            label_heuristic = self.font.render("Tipo heuristica", True, WHITE)
            self.screen.blit(label_heuristic, (970, 170))
            
            for button_name, button_rect in self.buttons.items():
                color = RED
                if (button_name == "ADMISSIVEL" and self.admissivel) or (button_name == "NÃO ADMISSIVEL" and not self.admissivel):
                    color = GREEN
                elif self.active_button == button_name:
                    color = RED
                else:
                    if button_name == "INICIAR":
                        color = BLUE
                    else:
                        color = BLACK
                pygame.draw.rect(self.screen, color, button_rect)
                label = self.font.render(button_name, True, WHITE)
                label_rect = label.get_rect(center=button_rect.center)
                self.screen.blit(label, label_rect)



    def draw(self):
        self.screen.fill(BLACK)
        self.draw_grid()
        self.draw_buttons()
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button_name, button_rect in self.buttons.items():
                        if button_rect.collidepoint(event.pos):
                            if button_name == "ADMISSIVEL":
                                self.admissivel = True
                            elif button_name == "NÃO ADMISSIVEL":
                                self.admissivel = False
                            else:
                                self.active_button = button_name
                            if self.active_button == "INICIAR":
                                inicio = self.positions["CAVALO"]
                                fim = self.positions["FENO"]
                                labirinto = self.board
                                
                                
                                self.board[fim[1]][fim[0]] = 0
                                self.board[inicio[1]][inicio[0]] = 0
                                inicio_corrigido = (inicio[1], inicio[0])
                                fim_corrigido = (fim[1], fim[0])
                                print('labirinto:', labirinto, 'inicio:', inicio_corrigido, 'fim:', fim_corrigido, 'admissivel:', self.admissivel)
                                self.path = aestrela(labirinto, inicio_corrigido,fim_corrigido, self.admissivel)
                                print(self.path)
                                self.board[fim[1]][fim[0]] = 3

                                self.path_index = 0
                            return
                    cell_x = (event.pos[0] - self.margin_x) // self.cell_size_x
                    cell_y = (event.pos[1] - self.margin_y) // self.cell_size_y
                    if 0 <= cell_x < self.board_size[0] and 0 <= cell_y < self.board_size[1] and self.active_button in self.button_values:
                        if self.board[cell_y][cell_x] == self.button_values[self.active_button]:
                            self.board[cell_y][cell_x] = 0
                            self.positions[self.active_button] = None if self.active_button != "OBSTACULO" else [
                                pos for pos in self.positions[self.active_button] if pos != (cell_x, cell_y)]
                        elif self.board[cell_y][cell_x] == 0:
                            if (self.active_button == "CAVALO" and self.positions["CAVALO"] is None) or \
                                    (self.active_button == "FENO" and self.positions["FENO"] is None) or \
                                    self.active_button == "OBSTACULO":
                                if self.active_button != "OBSTACULO":
                                    self.positions[self.active_button] = (cell_x, cell_y)
                                else:
                                    self.positions[self.active_button].append((cell_x, cell_y))
                                self.board[cell_y][cell_x] = self.button_values[self.active_button]
                print(self.board)
    def update(self):
        if self.path:  # If there is a path
            self.move_timer += self.clock.get_time()  # Add the time since the last frame to the timer
            if self.move_timer >= 500:  # If it's been 500 milliseconds since the last move
                self.move_timer = 0  # Reset the timer
                if self.path_index < len(self.path):  # If there are still steps to take in the path
                    pos = self.path[self.path_index]  # Get the next position in the path
                    self.board[pos[0]][pos[1]] = 2  # Move the horse to this position
                    
                    if self.path_index > 0:  # If it's not the first step
                        last_pos = self.path[self.path_index - 1]  # Get the last position
                        self.board[last_pos[0]][last_pos[1]] = 4  # Place a pegada in the last position

                    self.path_index += 1  # Move to the next step in the path


    def run_game(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)


        pygame.quit()
        sys.exit()

