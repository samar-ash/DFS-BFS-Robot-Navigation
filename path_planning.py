class Path:
    def __init__(self, file_name):
        self.file_name = file_name
        self.read_file()
        self.close_list = set()

    def read_file(self):
        file = open('worlds/' + self.file_name, 'r')
        state = {"robot_location": [], "samples_location": []}
        lines = file.readlines()
        gridsize = [int(lines[0]), int(lines[1])]

        count = -2
        blocks_location = []
        for line in lines:
            count += 1
            robot_index = line.rfind('@')
            if robot_index != -1:
                state['robot_location'].append([count, robot_index])
            for char_idx in range(len(line)):
                if line[char_idx] == '*':
                    sample_index = line.rfind('*')
                    state['samples_location'].append([count, sample_index])
                elif line[char_idx] == '#':
                    block_index = char_idx
                    blocks_location.append([count, block_index])

        return state, blocks_location, gridsize


    def solve(self, state, algorithm):
        node = Node(state, None, None)
        if algorithm == "dfs":
            open_list = OpenList()
        else:
            open_list = Queue()

        close_list = OpenList()
        open_list.add(node)

        i = 0
        count = 1
        while True:
            i += 1
            if open_list.empty():
                raise Exception("no solution")
            node = open_list.remove()
            if node.goal(node.state):
                final_actions = []
                while node.parent is not None:
                    final_actions.append(node.actions)
                    node = node.parent
                final_actions.reverse()
                print("The expanded nodes are:", (close_list.show()), "and The generated nodes are", count)
                return final_actions

            neighbor_action = ["U", "D", "L", "R", "S"]
            for move in neighbor_action:
                new_state = node.update_state(node.state, move, gridsize, blocks_location)
                if new_state != 0 and not open_list.contain_state(new_state) and not close_list.contain_state(new_state):

                    child = Node(new_state, node, move)
                    open_list.add(child)

                    count += 1

            print(move, open_list.show())
            close_list.add(node)


class Node:
    def __init__(self, state, parent, actions, g_cost=1):
        self.state = state
        self.parent = parent
        self.actions = actions
        self.g_cost = g_cost

    def goal(self, state):
        if len(state["samples_location"]) == 0:
            return True
    def update_state(self, state, action, gridsize, g_cost=1):
        flag = 0
        robot_x_cordinate = int(state['robot_location'][0][0])
        robot_y_cordinate = int(state['robot_location'][0][1])
        if action == "U":
            if ((robot_x_cordinate - 1) >= 1) and (
                    [robot_x_cordinate - 1, robot_y_cordinate] not in blocks_location):
                robot_x_cordinate -= 1
                action = "U"
                flag = 1
        elif action == "D":
            if (robot_x_cordinate + 1) <= gridsize[0] and (
                    [robot_x_cordinate + 1, robot_y_cordinate] not in blocks_location):
                robot_x_cordinate += 1
                action = "D"
                flag = 1

        elif action == "L":
            if (robot_y_cordinate - 1) >= 1 and ([robot_x_cordinate, robot_y_cordinate - 1] not in blocks_location):
                robot_y_cordinate -= 1
                action = "L"
                flag = 1
        elif action == "R":
            if (robot_y_cordinate + 1) <= gridsize[1] and (
                    [robot_x_cordinate, robot_y_cordinate + 1] not in blocks_location):
                robot_y_cordinate += 1
                action = "R"
                flag = 1
        elif action == "S":
            if state['robot_location'][0] in state['samples_location']:
                flag = 1
                action = "S"
        if flag == 1:
            new_state = {"robot_location": [[robot_x_cordinate, robot_y_cordinate]],
                         "samples_location": state['samples_location']}
            if action == "S" and state['robot_location'][0] in state['samples_location']:
                new_state['samples_location'] = [x for x in new_state['samples_location'] if
                                                 x != state['robot_location'][0]]
                return new_state

            return new_state
        else:
            return 0


class OpenList:
    def __init__(self):
        self.open_list = []

    def add(self, node):
        self.open_list.append(node)

    def contain_state(self, state):
        for node in self.open_list:
            if node.state == state:
                return True
        return False

    def empty(self):
        return len(self.open_list) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty open_list")
        else:
            node = self.open_list[-1]
            self.open_list = self.open_list[:-1]
            return node

    def show(self):
        j = 0
        for node in self.open_list:
            j += 1
            print(j, node.state, node.actions, node, node.parent)
        return j


class Queue(OpenList):
    def __init__(self):
        super().__init__()

    def remove(self):
        if self.empty():
            raise Exception("empty open_list")
        node = self.open_list[0]
        self.open_list = self.open_list[1:]
        return node


path_planning = Path("small1.txt")
state, blocks_location, gridsize = path_planning.read_file()
print("blocks locations:", blocks_location)
print("size of a world:", gridsize)
print(path_planning.solve(state, algorithm="ucs"))
