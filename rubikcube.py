from random import randint, choice
from math import sqrt


class RubikCube:
    def __init__(self, n=3, colors=['w', 'o', 'g', 'r', 'b', 'y'], state=None):
        """
        Initializes a new Rubik Cube
        :param n: (int) size of the nxn Rubik Cube
        :param colors: (list) contain all the colors of the Rubik Cube
        :param state: (string) current state of the Rubik Cube (ex: "rrrwrwrgryrywwwwrwbrbggggggwowyyyyyygygbbbbbbooobooooo")
        """
        if state:
            self.n = int(sqrt(len(state) / 6))
            self.colors = []
            for c in state:
                if c not in self.colors:
                    self.colors.append(c)
                if len(self.colors) == 6:
                    break
            self.cube = [[[c for c in state[r + s:r + s + self.n]] for r in range(0, self.n ** 2, self.n)] for s in
                         range(0, len(state), 6)]
        else:
            self.n = n
            self.colors = colors
            self.reset()

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
        actions = [('h', 0), ('h', 1), ('v', 0), ('v', 1), ('s', 0), ('s', 1)]
        for i in range(rot_num):
            a = choice(actions)
            r = randint(0, self.n - 1)
            if a[0] == 'h':
                self.horizontal_rotation(r, a[1])
            elif a[0] == 'v':
                self.vertical_rotation(r, a[1])
            elif a[0] == 's':
                self.side_rotation(r, a[1])

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

    def U2(self):
        self.U()
        self.U()

    def Ui(self):
        self._horizontal_rotation(0, 1)

    def L(self):
        self._vertical_rotation(0, 0)

    def L2(self):
        self.L()
        self.L()

    def Li(self):
        self._vertical_rotation(0, 1)

    def F(self):
        self._side_rotation(self.n - 1, 1)

    def F2(self):
        self.F()
        self.F()

    def Fi(self):
        self._side_rotation(self.n - 1, 0)

    def R(self):
        self._vertical_rotation(self.n - 1, 1)

    def R2(self):
        self.R()
        self.R()

    def Ri(self):
        self._vertical_rotation(self.n - 1, 0)

    def B(self):
        self._side_rotation(0, 0)

    def B2(self):
        self.B()
        self.B()

    def Bi(self):
        self._side_rotation(0, 1)

    def D(self):
        self._horizontal_rotation(self.n - 1, 1)

    def D2(self):
        self.D()
        self.D()

    def Di(self):
        self._horizontal_rotation(self.n - 1, 0)

cube = RubikCube(state="111111111222222222333333333444444444555555555666666666")
cube.reset()
cube.show()
print("---------------------------------------------------------")
cube.D()
cube.show()
