import pygame
import constants as c
from main import *
import sys
import json


class Game:
    def __init__(self, width, height):
        pygame.init()
        self.board_size = (width, height)
        self.board = [[0]*width for _ in range(height)]  # Create a 2D matrix of zeros
        self.screen_size = (c.SCREEN_WIDTH, c.SCREEN_HEIGHT)
        self.board_dimensions = (600, 600) 
        self.cell_size_x = self.board_dimensions[0] // self.board_size[0]
        self.cell_size_y = self.board_dimensions[1] // self.board_size[1]
        self.margin_x = (self.screen_size[0] - self.board_dimensions[0]) // 2
        self.margin_y = (self.screen_size[1] - self.board_dimensions[1]) // 2
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Labirinto - Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 40)
        self.running = True
        self.background_img = pygame.image.load("assets/img/fundo_jogo.png")
        self.horse_img = pygame.image.load("assets/img/horse.png")
        self.fence_img = pygame.image.load("assets/img/fence.png")
        self.hay_img = pygame.image.load("assets/img/feno.png")
        self.footprint_img = pygame.image.load("assets/img/pegada.png")
        self.move_timer = 0
        self.path = []
        self.path_index = 0
        self.custo = 0
        self.images = {
            2: self.horse_img,  
            1: self.fence_img,  
            3: self.hay_img,
            4: self.footprint_img
        }
        self.admissible = True
        self.buttons = {
            "OBSTACULO": pygame.Rect(100, 50, 200, 50),
            "CAVALO": pygame.Rect(350, 50, 200, 50),
            "FENO": pygame.Rect(600, 50, 200, 50),
            "INICIAR": pygame.Rect(750, 790, 200, 50),
            "ADMISSIVEL": pygame.Rect(1050, 250, 200, 50),
            "NÃO ADMISSIVEL": pygame.Rect(1000, 320, 250, 50),
            "RESETAR": pygame.Rect(970, 790, 200, 50)
        }
        self.button_values = {
            "OBSTACULO": 1,
            "CAVALO": 2,
            "FENO": 3,
            "PEGADA": 4
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

        if self.board[j][i] == 4:  # If cell contains a footprint
            footprint_img = pygame.transform.scale(self.footprint_img, (self.cell_size_x, self.cell_size_y))
            self.screen.blit(footprint_img, cell_rect)

    def reset_board(self):
        """Reset the board back to the initial state."""
        new_game = Game(self.board_size[0], self.board_size[1])
        new_game.run_game()


    def draw_buttons(self):
            pygame.draw.rect(self.screen, c.WHITE, (50, 40, 800, 80), 2)  # Retângulo em volta dos botões do mapa
            pygame.draw.rect(self.screen, c.WHITE, (970, 230, 300, 170), 2)  # Retângulo em volta dos botões de heurística

            label_map = self.font.render("Coloque no mapa:", True, c.WHITE)
            self.screen.blit(label_map, (50, 10))

            label_heuristic = self.font.render("Tipo heuristica", True, c.WHITE)
            self.screen.blit(label_heuristic, (970, 170))
            if self.custo is not None:
                cost_text = self.font.render("Custo final: " + str(self.custo), True, c.WHITE)
                self.screen.blit(cost_text, (970, 500))
            
            for button_name, button_rect in self.buttons.items():
                color = c.RED
                if (button_name == "ADMISSIVEL" and self.admissible) or (button_name == "NÃO ADMISSIVEL" and not self.admissible):
                    color = c.GREEN
                elif self.active_button == button_name:
                    color = c.RED
                else:
                    if button_name == "INICIAR":
                        color = c.BLUE
                    else:
                        color = c.BLACK
                pygame.draw.rect(self.screen, color, button_rect)
                label = self.font.render(button_name, True, c.WHITE)
                label_rect = label.get_rect(center=button_rect.center)
                self.screen.blit(label, label_rect)



    def draw(self):
        self.screen.fill(c.BLACK)
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
                                self.admissible = True
                            elif button_name == "NÃO ADMISSIVEL":
                                self.admissible = False
                            elif button_name == "RESETAR":
                                self.reset_board()
                            else:
                                self.active_button = button_name
                            if self.active_button == "INICIAR":
                                start_position = self.positions["CAVALO"]
                                end_position = self.positions["FENO"]
                                labirinto = self.board
                                self.board[end_position[1]][end_position[0]] = 0
                                self.board[start_position[1]][start_position[0]] = 0
                                correct_start_position = (start_position[1], start_position[0])
                                corrent_end_position = (end_position[1], end_position[0])
                                print(self.admissible)
                                self.path, open_list, closed_list, iterations_lists = a_star(labirinto, correct_start_position,corrent_end_position, self.admissible)
                                # print('labirinto:', labirinto, 'inicio:', correct_start_position, 'fim:', corrent_end_position, 'admissivel:', self.admissible)
                                # print("Lista de abertos:", open_list)
                                # print("Lista de fechados:", closed_list)
                                print("Caminho:", self.path)
                                treeData = build_tree_from_a_star(labirinto, open_list, closed_list)
                                treeData['interations_lists'] = iterations_lists
                                self.post_tree(treeData)
                                self.board[end_position[1]][end_position[0]] = 3
                                self.path_index = 0
                                self.custo = closed_list[-1].f
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


    def post_tree(self, tree):
        json_path = "assets/json/treeData.json"
        
        with open(json_path, 'w') as file:
            json.dump(tree, file)


    def run_game(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)


        pygame.quit()
        sys.exit()

