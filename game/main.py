import heapq
import math
import datetime

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f
    
    def __repr__(self):
        return f"Node(position={self.position}, g={self.g}, h={self.h}, f={self.f})"

class TreeNode:
    def __init__(self, name, parent=None, evaluation=0):
        self.name = name
        self.parent = parent
        self.evaluation = evaluation
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def to_dict(self):
        children = [child.to_dict() for child in self.children]

        return {
            "name": self.name,
            "parent": self.parent,
            "evaluation": self.evaluation,
            "children": children
        }

def a_star(maze, start_position, end_position, admissible_heuristic=True):
    open_list = []
    closed_list = []
    node_costs = {}

    initial_node = Node(start_position)
    end_node = Node(end_position)

    if admissible_heuristic:
        initial_node.h = abs(initial_node.position[0] - end_node.position[0]) + abs(initial_node.position[1] - end_node.position[1])
    else:
        initial_node.h = math.sqrt((initial_node.position[0] - end_node.position[0]) ** 2 + (initial_node.position[1] - end_node.position[1]) ** 2)

    initial_node.f = initial_node.h
    heapq.heappush(open_list, initial_node)
    node_costs[initial_node.position] = initial_node.f

    neighbors = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # Movements: up, down, left, right

    while open_list:
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        if current_node == end_node:
            path = []
            while current_node != initial_node:
                path.append(current_node.position)
                current_node = current_node.parent
            path.append(initial_node.position)
            path.reverse()
            return path, open_list, closed_list

        for neighbor in neighbors:
            neighbor_position = (current_node.position[0] + neighbor[0], current_node.position[1] + neighbor[1])

            if not in_maze_limits(neighbor_position, maze):
                continue

            if maze[neighbor_position[0]][neighbor_position[1]] != 0:
                neighbor_position = (neighbor_position[0] + neighbor[0], neighbor_position[1] + neighbor[1])
                if not in_maze_limits(neighbor_position, maze) or maze[neighbor_position[0]][neighbor_position[1]] != 0:
                    continue
                neighbor_g = current_node.g + 3  # Additional cost for obstacle
            else:
                neighbor_g = current_node.g + 1

            neighboring_node = Node(neighbor_position, current_node)

            if any(neighboring_node == node and neighboring_node.f >= node.f for node in open_list) or any(neighboring_node == node for node in closed_list):
                continue

            neighboring_node.g = neighbor_g
            if admissible_heuristic:
                neighboring_node.h = abs(neighboring_node.position[0] - end_node.position[0]) + abs(neighboring_node.position[1] - end_node.position[1])
            else:
                neighboring_node.h = (abs(neighboring_node.position[0] - end_node.position[0]) + abs(neighboring_node.position[1] - end_node.position[1]))*3
            neighboring_node.f = neighboring_node.g + neighboring_node.h

            if add_node_to_open_list(open_list, neighboring_node):
                heapq.heappush(open_list, neighboring_node)
                node_costs[neighboring_node.position] = neighboring_node.f

    return None, open_list, closed_list


def node_position_to_number(position, maze):
    return position[0] * len(maze[0]) + position[1] + 1

def in_maze_limits(position, maze):
    row, col = position
    return 0 <= row < len(maze) and 0 <= col < len(maze[row])

def add_node_to_open_list(open_list, neighbor):
    for node in open_list:
        if neighbor == node and neighbor.f >= node.f:
            return False
    return True

def build_tree_from_a_star(maze, closed_list):
    tree_nodes = {}
    root_node = None

    for node in closed_list:
        node_name = node_position_to_number(node.position, maze)
        parent_node = node.parent

        if parent_node is None:
            root_node = TreeNode(node_name, evaluation=node.f)
            tree_nodes[node_name] = root_node
        else:
            parent_node_name = node_position_to_number(parent_node.position, maze)
            tree_node = TreeNode(node_name, parent=parent_node_name, evaluation=node.f)
            tree_nodes[node_name] = tree_node
            parent_tree_node = tree_nodes[parent_node_name]
            parent_tree_node.add_child(tree_node)

    if root_node is not None:
        return {
            "treeNodes": root_node.to_dict(),
            "timestamp": datetime.datetime.now().timestamp()
        }

    return None

def main(maze, start_position, end_position,admissible_heuristic):
    path, open_list, closed_list = a_star(maze, start_position, end_position,admissible_heuristic)
    print("Caminho:", path)
    print(closed_list[-1])
    print("Lista de abertos:", open_list)
    print("Lista de fechados:", closed_list)

    tree = build_tree_from_a_star(maze, closed_list)
    show_tree(tree)

    return path

def show_tree(tree):
    pass
    if tree is not None:
        print("Árvore:")
        print(tree)

maze = [
    [0, 1, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 1, 0, 0, 0]
]

start_position = (0, 0)
end_position = (4, 4)

main(maze, start_position, end_position, admissible_heuristic=True)
main(maze, start_position, end_position, admissible_heuristic=False)
