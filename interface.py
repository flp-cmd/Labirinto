import pygame
import main

maze = main.labirinto
path = main.main()

# Inicializa o Pygame
pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Define o tamanho da tela
screen_width = 500
screen_height = 500

# Cria a tela
screen = pygame.display.set_mode((screen_width, screen_height))

# Define o título da janela
pygame.display.set_caption("Labirinto")

# Define o tamanho das células do labirinto
cell_width = screen_width // len(maze[0])
cell_height = screen_height // len(maze)


def draw_maze(maze):
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            x = col * cell_width
            y = row * cell_height
            if maze[row][col] == 1:
                color = BLACK
            else:
                color = WHITE
            pygame.draw.rect(screen, color, [x, y, cell_width-1, cell_height-1])


def draw_path(path):
    for position in path:
        row = position[0]
        col = position[1]
        x = col * cell_width
        y = row * cell_height
        pygame.draw.rect(screen, GREEN,[x+cell_width//4,y+cell_height//4,(cell_width//2)-1,(cell_height//2)-1])


def draw_start_end(start, end):
    start_x = start[1] * cell_width
    start_y = start[0] * cell_height
    end_x = end[1] * cell_width
    end_y = end[0] * cell_height

    pygame.draw.circle(screen, RED, (start_x + cell_width // 2, start_y + cell_height // 2), cell_width // 4)
    pygame.draw.circle(screen, RED, (end_x + cell_width // 2, end_y + cell_height // 2), cell_width // 4)


# Loop principal do jogo
running = True
while running:
    # Processa os eventos do Pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Desenha o labirinto
    draw_maze(maze)

    # Desenha o caminho
    draw_path(path)

    # Desenha o ponto inicial e o objetivo
    draw_start_end(main.inicio, main.fim)

    # Atualiza a tela
    pygame.display.flip()

# Finaliza o Pygame
pygame.quit()
