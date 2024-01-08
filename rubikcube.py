from random import randint, choice
from math import sqrt
from copy import deepcopy


class RubikCube:
    def __init__(self, n=3, colors=['Y', 'R', 'G', 'O', 'B', 'W'], state=None, history=[]):
        """
        Initializes a new Rubik Cube
        :param n: (int) size of the nxn Rubik Cube
        :param colors: (list) contain all the colors of the Rubik Cube
        :param state: (string) current state of the Rubik Cube (ex: "000000000111111111222222222333333333444444444555555555")
        :param history: (list) list of rotation history
        """
        self.history = history
        self.state = state
        if state:
            self.n = int(sqrt(len(state) / 6))
            self.colors = []
            for c in state:
                if c not in self.colors:
                    self.colors.append(c)
                if len(self.colors) == 6:
                    break
            self.cube = [[[c for c in state[r + s:r + s + self.n]] for r in range(0, self.n ** 2, self.n)] for s in
                         range(0, len(state), 9)]
            if not self._validate_state():
                print("--------------INVALID INPUT STATE--------------")
                print("------------------RESET CUBE------------------")
                self.reset()
        else:
            self.n = n
            self.colors = colors
            self.reset()

    def _validate_state(self):
        if len(self.colors) != 6:
            return False
        color_pieces_count = [0 for _ in self.colors]
        for s in self.cube:
            for r in s:
                for c in r:
                    for i in range(len(self.colors)):
                        if c == self.colors[i]:
                            color_pieces_count[i] += 1
        if color_pieces_count.count(9) != 6:
            return False
        return True

    def __str__(self):
        """
        Return string representation of the Rubik Cube's current state
        :return: string
        """
        return ''.join([c for s in self.cube for r in s for c in r])

    def update_state(self, state):
        self.state = state
        self.clear_history()
        self.n = int(sqrt(len(state) / 6))
        self.colors = []
        for c in state:
            if c not in self.colors:
                self.colors.append(c)
            if len(self.colors) == 6:
                break
        self.cube = [[[c for c in state[r + s:r + s + self.n]] for r in range(0, self.n ** 2, self.n)] for s in
                     range(0, len(state), 9)]
    def reset(self):
        """
        Reset the Rubik Cube to its initial state
        :return: None
        """
        self.cube = [[[s for c in range(self.n)] for r in range(self.n)] for s in self.colors]
        self._update_state()
        self.clear_history()

    def solved(self):
        """
        Check if the Rubik Cube solved or not
        :return: bool
        """
        for side in self.cube:
            check = []
            for row in side:
                if len(set(row)) != 1:
                    return False
                else:
                    check.append(row[0])
            if len(set(check)) != 1:
                return False
        return True

    def show(self):
        """
        Show the Rubik Cube in 2D form
        :return: None
        """
        spacing = f'{" " * (len(str(self.cube[0][0])) + 2)}'
        l1 = '\n'.join(spacing + str(c) for c in self.cube[0])
        l2 = '\n'.join('  '.join(str(self.cube[i][j]) for i in range(1, 5)) for j in range(self.n))
        l3 = '\n'.join(spacing + str(c) for c in self.cube[5])
        print(f'{l1}\n\n{l2}\n\n{l3}')

    def shuffle(self, min_rot=10, max_rot=100):
        """
        Shuffle the Rubik Cube's state
        :param min_rot: (int) lower bound of the number of rotation
        :param max_rot: (int) upper bound of the number of rotation
        :return: None
        """
        rot_num = randint(min_rot, max_rot)
        next_rot_side_dict = {"U": [1, 2, 3, 4, 5], "U2": [1, 2, 3, 4, 5], "U'": [1, 2, 3, 4, 5],
                              "L": [0, 2, 3, 4, 5], "L2": [0, 2, 3, 4, 5], "L'": [0, 2, 3, 4, 5],
                              "F": [0, 1, 3, 4, 5], "F2": [0, 1, 3, 4, 5], "F'": [0, 1, 3, 4, 5],
                              "R": [0, 1, 2, 4, 5], "R2": [0, 1, 2, 4, 5], "R'": [0, 1, 2, 4, 5],
                              "B": [0, 1, 2, 3, 5], "B2": [0, 1, 2, 3, 5], "B'": [0, 1, 2, 3, 5],
                              "D": [0, 1, 2, 3, 4], "D2": [0, 1, 2, 3, 4], "D'": [0, 1, 2, 3, 4]}
        rot_dict = {0: [self.U, self.U2, self.Ui],
                    1: [self.L, self.L2, self.Li],
                    2: [self.F, self.F2, self.Fi],
                    3: [self.R, self.R2, self.Ri],
                    4: [self.B, self.B2, self.Bi],
                    5: [self.D, self.D2, self.Di]}

        for _ in range(rot_num):
            dir = choice(range(3))
            rot_side = -1
            if self.history:
                rot_side = choice(next_rot_side_dict[self.history[len(self.history) - 1]])
            else:
                rot_side = choice(range(6))
            rot_dict[rot_side][dir]()
        self._update_state()
        self.clear_history()

    def clear_history(self):
        """
        Clear the history
        :return: None
        """
        self.history = []

    def show_history(self):
        """
        Print rotation history
        :return: None
        """
        for move in self.history:
            print(move, end=" ")

    def _update_state(self):
        """
        Update Rubik state
        :return: None
        """
        temp = []
        for s in self.cube:
            for r in range(self.n):
                for c in range(self.n):
                    temp.append(s[r][c])
        self.state = "".join(temp)

    def _horizontal_rotation(self, row, direction):
        """
        Rotates the Rubik Cube in horizontal direction
        :param row: (int) the selected row for horizontal rotation
        :param direction: (int) the direction for horizontal rotation (left = 0 || right = 1)
        :return: None
        """
        if row < self.n:
            if direction == 0:  # Rotate left
                self.cube[1][row], self.cube[2][row], self.cube[3][row], self.cube[4][row] = (self.cube[2][row],
                                                                                              self.cube[3][row],
                                                                                              self.cube[4][row],
                                                                                              self.cube[1][row])
                # Rotate the connected side
                if row == 0:
                    self.cube[0] = [[self.cube[0][i][r] for i in range(self.n - 1, -1, -1)] for r in range(self.n)]
                elif row == self.n - 1:
                    self.cube[5] = [[self.cube[5][i][r] for i in range(self.n)] for r in range(self.n - 1, -1, -1)]

            elif direction == 1:  # Rotate right
                self.cube[1][row], self.cube[2][row], self.cube[3][row], self.cube[4][row] = (self.cube[4][row],
                                                                                              self.cube[1][row],
                                                                                              self.cube[2][row],
                                                                                              self.cube[3][row])
                # Rotate the connected side
                if row == 0:
                    self.cube[0] = [[self.cube[0][i][r] for i in range(self.n)] for r in range(self.n - 1, -1, -1)]
                elif row == self.n - 1:
                    self.cube[5] = [[self.cube[5][i][r] for i in range(self.n - 1, -1, -1)] for r in range(self.n)]

    def _vertical_rotation(self, col, direction):
        """
        Rotates the Rubik Cube in vertical direction
        :param col: (int) the selected column for vertical rotation
        :param direction: (int) the direction for vertical rotation (down = 0 || up = 1)
        :return: None
        """
        if col < self.n:
            for i in range(self.n):
                if direction == 0:  # Rotate down
                    self.cube[0][i][col], self.cube[2][i][col], self.cube[4][-i - 1][-col - 1], self.cube[5][i][col] = (
                        self.cube[4][-i - 1][-col - 1],
                        self.cube[0][i][col],
                        self.cube[5][i][col],
                        self.cube[2][i][col])
                elif direction == 1:  # Rotate up
                    self.cube[0][i][col], self.cube[2][i][col], self.cube[4][-i - 1][-col - 1], self.cube[5][i][col] = (
                        self.cube[2][i][col],
                        self.cube[5][i][col],
                        self.cube[0][i][col],
                        self.cube[4][-i - 1][-col - 1])

            # Rotate the connected side
            if direction == 0:  # Rotate down
                if col == 0:
                    self.cube[1] = [[self.cube[1][i][r] for i in range(self.n - 1, -1, -1)] for r in range(self.n)]
                elif col == self.n - 1:
                    self.cube[3] = [[self.cube[3][i][r] for i in range(self.n)] for r in range(self.n - 1, -1, -1)]
            elif direction == 1:  # Rotate up
                if col == 0:
                    self.cube[1] = [[self.cube[1][i][r] for i in range(self.n)] for r in range(self.n - 1, -1, -1)]
                elif col == self.n - 1:
                    self.cube[3] = [[self.cube[3][i][r] for i in range(self.n - 1, -1, -1)] for r in range(self.n)]

    def _side_rotation(self, col, direction):
        """
        Rotates the Rubik Cube in side direction
        :param col: (int) the selected column for vertical rotation
        :param direction: (int) the direction for vertical rotation (down = 0 || up = 1)
        :return: None
        """
        if col < self.n:
            for i in range(self.n):
                if direction == 0:  # Rotate down
                    self.cube[0][col][i], self.cube[1][-i - 1][col], self.cube[3][i][-col - 1], self.cube[5][-col - 1][
                        -1 - i] = (self.cube[3][i][-col - 1],
                                   self.cube[0][col][i],
                                   self.cube[5][-col - 1][-1 - i],
                                   self.cube[1][-i - 1][col])
                elif direction == 1:  # Rotate up
                    self.cube[0][col][i], self.cube[1][-i - 1][col], self.cube[3][i][-col - 1], self.cube[5][-col - 1][
                        -1 - i] = (self.cube[1][-i - 1][col],
                                   self.cube[5][-col - 1][-1 - i],
                                   self.cube[0][col][i],
                                   self.cube[3][i][-col - 1])

            # Rotate the connected side
            if direction == 0:  # Rotate down
                if col == 0:
                    self.cube[4] = [[self.cube[4][i][r] for i in range(self.n - 1, -1, -1)] for r in range(self.n)]
                elif col == self.n - 1:
                    self.cube[2] = [[self.cube[2][i][r] for i in range(self.n)] for r in range(self.n - 1, -1, -1)]
            elif direction == 1:  # Rotate up
                if col == 0:
                    self.cube[4] = [[self.cube[4][i][r] for i in range(self.n)] for r in range(self.n - 1, -1, -1)]
                elif col == self.n - 1:
                    self.cube[2] = [[self.cube[2][i][r] for i in range(self.n - 1, -1, -1)] for r in range(self.n)]

    def U(self):
        self._horizontal_rotation(0, 0)
        self._update_state()
        if self.history:
            if self.history[-1] == "U2":
                self.history.pop()
                self.history.append("U'")
            elif self.history[-1] == "U'":
                self.history.pop()
            elif self.history[-1] == "U":
                self.history.pop()
                self.history.append("U2")
            else:
                self.history.append("U")
        else:
            self.history.append("U")

    def U2(self):
        self._horizontal_rotation(0, 0)
        self._horizontal_rotation(0, 0)
        self._update_state()
        if self.history:
            if self.history[-1] == "U2":
                self.history.pop()
            elif self.history[-1] == "U'":
                self.history.pop()
                self.history.append("U")
            elif self.history[-1] == "U":
                self.history.pop()
                self.history.append("U'")
            else:
                self.history.append("U2")
        else:
            self.history.append("U2")

    def Ui(self):
        self._horizontal_rotation(0, 1)
        self._update_state()
        if self.history:
            if self.history[-1] == "U2":
                self.history.pop()
                self.history.append("U")
            elif self.history[-1] == "U'":
                self.history.pop()
                self.history.append("U2")
            elif self.history[-1] == "U":
                self.history.pop()
            else:
                self.history.append("U'")
        else:
            self.history.append("U'")

    def L(self):
        self._vertical_rotation(0, 0)
        self._update_state()
        if self.history:
            if self.history[-1] == "L2":
                self.history.pop()
                self.history.append("L'")
            elif self.history[-1] == "L'":
                self.history.pop()
            elif self.history[-1] == "L":
                self.history.pop()
                self.history.append("L2")
            else:
                self.history.append("L")
        else:
            self.history.append("L")

    def L2(self):
        self._vertical_rotation(0, 0)
        self._vertical_rotation(0, 0)
        self._update_state()
        if self.history:
            if self.history[-1] == "L2":
                self.history.pop()
            elif self.history[-1] == "L'":
                self.history.pop()
                self.history.append("L")
            elif self.history[-1] == "L":
                self.history.pop()
                self.history.append("L'")
            else:
                self.history.append("L2")
        else:
            self.history.append("L2")

    def Li(self):
        self._vertical_rotation(0, 1)
        self._update_state()
        if self.history:
            if self.history[-1] == "L2":
                self.history.pop()
                self.history.append("L")
            elif self.history[-1] == "L'":
                self.history.pop()
                self.history.append("L2")
            elif self.history[-1] == "L":
                self.history.pop()
            else:
                self.history.append("L'")
        else:
            self.history.append("L'")

    def F(self):
        self._side_rotation(self.n - 1, 1)
        self._update_state()
        if self.history:
            if self.history[-1] == "F2":
                self.history.pop()
                self.history.append("F'")
            elif self.history[-1] == "F'":
                self.history.pop()
            elif self.history[-1] == "F":
                self.history.pop()
                self.history.append("F2")
            else:
                self.history.append("F")
        else:
            self.history.append("F")

    def F2(self):
        self._side_rotation(self.n - 1, 1)
        self._side_rotation(self.n - 1, 1)
        self._update_state()
        if self.history:
            if self.history[-1] == "F2":
                self.history.pop()
            elif self.history[-1] == "F'":
                self.history.pop()
                self.history.append("F")
            elif self.history[-1] == "F":
                self.history.pop()
                self.history.append("F'")
            else:
                self.history.append("F2")
        else:
            self.history.append("F2")

    def Fi(self):
        self._side_rotation(self.n - 1, 0)
        self._update_state()
        if self.history:
            if self.history[-1] == "F2":
                self.history.pop()
                self.history.append("F")
            elif self.history[-1] == "F'":
                self.history.pop()
                self.history.append("F2")
            elif self.history[-1] == "F":
                self.history.pop()
            else:
                self.history.append("F'")
        else:
            self.history.append("F'")

    def R(self):
        self._vertical_rotation(self.n - 1, 1)
        self._update_state()
        if self.history:
            if self.history[-1] == "R2":
                self.history.pop()
                self.history.append("R'")
            elif self.history[-1] == "R'":
                self.history.pop()
            elif self.history[-1] == "R":
                self.history.pop()
                self.history.append("R2")
            else:
                self.history.append("R")
        else:
            self.history.append("R")

    def R2(self):
        self._vertical_rotation(self.n - 1, 1)
        self._vertical_rotation(self.n - 1, 1)
        self._update_state()
        if self.history:
            if self.history[-1] == "R2":
                self.history.pop()
            elif self.history[-1] == "R'":
                self.history.pop()
                self.history.append("R")
            elif self.history[-1] == "R":
                self.history.pop()
                self.history.append("R'")
            else:
                self.history.append("R2")
        else:
            self.history.append("R2")

    def Ri(self):
        self._vertical_rotation(self.n - 1, 0)
        self._update_state()
        if self.history:
            if self.history[-1] == "R2":
                self.history.pop()
                self.history.append("R")
            elif self.history[-1] == "R'":
                self.history.pop()
                self.history.append("R2")
            elif self.history[-1] == "R":
                self.history.pop()
            else:
                self.history.append("R'")
        else:
            self.history.append("R'")

    def B(self):
        self._side_rotation(0, 0)
        self._update_state()
        if self.history:
            if self.history[-1] == "B2":
                self.history.pop()
                self.history.append("B'")
            elif self.history[-1] == "B'":
                self.history.pop()
            elif self.history[-1] == "B":
                self.history.pop()
                self.history.append("B2")
            else:
                self.history.append("B")
        else:
            self.history.append("B")

    def B2(self):
        self._side_rotation(0, 0)
        self._side_rotation(0, 0)
        self._update_state()
        if self.history:
            if self.history[-1] == "B2":
                self.history.pop()
            elif self.history[-1] == "B'":
                self.history.pop()
                self.history.append("B")
            elif self.history[-1] == "B":
                self.history.pop()
                self.history.append("B'")
            else:
                self.history.append("B2")
        else:
            self.history.append("B2")

    def Bi(self):
        self._side_rotation(0, 1)
        self._update_state()
        if self.history:
            if self.history[-1] == "B2":
                self.history.pop()
                self.history.append("B")
            elif self.history[-1] == "B'":
                self.history.pop()
                self.history.append("B2")
            elif self.history[-1] == "B":
                self.history.pop()
            else:
                self.history.append("B'")
        else:
            self.history.append("B'")

    def D(self):
        self._horizontal_rotation(self.n - 1, 1)
        self._update_state()
        if self.history:
            if self.history[-1] == "D2":
                self.history.pop()
                self.history.append("D'")
            elif self.history[-1] == "D'":
                self.history.pop()
            elif self.history[-1] == "D":
                self.history.pop()
                self.history.append("D2")
            else:
                self.history.append("D")
        else:
            self.history.append("D")

    def D2(self):
        self._horizontal_rotation(self.n - 1, 1)
        self._horizontal_rotation(self.n - 1, 1)
        self._update_state()
        if self.history:
            if self.history[-1] == "D2":
                self.history.pop()
            elif self.history[-1] == "D'":
                self.history.pop()
                self.history.append("D")
            elif self.history[-1] == "D":
                self.history.pop()
                self.history.append("D'")
            else:
                self.history.append("D2")
        else:
            self.history.append("D2")

    def Di(self):
        self._horizontal_rotation(self.n - 1, 0)
        self._update_state()
        if self.history:
            if self.history[-1] == "D2":
                self.history.pop()
                self.history.append("D")
            elif self.history[-1] == "D'":
                self.history.pop()
                self.history.append("D2")
            elif self.history[-1] == "D":
                self.history.pop()
            else:
                self.history.append("D'")
        else:
            self.history.append("D'")


class BFSBBCube(RubikCube):
    def __init__(self, n=3, colors=['Y', 'R', 'G', 'O', 'B', 'W'], state=None, history=[]):
        super().__init__(n, colors, state, history)

    def _validate_state(self):
        if len(self.colors) != 6:
            return False
        color_pieces_count = [0 for _ in self.colors]
        for s in self.cube:
            for r in s:
                for c in r:
                    for i in range(len(self.colors)):
                        if c == self.colors[i]:
                            color_pieces_count[i] += 1
        if color_pieces_count.count(9) != 6:
            return False
        return True

    def __str__(self):
        """
        Return string representation of the Rubik Cube's current state
        :return: string
        """
        return ''.join([c for s in self.cube for r in s for c in r])

    def reset(self):
        """
        Reset the Rubik Cube to its initial state
        :return: None
        """
        self.cube = [[[s for c in range(self.n)] for r in range(self.n)] for s in self.colors]
        self._update_state()
        self.clear_history()

    def solved(self):
        """
        Check if the Rubik Cube solved or not
        :return: bool
        """
        for side in self.cube:
            check = []
            for row in side:
                if len(set(row)) != 1:
                    return False
                else:
                    check.append(row[0])
            if len(set(check)) != 1:
                return False
        return True

    def show(self):
        """
        Show the Rubik Cube in 2D form
        :return: None
        """
        spacing = f'{" " * (len(str(self.cube[0][0])) + 2)}'
        l1 = '\n'.join(spacing + str(c) for c in self.cube[0])
        l2 = '\n'.join('  '.join(str(self.cube[i][j]) for i in range(1, 5)) for j in range(self.n))
        l3 = '\n'.join(spacing + str(c) for c in self.cube[5])
        print(f'{l1}\n\n{l2}\n\n{l3}')

    def shuffle(self, min_rot=10, max_rot=100):
        rot_num = randint(min_rot, max_rot)
        # Action = 0 (U), 1 (U2), 3 (Ui), 4 (L), ... , 16 (D2), 17(Di)
        rot_num = randint(min_rot, max_rot)
        next_rot_side_dict = {"U": [1, 2, 3, 4, 5], "U2": [1, 2, 3, 4, 5], "U'": [1, 2, 3, 4, 5],
                              "L": [0, 2, 3, 4, 5], "L2": [0, 2, 3, 4, 5], "L'": [0, 2, 3, 4, 5],
                              "F": [0, 1, 3, 4, 5], "F2": [0, 1, 3, 4, 5], "F'": [0, 1, 3, 4, 5],
                              "R": [0, 1, 2, 4, 5], "R2": [0, 1, 2, 4, 5], "R'": [0, 1, 2, 4, 5],
                              "B": [0, 1, 2, 3, 5], "B2": [0, 1, 2, 3, 5], "B'": [0, 1, 2, 3, 5],
                              "D": [0, 1, 2, 3, 4], "D2": [0, 1, 2, 3, 4], "D'": [0, 1, 2, 3, 4]}
        rot_dict = {0: [self.U, self.U2, self.Ui],
                    1: [self.L, self.L2, self.Li],
                    2: [self.F, self.F2, self.Fi],
                    3: [self.R, self.R2, self.Ri],
                    4: [self.B, self.B2, self.Bi],
                    5: [self.D, self.D2, self.Di]}

        for _ in range(rot_num):
            dir = choice(range(3))
            rot_side = -1
            if self.history:
                rot_side = choice(next_rot_side_dict[self.history[len(self.history) - 1]])
            else:
                rot_side = choice(range(6))
            rot_dict[rot_side][dir](self.cube, self.history)
        self.clear_history()

    def clear_history(self):
        """
        Clear the history
        :return: None
        """
        self.history = []

    def show_history(self):
        """
        Print rotation history
        :return: None
        """
        for move in self.history:
            print(move, end=" ")

    def _update_state(self):
        """
        Update Rubik state
        :return: None
        """
        temp = []
        for s in self.cube:
            for r in range(self.n):
                for c in range(self.n):
                    temp.append(s[r][c])
        self.state = "".join(temp)

    def _horizontal_rotation(self, row, direction, cube):
        """
        Rotates the Rubik Cube in horizontal direction
        :param row: (int) the selected row for horizontal rotation
        :param direction: (int) the direction for horizontal rotation (left = 0 || right = 1)
        :return: None
        """
        if row < self.n:
            if direction == 0:  # Rotate left
                cube[1][row], cube[2][row], cube[3][row], cube[4][row] = (cube[2][row],
                                                                          cube[3][row],
                                                                          cube[4][row],
                                                                          cube[1][row])
                # Rotate the connected side
                if row == 0:
                    cube[0] = [[cube[0][i][r] for i in range(self.n - 1, -1, -1)] for r in range(self.n)]
                elif row == self.n - 1:
                    cube[5] = [[cube[5][i][r] for i in range(self.n)] for r in range(self.n - 1, -1, -1)]

            elif direction == 1:  # Rotate right
                cube[1][row], cube[2][row], cube[3][row], cube[4][row] = (cube[4][row],
                                                                          cube[1][row],
                                                                          cube[2][row],
                                                                          cube[3][row])
                # Rotate the connected side
                if row == 0:
                    cube[0] = [[cube[0][i][r] for i in range(self.n)] for r in range(self.n - 1, -1, -1)]
                elif row == self.n - 1:
                    cube[5] = [[cube[5][i][r] for i in range(self.n - 1, -1, -1)] for r in range(self.n)]

    def _vertical_rotation(self, col, direction, cube):
        """
        Rotates the Rubik Cube in vertical direction
        :param col: (int) the selected column for vertical rotation
        :param direction: (int) the direction for vertical rotation (down = 0 || up = 1)
        :return: None
        """
        if col < self.n:
            for i in range(self.n):
                if direction == 0:  # Rotate down
                    cube[0][i][col], cube[2][i][col], cube[4][-i - 1][-col - 1], cube[5][i][col] = (
                        cube[4][-i - 1][-col - 1],
                        cube[0][i][col],
                        cube[5][i][col],
                        cube[2][i][col])
                elif direction == 1:  # Rotate up
                    cube[0][i][col], cube[2][i][col], cube[4][-i - 1][-col - 1], cube[5][i][col] = (
                        cube[2][i][col],
                        cube[5][i][col],
                        cube[0][i][col],
                        cube[4][-i - 1][-col - 1])

            # Rotate the connected side
            if direction == 0:  # Rotate down
                if col == 0:
                    cube[1] = [[cube[1][i][r] for i in range(self.n - 1, -1, -1)] for r in range(self.n)]
                elif col == self.n - 1:
                    cube[3] = [[cube[3][i][r] for i in range(self.n)] for r in range(self.n - 1, -1, -1)]
            elif direction == 1:  # Rotate up
                if col == 0:
                    cube[1] = [[cube[1][i][r] for i in range(self.n)] for r in range(self.n - 1, -1, -1)]
                elif col == self.n - 1:
                    cube[3] = [[cube[3][i][r] for i in range(self.n - 1, -1, -1)] for r in range(self.n)]

    def _side_rotation(self, col, direction, cube):
        """
        Rotates the Rubik Cube in side direction
        :param col: (int) the selected column for vertical rotation
        :param direction: (int) the direction for vertical rotation (down = 0 || up = 1)
        :return: None
        """
        if col < self.n:
            for i in range(self.n):
                if direction == 0:  # Rotate down
                    cube[0][col][i], cube[1][-i - 1][col], cube[3][i][-col - 1], cube[5][-col - 1][
                        -1 - i] = (cube[3][i][-col - 1],
                                   cube[0][col][i],
                                   cube[5][-col - 1][-1 - i],
                                   cube[1][-i - 1][col])
                elif direction == 1:  # Rotate up
                    cube[0][col][i], cube[1][-i - 1][col], cube[3][i][-col - 1], cube[5][-col - 1][
                        -1 - i] = (cube[1][-i - 1][col],
                                   cube[5][-col - 1][-1 - i],
                                   cube[0][col][i],
                                   cube[3][i][-col - 1])

            # Rotate the connected side
            if direction == 0:  # Rotate down
                if col == 0:
                    cube[4] = [[cube[4][i][r] for i in range(self.n - 1, -1, -1)] for r in range(self.n)]
                elif col == self.n - 1:
                    cube[2] = [[cube[2][i][r] for i in range(self.n)] for r in range(self.n - 1, -1, -1)]
            elif direction == 1:  # Rotate up
                if col == 0:
                    cube[4] = [[cube[4][i][r] for i in range(self.n)] for r in range(self.n - 1, -1, -1)]
                elif col == self.n - 1:
                    cube[2] = [[cube[2][i][r] for i in range(self.n - 1, -1, -1)] for r in range(self.n)]

    def F(self, cube, history):
        self._side_rotation(self.n - 1, 1, cube)

        if history:
            if history[len(history) - 1] == "F":
                history.pop()
                history.append("F2")
            elif history[len(history) - 1] == "F2":
                history.pop()
                history.append("F'")
            elif history[len(history) - 1] == "F'":
                history.pop()
            else:
                history.append("F")
        else:
            history.append("F")

    def Fi(self, cube, history):
        self._side_rotation(self.n - 1, 0, cube)

        if history:
            if history[len(history) - 1] == "F":
                history.pop()
            elif history[len(history) - 1] == "F2":
                history.pop()
                history.append("F")
            elif history[len(history) - 1] == "F'":
                history.pop()
                history.append("F2")
            else:
                history.append("F'")
        else:
            history.append("F'")

    def L(self, cube, history):
        self._vertical_rotation(0, 0, cube)

        if history:
            if history[len(history) - 1] == "L":
                history.pop()
                history.append("L2")
            elif history[len(history) - 1] == "L2":
                history.pop()
                history.append("L'")
            elif history[len(history) - 1] == "L'":
                history.pop()
            else:
                history.append("L")
        else:
            history.append("L")

    def Li(self, cube, history):
        self._vertical_rotation(0, 1, cube)

        if history:
            if history[len(history) - 1] == "L":
                history.pop()
            elif history[len(history) - 1] == "L2":
                history.pop()
                history.append("L")
            elif history[len(history) - 1] == "L'":
                history.pop()
                history.append("L2")
            else:
                history.append("L'")
        else:
            history.append("L'")

    def B(self, cube, history):
        self._side_rotation(0, 0, cube)

        if history:
            if history[len(history) - 1] == "B":
                history.pop()
                history.append("B2")
            elif history[len(history) - 1] == "B2":
                history.pop()
                history.append("B'")
            elif history[len(history) - 1] == "B'":
                history.pop()
            else:
                history.append("B")
        else:
            history.append("B")

    def Bi(self, cube, history):
        self._side_rotation(0, 1, cube)

        if history:
            if history[len(history) - 1] == "B":
                history.pop()
            elif history[len(history) - 1] == "B2":
                history.pop()
                history.append("B")
            elif history[len(history) - 1] == "B'":
                history.pop()
                history.append("B2")
            else:
                history.append("B'")
        else:
            history.append("B'")

    def R(self, cube, history):
        self._vertical_rotation(self.n - 1, 1, cube)

        if history:
            if history[len(history) - 1] == "R":
                history.pop()
                history.append("R2")
            elif history[len(history) - 1] == "R2":
                history.pop()
                history.append("R'")
            elif history[len(history) - 1] == "R'":
                history.pop()
            else:
                history.append("R")
        else:
            history.append("R")

    def Ri(self, cube, history):
        self._vertical_rotation(self.n - 1, 0, cube)

        if history:
            if history[len(history) - 1] == "R":
                history.pop()
            elif history[len(history) - 1] == "R2":
                history.pop()
                history.append("R")
            elif history[len(history) - 1] == "R'":
                history.pop()
                history.append("R2")
            else:
                history.append("R'")
        else:
            history.append("R'")

    def U(self, cube, history):
        self._horizontal_rotation(0, 0, cube)

        if history:
            if history[len(history) - 1] == "U":
                history.pop()
                history.append("U2")
            elif history[len(history) - 1] == "U2":
                history.pop()
                history.append("U'")
            elif history[len(history) - 1] == "U'":
                history.pop()
            else:
                history.append("U")
        else:
            history.append("U")

    def Ui(self, cube, history):
        self._horizontal_rotation(0, 1, cube)

        if history:
            if history[len(history) - 1] == "U":
                history.pop()
            elif history[len(history) - 1] == "U2":
                history.pop()
                history.append("U")
            elif history[len(history) - 1] == "U'":
                history.pop()
                history.append("U2")
            else:
                history.append("U'")
        else:
            history.append("U'")

    def D(self, cube, history):
        self._horizontal_rotation(self.n - 1, 1, cube)

        if history:
            if history[len(history) - 1] == "D":
                history.pop()
                history.append("D2")
            elif history[len(history) - 1] == "D2":
                history.pop()
                history.append("D'")
            elif history[len(history) - 1] == "D'":
                history.pop()
            else:
                history.append("D")
        else:
            history.append("D")

    def Di(self, cube, history):
        self._horizontal_rotation(self.n - 1, 0, cube)

        if history:
            if history[len(history) - 1] == "D":
                history.pop()
            elif history[len(history) - 1] == "D2":
                history.pop()
                history.append("D")
            elif history[len(history) - 1] == "D'":
                history.pop()
                history.append("D2")
            else:
                history.append("D'")
        else:
            history.append("D'")

    def F2(self, cube, history):
        self.F(cube, history)
        self.F(cube, history)

    def R2(self, cube, history):
        self.R(cube, history)
        self.R(cube, history)

    def U2(self, cube, history):
        self.U(cube, history)
        self.U(cube, history)

    def B2(self, cube, history):
        self.B(cube, history)
        self.B(cube, history)

    def L2(self, cube, history):
        self.L(cube, history)
        self.L(cube, history)

    def D2(self, cube, history):
        self.D(cube, history)
        self.D(cube, history)

cube = RubikCube(state = "RGYWYWGYWBOOBRBYROYRRRGYWGWBBROOROWWGOYGBYROOGYBWWGBBG")
cube.show()
