from random import choice
from copy import deepcopy
from rubikcube import RubikCube


class LayerByLayer(object):
    def __init__(self, cube):
        self.cube = cube
        self.neighbor_dict = {(0, 0, 1): [4, 0, 1], (4, 0, 1): [0, 0, 1],
                              (0, 1, 0): [1, 0, 1], (1, 0, 1): [0, 1, 0],
                              (0, 2, 1): [2, 0, 1], (2, 0, 1): [0, 2, 1],
                              (0, 1, 2): [3, 0, 1], (3, 0, 1): [0, 1, 2],
                              (1, 1, 0): [4, 1, 2], (4, 1, 2): [1, 1, 0],
                              (1, 1, 2): [2, 1, 0], (2, 1, 0): [1, 1, 2],
                              (2, 1, 2): [3, 1, 0], (3, 1, 0): [2, 1, 2],
                              (3, 1, 2): [4, 1, 0], (4, 1, 0): [3, 1, 2],
                              (5, 0, 1): [2, 2, 1], (2, 2, 1): [5, 0, 1],
                              (5, 1, 0): [1, 2, 1], (1, 2, 1): [5, 1, 0],
                              (5, 1, 2): [3, 2, 1], (3, 2, 1): [5, 1, 2],
                              (5, 2, 1): [4, 2, 1], (4, 2, 1): [5, 2, 1]}

    def cross(self):
        down_center = self.cube.cube[5][1][1]
        rot_dict = {0: [self.cube.U, self.cube.U2, self.cube.Ui],
                    1: [self.cube.L, self.cube.L2, self.cube.Li],
                    2: [self.cube.F, self.cube.F2, self.cube.Fi],
                    3: [self.cube.R, self.cube.R2, self.cube.Ri],
                    4: [self.cube.B, self.cube.B2, self.cube.Bi],
                    5: [self.cube.D, self.cube.D2, self.cube.Di]}
        while True:
            if self._validate_cross(side=5):
                break
            edge_coordinates = self._find_edge(down_center)
            goal_coordinate, neighbor_coordinate = edge_coordinates[0], edge_coordinates[1]
            goal_piece, neighbor_piece = down_center, self._coordinate_to_color(neighbor_coordinate)
            if goal_coordinate[0] != 0 and goal_coordinate[0] != 5:
                row, column = goal_coordinate[1], goal_coordinate[2]
                if row == 2:
                    rot_dict[goal_coordinate[0]][1]()
                elif row == 1:
                    if neighbor_piece == self.cube.cube[neighbor_coordinate[0]][1][1]:
                        if column == 0:
                            rot_dict[neighbor_coordinate[0]][0]()
                        elif column == 2:
                            rot_dict[neighbor_coordinate[0]][2]()
                    else:
                        for s in range(1, 5):
                            center = self.cube.cube[s][1][1]
                            if center == neighbor_piece:
                                rot_num = s - neighbor_coordinate[0]
                                if column == 0:
                                    rot_dict[neighbor_coordinate[0]][2]()
                                elif column == 2:
                                    rot_dict[neighbor_coordinate[0]][0]()

                                if rot_num == 1 or rot_num == -3:
                                    self.cube.Ui()
                                elif rot_num == 2 or rot_num == -2:
                                    self.cube.U2()
                                elif rot_num == -1 or rot_num == 3:
                                    self.cube.U()

                                if column == 0:
                                    rot_dict[neighbor_coordinate[0]][0]()
                                elif column == 2:
                                    rot_dict[neighbor_coordinate[0]][2]()

                                rot_dict[s][1]()
                                break
                elif row == 0:
                    for s in range(1, 5):
                        center = self.cube.cube[s][1][1]
                        if center == neighbor_piece:
                            rot_num = s - goal_coordinate[0]
                            if rot_num == 0:
                                self.cube.U()
                                if s == 1:
                                    rot_dict[4][0]()
                                    rot_dict[s][2]()
                                    rot_dict[4][2]()
                                else:
                                    rot_dict[s - 1][0]()
                                    rot_dict[s][2]()
                                    rot_dict[s - 1][2]()
                            elif rot_num == 1 or rot_num == -3:
                                rot_dict[goal_coordinate[0]][0]()
                                rot_dict[s][2]()
                                rot_dict[goal_coordinate[0]][2]()
                            elif rot_num == 2 or rot_num == -2:
                                self.cube.U()
                                rot_dict[goal_coordinate[0]][0]()
                                rot_dict[s][2]()
                                rot_dict[goal_coordinate[0]][2]()
                            elif rot_num == -1 or rot_num == 3:
                                rot_dict[goal_coordinate[0]][2]()
                                rot_dict[s][0]()
                                rot_dict[goal_coordinate[0]][0]()

                            break
            elif goal_coordinate[0] == 0:
                for s in range(1, 5):
                    center = self.cube.cube[s][1][1]
                    if center == neighbor_piece:
                        rot_num = s - neighbor_coordinate[0]
                        if rot_num == 1 or rot_num == -3:
                            self.cube.Ui()
                        elif rot_num == 2 or rot_num == -2:
                            self.cube.U2()
                        elif rot_num == -1 or rot_num == 3:
                            self.cube.U()
                        rot_dict[s][1]()
                        break
            elif goal_coordinate[0] == 5:
                for s in range(1, 5):
                    center = self.cube.cube[s][1][1]
                    if center == neighbor_piece:
                        rot_num = s - neighbor_coordinate[0]
                        if rot_num == 1 or rot_num == -3:
                            rot_dict[neighbor_coordinate[0]][1]()
                            self.cube.Ui()
                            rot_dict[s][1]()
                        elif rot_num == 2 or rot_num == -2:
                            rot_dict[neighbor_coordinate[0]][1]()
                            self.cube.U2()
                            rot_dict[s][1]()
                        elif rot_num == -1 or rot_num == 3:
                            rot_dict[neighbor_coordinate[0]][1]()
                            self.cube.U()
                            rot_dict[s][1]()
                        break

    def _validate_cross(self, side):
        color = self.cube.cube[side][1][1]
        neighbor_dict = {0: [1, 2, 3, 4], 1: [0, 2, 4, 5], 2: [0, 1, 3, 5], 3: [0, 2, 4, 5], 4: [0, 1, 3, 5],
                         5: [1, 2, 3, 4]}
        neighbor_sides = neighbor_dict[side]
        if (self.cube.cube[side][0][1] == color and self.cube.cube[side][1][0] == color and self.cube.cube[side][1][
            2] == color and self.cube.cube[side][2][1] == color) and (
                self.cube.cube[neighbor_sides[0]][2][1] == self.cube.cube[neighbor_sides[0]][1][1] and
                self.cube.cube[neighbor_sides[1]][2][1] == self.cube.cube[neighbor_sides[1]][1][1] and
                self.cube.cube[neighbor_sides[2]][2][1] == self.cube.cube[neighbor_sides[2]][1][1] and
                self.cube.cube[neighbor_sides[3]][2][1] == self.cube.cube[neighbor_sides[3]][1][1]):
            return True
        return False

    def _coordinate_to_color(self, coord):
        s = coord[0]
        r = coord[1]
        c = coord[2]
        return self.cube.cube[s][r][c]

    def _find_edge(self, color):
        """
        :param color: edge color to find
        :return: (list) 2 coordinates of edge piece
        """
        # ans[0] = coordinate of given color edge piece; ans[1] = coordinate of neighbor edge piece
        ans = []
        found = False
        for s in range(6):
            for r in range(3):
                if self.cube.cube[s][r][1] == color and (r == 0 or r == 2):
                    ans.append([s, r, 1])
                    found = True
                elif self.cube.cube[s][1][0] == color:
                    ans.append([s, 1, 0])
                    found = True
                elif self.cube.cube[s][1][2] == color:
                    ans.append([s, 1, 2])
                    found = True
                if found:
                    break
            if found:
                break
        ans.append(self.neighbor_dict[tuple(ans[0])])
        return ans


cube = RubikCube(state="215205401501312522012124014034033343341042531350555442")
cube.show()
print("--------------------------------")

solver = LayerByLayer(cube=cube)
solver.cross()
cube.show()

print("--------------------------------")
cube.show_history()
