import heapq

maze = [[0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 0, 1, 0]]

start = (0, 0)
end = (4, 4)


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


def astar(maze, start, end):
    start_node = Node(start)
    end_node = Node(end)

    open_list = []
    closed_list = []

    heapq.heappush(open_list, start_node)

    while open_list:
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        if current_node == end_node:
            path = []
            while current_node != start_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]

        neighbors = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for neighbor in neighbors:
            neighbor_position = (current_node.position[0] + neighbor[0], current_node.position[1] + neighbor[1])

            if neighbor_position[0] > (len(maze) - 1) or neighbor_position[0] < 0 or neighbor_position[1] > (len(maze[len(maze)-1]) - 1) or neighbor_position[1] < 0:
                continue

            if maze[neighbor_position[0]][neighbor_position[1]] != 0:
                continue

            neighbor_node = Node(neighbor_position, current_node)

            if neighbor_node in closed_list:
                continue

            neighbor_node.g = current_node.g + 1
            neighbor_node.h = ((neighbor_node.position[0] - end_node.position[0]) ** 2) + ((neighbor_node.position[1] - end_node.position[1]) ** 2)
            neighbor_node.f = neighbor_node.g + neighbor_node.h

            if add_to_open(open_list, neighbor_node):
                heapq.heappush(open_list, neighbor_node)

    return None


def add_to_open(open_list, neighbor):
    for node in open_list:
        if neighbor == node and neighbor.f >= node.f:
            return False
    return True


def main():
    path = astar(maze, start, end)
    return path


if __name__ == '__main__':
    main()
