import heapq
import math

class No:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    # Comparator method to check if node has visited
    def __eq__(self, other):
        return self.position == other.position

    # Comparator method to sort open nodes by f
    def __lt__(self, other):
        return self.f < other.f


def aestrela(maze, start_position, end_position, admissible_heuristic=True):
    open_list = []  
    closed_list = [] 
    node_costs = {}

    initial_node = No(start_position)
    end_node = No(end_position)

    if admissible_heuristic:
        # Manhattan distance
        initial_node.f = abs((initial_node.position[0] - end_node.position[0])) + abs((initial_node.position[1] - end_node.position[1]))  
    else:
        # Euclidean distance
        initial_node.f = ((initial_node.position[0] - end_node.position[0]) ** 2) + ((initial_node.position[1] - end_node.position[1]) ** 2)

    # Priority list sorted by _lt_ method
    heapq.heappush(open_list, initial_node)   
    node_costs[initial_node.position] = initial_node.f

    while open_list:
        current_node = heapq.heappop(open_list)  
        closed_list.append(current_node)  
        print(f"O nó visitado foi o {node_position_to_number(current_node.position, maze)} com custo {node_costs[current_node.position]}")

        if current_node == end_node:    
            path = []
            while current_node != initial_node:
                path.append(current_node.position)
                current_node = current_node.parent
            # Returns the inverted path
            return path[::-1]

        neighbors = [(0, -1), (0, 1), (-1, 0), (1, 0)]  
        for neighbor in neighbors:
            neighbor_position = (current_node.position[0] + neighbor[0], current_node.position[1] + neighbor[1])

            if not in_maze_limits(neighbor_position, maze):  
                continue    

            # Checks if found a wall
            if maze[neighbor_position[0]][neighbor_position[1]] != 0:  
                neighbor_position = (neighbor_position[0] + neighbor[0], neighbor_position[1] + neighbor[1])
                if not in_maze_limits(neighbor_position, maze):  
                    continue    
                # Checks if found a wall after a wall
                if maze[neighbor_position[0]][neighbor_position[1]] != 0:
                    continue    
                neighbor_g = current_node.g + 3  
            else:
                neighbor_g = current_node.g + 1  

            # Current node is the parent of new node
            neighboring_node = No(neighbor_position, current_node)

            # Check if the neighboring node is already in the open list with an equal or higher cost
            if any(neighboring_node == no and neighboring_node.f >= no.f for no in open_list):  
                continue    

            neighboring_node.g = neighbor_g
            if admissible_heuristic:
                # Manhattan distance
                neighboring_node.h = abs((neighboring_node.position[0] - end_node.position[0])) + abs((neighboring_node.position[1] - end_node.position[1]))  
            else:
                # Euclidean distance
                neighboring_node.h = math.sqrt(((neighboring_node.position[0] - end_node.position[0]) ** 2) + ((neighboring_node.position[1] - end_node.position[1]) ** 2)) 

            neighboring_node.f = neighboring_node.g + neighboring_node.h

            if add_node_to_open_list(open_list, neighboring_node):
                heapq.heappush(open_list, neighboring_node)    
                node_costs[neighboring_node.position] = neighboring_node.f
                print(f"Nó aberto: {node_position_to_number(neighboring_node.position, maze)} de custo: {node_costs[neighboring_node.position]}")

    return None

def node_position_to_number(position, maze):
    return (position[0] * len(maze[0])) + (position[1] + 1)


def in_maze_limits(position, maze):   
    linha, coluna = position
    return 0 <= linha < len(maze) and 0 <= coluna < len(maze[linha])


def add_node_to_open_list(open_list, neighbor):  
    for no in open_list:
        if neighbor == no and neighbor.f >= no.f:
            return False
    return True


def show_tree(closed_list, node_costs):
    for no in closed_list:
        print(f"Nó: {no.position} de custo: {node_costs[no.position]}")


def main(maze, start_position, end_position):  
    path = aestrela(maze, start_position, end_position)
    return path

if __name__ == '__main__':
    maze = []  
    start_position = (0, 0)  
    end_position = (5, 5) 
    path = main(maze, start_position, end_position)
    print(path)
