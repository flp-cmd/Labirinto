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

    # Method to heapeq order the open list by f
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
    # Create an empty dictionary to store the iterations' open list and closed list.
    iterations_lists = {"open_list": [], "closed_list": []}
    
    initial_node = Node(start_position)
    end_node = Node(end_position)

    if admissible_heuristic:
        # Manhattan distance
        initial_node.h = abs(initial_node.position[0] - end_node.position[0]) + abs(initial_node.position[1] - end_node.position[1])
    else:
        # Manhattan distance multiplied by 3
        initial_node.h = (abs(initial_node.position[0] - end_node.position[0]) + abs(initial_node.position[1] - end_node.position[1]))*3

    initial_node.f = initial_node.h
    # Adds the initial node to the open list in order ordered by the value of f
    heapq.heappush(open_list, initial_node)

    neighbours = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    # Registers the initial node in the open list of the iterations lists.
    iterations_lists["open_list"].append([node_position_to_number(initial_node.position, maze)])
    
    while open_list:
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)
        # Registers all nodes of the closed list in closed list of the iterations lists
        iterations_lists["closed_list"].append([node_position_to_number(node.position, maze) for node in closed_list])

        if current_node == end_node:
            path = []
            while current_node != initial_node:
                path.append(current_node.position) # Add nodes from end to beginning
                current_node = current_node.parent
            path.append(initial_node.position)
            path.reverse() # Path in order from start to end
            return path, open_list, closed_list, iterations_lists

        for neighbour in neighbours:
            neighbour_position = (current_node.position[0] + neighbour[0], current_node.position[1] + neighbour[1])

            if not in_maze_limits(neighbour_position, maze):
                continue

            # Checks if found a obstacle
            if maze[neighbour_position[0]][neighbour_position[1]] != 0:
                neighbour_position = (neighbour_position[0] + neighbour[0], neighbour_position[1] + neighbour[1])
                # Checks if you are at the limits or if one obstacle after another has been encountered
                if not in_maze_limits(neighbour_position, maze) or maze[neighbour_position[0]][neighbour_position[1]] != 0:
                    continue
                neighbour_g = current_node.g + 3  # Additional cost for obstacle
            else:
                neighbour_g = current_node.g + 1

            neighbour_node = Node(neighbour_position, current_node)

            # Skip the current iteration if the neighbor node is already present in either the open or closed list.
            if any(neighbour_node == node and neighbour_node.f >= node.f for node in open_list) or any(neighbour_node == node for node in closed_list):
                continue

            neighbour_node.g = neighbour_g
            if admissible_heuristic:
                neighbour_node.h = abs(neighbour_node.position[0] - end_node.position[0]) + abs(neighbour_node.position[1] - end_node.position[1])
            else:
                neighbour_node.h = (abs(neighbour_node.position[0] - end_node.position[0]) + abs(neighbour_node.position[1] - end_node.position[1]))*3
            neighbour_node.f = neighbour_node.g + neighbour_node.h

            if add_node_to_open_list(open_list, neighbour_node):
                heapq.heappush(open_list, neighbour_node)
                
        iterations_lists["open_list"].append([node_position_to_number(node.position, maze) for node in open_list])

    return None, open_list, closed_list, iterations_lists

def node_position_to_number(position, maze):
    return position[0] * len(maze[0]) + position[1] + 1

def in_maze_limits(position, maze):
    row, col = position
    return 0 <= row < len(maze) and 0 <= col < len(maze[row])

def add_node_to_open_list(open_list, neighbour):
    for node in open_list:
        if neighbour == node and neighbour.f >= node.f:
            return False
    return True

def build_tree_from_a_star(maze, open_list, closed_list):
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

    for node in open_list:
        if node.parent is not None:
            node_name = node_position_to_number(node.position, maze)
            parent_node_name = node_position_to_number(node.parent.position, maze)
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
    path, open_list, closed_list, iterations_lists = a_star(maze, start_position, end_position,admissible_heuristic)
    #print("Caminho:", path)
    #print("Lista de abertos:", open_list)
    #print("Lista de fechados:", closed_list)

    treeData = build_tree_from_a_star(maze, open_list, closed_list)
    treeData['interations_lists'] = iterations_lists
    return path

maze = [
    [0, 1, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 1, 0, 0, 0],
]

start_position = (0, 0)
end_position = (4, 4)

main(maze, start_position, end_position, admissible_heuristic=True)
main(maze, start_position, end_position, admissible_heuristic=False)
