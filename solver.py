from random import choice
from copy import deepcopy
from rubikcube import RubikCube


class LayerByLayer(object):
    def __init__(self, cube):
        self.cube = cube

    def solve(self):
        self.FL()
        self.SL()

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
            edge_coordinates = self._find_edge_FL(down_center)
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

    def _find_edge_FL(self, color):
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
        neighbor_dict = {(0, 0, 1): [4, 0, 1], (4, 0, 1): [0, 0, 1],
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
        ans.append(neighbor_dict[tuple(ans[0])])
        return ans

    def FL(self):
        self.cross()
        down_center = self.cube.cube[5][1][1]
        rot_dict = {0: [self.cube.U, self.cube.U2, self.cube.Ui],
                    1: [self.cube.L, self.cube.L2, self.cube.Li],
                    2: [self.cube.F, self.cube.F2, self.cube.Fi],
                    3: [self.cube.R, self.cube.R2, self.cube.Ri],
                    4: [self.cube.B, self.cube.B2, self.cube.Bi],
                    5: [self.cube.D, self.cube.D2, self.cube.Di]}
        while True:
            if self._validate_corners(5):
                break
            corner_coordinates = self._find_corner(down_center)
            goal_coord, neighbor_coord1, neighbor_coord2 = corner_coordinates[0], corner_coordinates[1], \
                corner_coordinates[2]
            goal_piece, neighbor_piece1, neighbor_piece2 = down_center, self._coordinate_to_color(
                neighbor_coord1), self._coordinate_to_color(neighbor_coord2)

            side, row, column = goal_coord[0], goal_coord[1], goal_coord[2]
            if side == 0:
                corner_dict = {(1, 2): [0, 2, 0], (2, 3): [0, 2, 2], (3, 4): [0, 0, 2], (1, 4): [0, 0, 0]}
                centers = []
                for s in range(1, 5):
                    if self.cube.cube[s][1][1] == neighbor_piece1 or self.cube.cube[s][1][1] == neighbor_piece2:
                        centers.append(s)
                    if len(centers) == 2:
                        if neighbor_coord1[0] not in centers and neighbor_coord2[0] not in centers:
                            self.cube.U2()
                        elif neighbor_coord1[0] not in centers and neighbor_coord2[0] in centers:
                            if neighbor_coord1[0] == 1 and neighbor_coord2[0] == 4:
                                self.cube.U()
                            elif (neighbor_coord1[0] == 4 and neighbor_coord2[0] == 1) or (
                                    neighbor_coord1[0] < neighbor_coord2[0]):
                                self.cube.Ui()
                            elif neighbor_coord1[0] > neighbor_coord2[0]:
                                self.cube.U()
                        break
                right_pos = corner_dict[(min(centers), max(centers))]
                if right_pos[2] == 0:
                    rot_side = 1
                    rot_dir = 2
                    if right_pos[1] == 0:
                        rot_dir = 0
                    rot_dict[rot_side][rot_dir]()
                    rot_dict[0][2 - rot_dir]()
                    rot_dict[rot_side][2 - rot_dir]()
                elif right_pos[2] == 2:
                    rot_side = 3
                    rot_dir = 2
                    if right_pos[1] == 2:
                        rot_dir = 0
                    rot_dict[rot_side][rot_dir]()
                    rot_dict[0][2 - rot_dir]()
                    rot_dict[rot_side][2 - rot_dir]()
                continue
            elif side == 5:
                if neighbor_piece1 != self.cube.cube[neighbor_coord1[0]][1][1] or neighbor_piece2 != \
                        self.cube.cube[neighbor_coord2[0]][1][1]:
                    if goal_coord[2] == 0:
                        rot_side = 1
                        rot_dir = 2
                        if rot_dir[1] == 2:
                            rot_dir = 0
                        rot_dict[rot_side][rot_dir]()
                        rot_dict[0][rot_dir]()
                        rot_dict[rot_side][2 - rot_dir]()
                    elif goal_coord[2] == 2:
                        rot_side = 3
                        rot_dir = 2
                        if goal_coord[1] == 0:
                            rot_dir = 0
                        rot_dict[rot_side][rot_dir]()
                        rot_dict[0][rot_dir]()
                        rot_dict[rot_side][2 - rot_dir]()
                continue
            else:
                if row == 2:
                    rot_dir = 2
                    if column == 0:
                        rot_dir = 0
                    rot_dict[side][rot_dir]()
                    rot_dict[0][rot_dir]()
                    rot_dict[side][2 - rot_dir]()
                    continue
            rot_coord = neighbor_coord1
            rot_side = self._color_to_side(neighbor_piece2)
            if neighbor_coord1[0] not in range(1, 5):
                rot_coord = neighbor_coord2
                rot_side = self._color_to_side(neighbor_piece1)
            for s in range(1, 5):
                if self._coordinate_to_color(rot_coord) == self.cube.cube[s][1][1]:
                    rot_num = s - rot_coord[0]
                    if rot_num == 1 or rot_num == -3:
                        self.cube.Ui()
                    elif rot_num == -2 or rot_num == 2:
                        self.cube.U2()
                    elif rot_num == -1 or rot_num == 3:
                        self.cube.U()
            if rot_coord[2] == 0:
                rot_dict[rot_side][2]()
                self.cube.Ui()
                rot_dict[rot_side][0]()
            elif rot_coord[2] == 2:
                rot_dict[rot_side][0]()
                self.cube.U()
                rot_dict[rot_side][2]()

    def _color_to_side(self, color):
        """
        Find the right side of given piece
        :param color: the given color piece
        :return: the right side of the given color piece
        """
        for s in range(6):
            center = self.cube.cube[s][1][1]
            if center == color:
                return s
        return None

    def _find_corner(self, color):
        """
        :param color: given color to find
        :return: (list) list of corner coordinates
        """
        # ans[0] = coordinate of the first corner found with given color
        # ans[1], ans[2] = coordinates of 2 neighbor corners
        ans = []
        found = False
        neighbor_dict = {(0, 0, 0): [[1, 0, 0], [4, 0, 2]], (1, 0, 0): [[0, 0, 0], [4, 0, 2]],
                         (4, 0, 2): [[0, 0, 0], [1, 0, 0]],
                         (0, 0, 2): [[3, 0, 2], [4, 0, 0]], (3, 0, 2): [[0, 0, 2], [4, 0, 0]],
                         (4, 0, 0): [[0, 0, 2], [3, 0, 2]],
                         (0, 2, 0): [[1, 0, 2], [2, 0, 0]], (1, 0, 2): [[0, 2, 0], [2, 0, 0]],
                         (2, 0, 0): [[0, 2, 0], [1, 0, 2]],
                         (0, 2, 2): [[2, 0, 2], [3, 0, 0]], (2, 0, 2): [[0, 2, 2], [3, 0, 0]],
                         (3, 0, 0): [[0, 2, 2], [2, 0, 2]],
                         (5, 0, 0): [[1, 2, 2], [2, 2, 0]], (1, 2, 2): [[2, 2, 0], [5, 0, 0]],
                         (2, 2, 0): [[1, 2, 2], [5, 0, 0]],
                         (5, 0, 2): [[2, 2, 2], [3, 2, 0]], (2, 2, 2): [[3, 2, 0], [5, 0, 2]],
                         (3, 2, 0): [[2, 2, 2], [5, 0, 2]],
                         (5, 2, 0): [[1, 2, 0], [4, 2, 2]], (1, 2, 0): [[4, 2, 2], [5, 2, 0]],
                         (4, 2, 2): [[1, 2, 0], [5, 2, 0]],
                         (5, 2, 2): [[3, 2, 2], [4, 2, 0]], (3, 2, 2): [[4, 2, 0], [5, 2, 2]],
                         (4, 2, 0): [[3, 2, 2], [5, 2, 2]]}
        for s in range(1, 5):
            if self.cube.cube[s][0][0] == color:
                ans.append([s, 0, 0])
                found = True
                break
            elif self.cube.cube[s][0][2] == color:
                ans.append([s, 0, 2])
                found = True
                break
        if not found:
            for s in range(1, 5):
                if self.cube.cube[s][2][0] == color:
                    ans.append([s, 2, 0])
                    found = True
                    break
                elif self.cube.cube[s][2][2] == color:
                    ans.append([s, 2, 2])
                    found = True
                    break
        if not found:
            if self.cube.cube[0][0][0] == color:
                ans.append([0, 0, 0])
                found = True
            elif self.cube.cube[0][0][2] == color:
                ans.append([0, 0, 2])
                found = True
            elif self.cube.cube[0][2][0] == color:
                ans.append([0, 2, 0])
                found = True
            elif self.cube.cube[0][2][2] == color:
                ans.append([0, 2, 2])
                found = True
        if not found:
            if self._coordinate_to_color(neighbor_dict[(5, 0, 0)][0]) != \
                    self.cube.cube[neighbor_dict[(5, 0, 0)][0][0]][1][1]:
                ans.append([5, 0, 0])
            elif self._coordinate_to_color(neighbor_dict[(5, 0, 2)][0]) != \
                    self.cube.cube[neighbor_dict[(5, 0, 2)][0][0]][1][1]:
                ans.append([5, 0, 2])
            elif self._coordinate_to_color(neighbor_dict[(5, 2, 0)][0]) != \
                    self.cube.cube[neighbor_dict[(5, 2, 0)][0][0]][1][1]:
                ans.append([5, 2, 0])
            elif self._coordinate_to_color(neighbor_dict[(5, 2, 2)][0]) != \
                    self.cube.cube[neighbor_dict[(5, 2, 2)][0][0]][1][1]:
                ans.append([5, 2, 2])

        ans.append(neighbor_dict[tuple(ans[0])][0])
        ans.append(neighbor_dict[tuple(ans[0])][1])
        return ans

    def _validate_corners(self, side):
        validate = True
        neighbor_dict = {(0, 0, 0): [[1, 0, 0], [4, 0, 2]], (1, 0, 0): [[0, 0, 0], [4, 0, 2]],
                         (4, 0, 2): [[0, 0, 0], [1, 0, 0]],
                         (0, 0, 2): [[3, 0, 2], [4, 0, 0]], (3, 0, 2): [[0, 0, 2], [4, 0, 0]],
                         (4, 0, 0): [[0, 0, 2], [3, 0, 2]],
                         (0, 2, 0): [[1, 0, 2], [2, 0, 0]], (1, 0, 2): [[0, 2, 0], [2, 0, 0]],
                         (2, 0, 0): [[0, 2, 0], [1, 0, 2]],
                         (0, 2, 2): [[2, 0, 2], [3, 0, 0]], (2, 0, 2): [[0, 2, 2], [3, 0, 0]],
                         (3, 0, 0): [[0, 2, 2], [2, 0, 2]],
                         (5, 0, 0): [[1, 2, 2], [2, 2, 0]], (1, 2, 2): [[2, 2, 0], [5, 0, 0]],
                         (2, 2, 0): [[1, 2, 2], [5, 0, 0]],
                         (5, 0, 2): [[2, 2, 2], [3, 2, 0]], (2, 2, 2): [[3, 2, 0], [5, 0, 2]],
                         (3, 2, 0): [[2, 2, 2], [5, 0, 2]],
                         (5, 2, 0): [[1, 2, 0], [4, 2, 2]], (1, 2, 0): [[4, 2, 2], [5, 2, 0]],
                         (4, 2, 2): [[1, 2, 0], [5, 2, 0]],
                         (5, 2, 2): [[3, 2, 2], [4, 2, 0]], (3, 2, 2): [[4, 2, 0], [5, 2, 2]],
                         (4, 2, 0): [[3, 2, 2], [5, 2, 2]]}
        center = self.cube.cube[side][1][1]
        if self.cube.cube[side][0][0] != center or self.cube.cube[side][0][2] != center or self.cube.cube[side][2][
            0] != center or self.cube.cube[side][2][2] != center:
            return False
        neighbor_coordinates = [neighbor_dict[(side, 0, 0)], neighbor_dict[(side, 0, 2)], neighbor_dict[(side, 2, 0)],
                                neighbor_dict[(side, 2, 2)]]
        for neighbor in neighbor_coordinates:
            for coord in neighbor:
                side = coord[0]
                color = self._coordinate_to_color(coord)
                if color != self.cube.cube[side][1][1]:
                    return False
        return True

    def SL(self):
        up_center = self.cube.cube[0][1][1]
        neighbor_dict = {1: [4, 2], 2: [1, 3], 3: [2, 4], 4: [3, 1]}
        rot_dict = {0: [self.cube.U, self.cube.U2, self.cube.Ui],
                    1: [self.cube.L, self.cube.L2, self.cube.Li],
                    2: [self.cube.F, self.cube.F2, self.cube.Fi],
                    3: [self.cube.R, self.cube.R2, self.cube.Ri],
                    4: [self.cube.B, self.cube.B2, self.cube.Bi],
                    5: [self.cube.D, self.cube.D2, self.cube.Di]}
        while True:
            if self._validate_SL():
                break
            edge_coordinates = self._find_edge_SL(up_center)
            edge_coord1, edge_coord2 = edge_coordinates[0], edge_coordinates[1]
            edge_piece1, edge_piece2 = self._coordinate_to_color(edge_coord1), self._coordinate_to_color(edge_coord2)
            if edge_coord1[0] == 0:
                for s in range(1, 5):
                    if self.cube.cube[s][1][1] == edge_piece2:
                        rot_num = s - edge_coord2[0]
                        if rot_num == 1 or rot_num == -3:
                            self.cube.Ui()
                        elif rot_num == 2 or rot_num == -2:
                            self.cube.U2()
                        elif rot_num == -1 or rot_num == 3:
                            self.cube.U()
                        if self.cube.cube[neighbor_dict[s][0]][1][1] == edge_piece1:
                            lrot_steps = [self.cube.Ui, rot_dict[neighbor_dict[s][0]][2], self.cube.U,
                                          rot_dict[neighbor_dict[s][0]][0], self.cube.U, rot_dict[s][0], self.cube.Ui,
                                          rot_dict[s][2]]
                            for rot in lrot_steps:
                                rot()
                        elif self.cube.cube[neighbor_dict[s][1]][1][1] == edge_piece1:
                            rrot_steps = [self.cube.U, rot_dict[neighbor_dict[s][1]][0], self.cube.Ui,
                                          rot_dict[neighbor_dict[s][1]][2], self.cube.Ui, rot_dict[s][2], self.cube.U,
                                          rot_dict[s][0]]
                            for rot in rrot_steps:
                                rot()
                        break
            else:
                lrot_steps = [rot_dict[edge_coord2[0]][0], self.cube.U, rot_dict[edge_coord2[0]][2], self.cube.Ui,
                              rot_dict[edge_coord1[0]][2], self.cube.Ui, rot_dict[edge_coord1[0]][0], self.cube.U]
                for rot in lrot_steps:
                    rot()

    def _find_edge_SL(self, avoid_color):
        """
        Find the first edge that doesn't have the given color
        :param avoid_color: color to avoid
        :return: (list) list of edge coordinates that doesn't have the given color
        """
        ans = []
        neighbor_dict = {(0, 0, 1): [4, 0, 1], (4, 0, 1): [0, 0, 1],
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
        found = False
        if self.cube.cube[0][1][0] != avoid_color and self._coordinate_to_color(
                neighbor_dict[(0, 1, 0)]) != avoid_color:
            ans.append([0, 1, 0])
            ans.append(neighbor_dict[(0, 1, 0)])
            found = True
        elif self.cube.cube[0][0][1] != avoid_color and self._coordinate_to_color(
                neighbor_dict[(0, 0, 1)]) != avoid_color:
            ans.append([0, 0, 1])
            ans.append(neighbor_dict[(0, 0, 1)])
            found = True
        elif self.cube.cube[0][1][2] != avoid_color and self._coordinate_to_color(
                neighbor_dict[(0, 1, 2)]) != avoid_color:
            ans.append([0, 1, 2])
            ans.append(neighbor_dict[(0, 1, 2)])
            found = True
        elif self.cube.cube[0][2][1] != avoid_color and self._coordinate_to_color(
                neighbor_dict[(0, 2, 1)]) != avoid_color:
            ans.append([0, 2, 1])
            ans.append(neighbor_dict[(0, 2, 1)])
            found = True
        if not found:
            for s in range(1, 5):
                if (self.cube.cube[s][1][0] != self.cube.cube[s][1][1] or self._coordinate_to_color(
                        neighbor_dict[(s, 1, 0)]) != self.cube.cube[neighbor_dict[(s, 1, 0)][0]][1][1]) and (
                        self.cube.cube[s][1][0] != avoid_color and self._coordinate_to_color(
                    neighbor_dict[(s, 1, 0)]) != avoid_color):
                    ans.append(neighbor_dict[(s, 1, 0)])
                    ans.append([s, 1, 0])
                    break
        return ans

    def _validate_SL(self):
        for s in range(1, 5):
            center = self.cube.cube[s][1][1]
            if self.cube.cube[s][1][0] != center or self.cube.cube[s][1][2] != center:
                return False
        return True


cube = RubikCube(state="414502430143410240551125320250130133325441501204352532")
solver = LayerByLayer(cube=cube)
print("------------------------------------------------")
solver.FL()
cube.show()
print("------------------------------------------------")
solver.SL()
cube.show()
print("------------------------------------------------")
cube.show_history()
