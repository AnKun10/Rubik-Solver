from random import choice
from copy import deepcopy
from rubikcube import RubikCube, BFSBBCube
import twophase.solver as sv


class LayerByLayer(object):
    def __init__(self, cube):
        self.cube = cube

    def solve(self):
        self.FL()
        self.SL()
        self.TL()
        return self.cube.history

    def cross_FL(self):
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
        for s in range(6):
            for r in range(3):
                if s == 5:
                    if self._coordinate_to_color(neighbor_dict[(s, r, 1)]) != \
                            self.cube.cube[neighbor_dict[(s, r, 1)][0]][1][1] and (r == 0 or r == 2):
                        ans.append([s, r, 1])
                        found = True
                    elif self._coordinate_to_color(neighbor_dict[(s, 1, 0)]) != \
                            self.cube.cube[neighbor_dict[(s, 1, 0)][0]][1][1]:
                        ans.append([s, 1, 0])
                        found = True
                    elif self._coordinate_to_color(neighbor_dict[(s, 1, 2)]) != \
                            self.cube.cube[neighbor_dict[(s, 1, 2)][0]][1][1]:
                        ans.append([s, 1, 2])
                        found = True
                else:
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
        ans.append(neighbor_dict[tuple(ans[0])])
        return ans

    def FL(self):
        self.cross_FL()
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
                        elif neighbor_coord1[0] in centers and neighbor_coord2[0] not in centers:
                            if neighbor_coord1[0] == 1 and neighbor_coord2[0] == 4:
                                self.cube.Ui()
                            elif (neighbor_coord1[0] == 4 and neighbor_coord2[0] == 1) or (
                                    neighbor_coord1[0] < neighbor_coord2[0]):
                                self.cube.U()
                            elif neighbor_coord1[0] > neighbor_coord2[0]:
                                self.cube.Ui()
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
                        if goal_coord[1] == 2:
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

    def cross_TL(self):
        rneighbor_dict = {1: 2, 2: 3, 3: 4, 4: 1}
        rot_dict = {0: [self.cube.U, self.cube.U2, self.cube.Ui],
                    1: [self.cube.L, self.cube.L2, self.cube.Li],
                    2: [self.cube.F, self.cube.F2, self.cube.Fi],
                    3: [self.cube.R, self.cube.R2, self.cube.Ri],
                    4: [self.cube.B, self.cube.B2, self.cube.Bi],
                    5: [self.cube.D, self.cube.D2, self.cube.Di]}
        while True:
            rot_side = self._check_shape_TL(0)
            if rot_side == -1:
                break
            rot_steps = [rot_dict[rot_side][0], rot_dict[rneighbor_dict[rot_side]][0], self.cube.U,
                         rot_dict[rneighbor_dict[rot_side]][2], self.cube.Ui, rot_dict[rot_side][2]]
            for rot in rot_steps:
                rot()
        while True:
            if self._swap_edges_TL():
                break

    def _check_shape_TL(self, side=0):
        center = self.cube.cube[side][1][1]
        same_color_pieces = [(side, 1, 1)]
        # key = coordinate of an edge piece, value = return side to rotate
        return_side_dict = {(0, 0, 1): 4, (0, 1, 0): 1, (0, 1, 2): 3, (0, 2, 1): 2}
        edge_pieces = [(side, 0, 1), (side, 1, 0), (side, 1, 2), (side, 2, 1)]
        for piece in edge_pieces:
            if self._coordinate_to_color(piece) == center:
                same_color_pieces.append(piece)

        # dot shape = return 2, reverse L (stick) shape = return side that we can see reverse L (stick) shape, cross = return 2
        if len(same_color_pieces) == 1 or len(same_color_pieces) == 2:
            return 2
        elif len(same_color_pieces) == 5:
            return -1
        elif len(same_color_pieces) == 4:
            for piece in edge_pieces:
                if piece not in same_color_pieces:
                    return return_side_dict[piece]
        elif len(same_color_pieces) == 3:
            if same_color_pieces[1][1] == same_color_pieces[2][1] or same_color_pieces[1][2] == same_color_pieces[2][2]:
                for piece in edge_pieces:
                    if piece not in same_color_pieces:
                        return return_side_dict[piece]
            else:
                return_side_dict_new = {((0, 0, 1), (0, 1, 0)): 2, ((0, 1, 0), (0, 2, 1)): 3, ((0, 1, 2), (0, 2, 1)): 4,
                                        ((0, 0, 1), (0, 1, 2)): 1}
                return return_side_dict_new[tuple(same_color_pieces[1::])]

    def _swap_edges_TL(self):
        swap_dict = {(1, 2): 2, (2, 3): 3, (3, 4): 4, (1, 4): 1}
        rneighbor_dict = {1: 2, 2: 3, 3: 4, 4: 1}
        rot_dict = {0: [self.cube.U, self.cube.U2, self.cube.Ui],
                    1: [self.cube.L, self.cube.L2, self.cube.Li],
                    2: [self.cube.F, self.cube.F2, self.cube.Fi],
                    3: [self.cube.R, self.cube.R2, self.cube.Ri],
                    4: [self.cube.B, self.cube.B2, self.cube.Bi],
                    5: [self.cube.D, self.cube.D2, self.cube.Di]}
        right_pos_sides = []
        rot_side = -1
        while True:
            right_pos_counter = 0
            temp = []
            for s in range(1, 5):
                if self.cube.cube[s][1][1] == self.cube.cube[s][0][1]:
                    right_pos_counter += 1
                    temp.append(s)
            if right_pos_counter == 4:
                return True
            elif right_pos_counter >= 2:
                right_pos_sides = temp
                right_pos_sides.sort()
                break
            self.cube.U()
        if right_pos_sides == [1, 3] or right_pos_sides == [2, 4]:
            rot_side = right_pos_sides[0]
        else:
            temp = []
            for i in range(1, 5):
                if i not in right_pos_sides:
                    temp.append(i)
                if len(temp) == 2:
                    break
            rot_side = swap_dict[tuple(temp)]
        rot_steps = [rot_dict[rneighbor_dict[rot_side]][0], self.cube.U, rot_dict[rneighbor_dict[rot_side]][2],
                     self.cube.U, rot_dict[rneighbor_dict[rot_side]][0], self.cube.U2,
                     rot_dict[rneighbor_dict[rot_side]][2], self.cube.U]
        for rot in rot_steps:
            rot()
        return False

    def corner_TL(self):
        neighbor_dict = {1: [4, 2], 2: [1, 3], 3: [2, 4], 4: [3, 1]}
        rot_dict = {0: [self.cube.U, self.cube.U2, self.cube.Ui],
                    1: [self.cube.L, self.cube.L2, self.cube.Li],
                    2: [self.cube.F, self.cube.F2, self.cube.Fi],
                    3: [self.cube.R, self.cube.R2, self.cube.Ri],
                    4: [self.cube.B, self.cube.B2, self.cube.Bi],
                    5: [self.cube.D, self.cube.D2, self.cube.Di]}
        while True:
            right_pos_corners = self._check_right_pos_corners_TL(0)
            if len(right_pos_corners) == 4:
                break
            chosen_corner_coords = right_pos_corners[0]
            chosen_side = -1
            if neighbor_dict[chosen_corner_coords[1][0]][1] == chosen_corner_coords[2][0]:
                chosen_side = chosen_corner_coords[1][0]
            elif neighbor_dict[chosen_corner_coords[2][0]][1] == chosen_corner_coords[1][0]:
                chosen_side = chosen_corner_coords[2][0]
            rot_steps = [self.cube.U, rot_dict[neighbor_dict[chosen_side][1]][0], self.cube.Ui,
                         rot_dict[neighbor_dict[chosen_side][0]][2], self.cube.U,
                         rot_dict[neighbor_dict[chosen_side][1]][2], self.cube.Ui,
                         rot_dict[neighbor_dict[chosen_side][0]][0]]
            for rot in rot_steps:
                rot()
        self._orient_corners_TL(0)

    def _orient_corners_TL(self, side=0):
        if self.cube.solved():
            return
        center = self.cube.cube[side][1][1]
        corner_coords = [(side, 0, 0), (side, 0, 2), (side, 2, 0), (side, 2, 2)]
        opposite_side_dict = {0: 5, 1: 3, 2: 4, 3: 1, 4: 2, 5: 0}
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
        rot_dict = {0: [self.cube.U, self.cube.U2, self.cube.Ui],
                    1: [self.cube.L, self.cube.L2, self.cube.Li],
                    2: [self.cube.F, self.cube.F2, self.cube.Fi],
                    3: [self.cube.R, self.cube.R2, self.cube.Ri],
                    4: [self.cube.B, self.cube.B2, self.cube.Bi],
                    5: [self.cube.D, self.cube.D2, self.cube.Di]}
        rot_side = -1
        validate_coord = corner_coords[0]
        for coord in corner_coords:
            piece = self._coordinate_to_color(coord)
            if piece != center:
                validate_coord = coord
                neigbor_coords = neighbor_dict[coord]
                if neigbor_coords[0][2] == 0:
                    rot_side = neigbor_coords[0][0]
                elif neigbor_coords[1][2] == 0:
                    rot_side = neigbor_coords[1][0]
                break
        rot_steps = [rot_dict[rot_side][2], rot_dict[opposite_side_dict[side]][2], rot_dict[rot_side][0],
                     rot_dict[opposite_side_dict[side]][0]]
        right_corner_counter = 0
        while True:
            if right_corner_counter == 4:
                break
            if self._coordinate_to_color(validate_coord) == center:
                right_corner_counter += 1
                rot_dict[side][0]()
                continue
            for rot in rot_steps:
                rot()
        while True:
            if self.cube.cube[rot_side][1][1] != self.cube.cube[rot_side][0][0]:
                rot_dict[side][0]()
            else:
                break

    def _check_right_pos_corners_TL(self, side=0):
        right_pos_corners = []
        neighbor_dict = {(0, 0, 0): [[4, 0, 2], [1, 0, 0]], (1, 0, 0): [[0, 0, 0], [4, 0, 2]],
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
        # color of 3 pieces of corners
        for r in range(0, 3, 2):
            for c in range(0, 3, 2):
                neighbor_coord1, neighbor_coord2 = neighbor_dict[(side, r, c)][0], neighbor_dict[(side, r, c)][1]
                validate1 = [self.cube.cube[side][r][c], self._coordinate_to_color(neighbor_coord1),
                             self._coordinate_to_color(neighbor_coord2)]
                validate2 = [self.cube.cube[side][1][1], self.cube.cube[neighbor_coord1[0]][1][1],
                             self.cube.cube[neighbor_coord2[0]][1][1]]
                right_pos = True
                for piece in validate1:
                    if piece not in validate2:
                        right_pos = False
                        break
                if right_pos:
                    right_pos_corners.append([[side, r, c], neighbor_coord1, neighbor_coord2])
        if len(right_pos_corners) == 0:
            right_pos_corners.append([[side, 2, 2], neighbor_dict[(side, 2, 2)][0], neighbor_dict[(side, 2, 2)][1]])
        return right_pos_corners

    def TL(self):
        self.cross_TL()
        self.corner_TL()


class BFSBB(object):
    def __init__(self, cube):
        self.cube = cube
        # key = last rot_move, value = heuristic next rot_side
        self.next_rot_side_dict = {"U": [1, 2, 3, 4, 5], "U2": [1, 2, 3, 4, 5], "U'": [1, 2, 3, 4, 5],
                                   "L": [0, 2, 3, 4, 5], "L2": [0, 2, 3, 4, 5], "L'": [0, 2, 3, 4, 5],
                                   "F": [0, 1, 3, 4, 5], "F2": [0, 1, 3, 4, 5], "F'": [0, 1, 3, 4, 5],
                                   "R": [0, 1, 2, 4, 5], "R2": [0, 1, 2, 4, 5], "R'": [0, 1, 2, 4, 5],
                                   "B": [0, 1, 2, 3, 5], "B2": [0, 1, 2, 3, 5], "B'": [0, 1, 2, 3, 5],
                                   "D": [0, 1, 2, 3, 4], "D2": [0, 1, 2, 3, 4], "D'": [0, 1, 2, 3, 4]}
        # key = rot_side, value = possible rot_direction on that side
        self.rot_dict = {0: [self.cube.U, self.cube.U2, self.cube.Ui],
                         1: [self.cube.L, self.cube.L2, self.cube.Li],
                         2: [self.cube.F, self.cube.F2, self.cube.Fi],
                         3: [self.cube.R, self.cube.R2, self.cube.Ri],
                         4: [self.cube.B, self.cube.B2, self.cube.Bi],
                         5: [self.cube.D, self.cube.D2, self.cube.Di]}

        self.notion_to_rotation = {"U": self.cube.U, "U2": self.cube.U2, "U'": self.cube.Ui,
                                   "L": self.cube.L, "L2": self.cube.L2, "L'": self.cube.Li,
                                   "F": self.cube.F, "F2": self.cube.F2, "F'": self.cube.Fi,
                                   "R": self.cube.R, "R2": self.cube.R2, "R'": self.cube.Ri,
                                   "B": self.cube.B, "B2": self.cube.B2, "B'": self.cube.Bi,
                                   "D": self.cube.D, "D2": self.cube.D2, "D'": self.cube.Di}

    def _cal_g_cost(self, cur_cube):
        cost = 0
        for s in range(6):
            center = cur_cube[s][1][1]
            for r in range(len(cur_cube[s])):
                for c in range(len(cur_cube[s])):
                    if cur_cube[s][r][c] != center:
                        cost += 1
        return cost

    def _cal_h_cost(self, history):
        return len(history)

    def _get_cur_level_nodes(self, node_queue, level):
        """
        Get a list of all nodes in the given level and get the index of the next process node (last node in this list).
        :param node_queue: (list) contain all processing nodes
        :param level: (int) node's level to get from node_queue
        :return: (list) contains index of all nodes with given level in node_queue
        """
        cur_level_indexs = []
        for i in range(len(node_queue)):
            if node_queue[i][0] == level:
                cur_level_indexs.append(i)
        return cur_level_indexs

    def solve(self, node_queue=[]):
        """
        :param node_queue: (list) contains all processing nodes
        :return: (list) Solution steps
        """
        # cur_node[0] = current cube matrix; cur_node[1] = list of path moves; cur_node[2] = f(current node)
        if node_queue:
            cur_node = node_queue.pop()
            rot_sides = self.next_rot_side_dict[cur_node[1][len(cur_node[1]) - 1]]

            # Reach solved state
            if self._cal_g_cost(cur_node[0]) == 0:
                for rot in cur_node[1]:
                    self.notion_to_rotation[rot](self.cube.cube, self.cube.history)
                return cur_node[1]

            for i in range(3):
                for s in rot_sides:
                    cur_cube, history = deepcopy(cur_node[0]), deepcopy(cur_node[1])
                    self.rot_dict[s][i](cube=cur_cube, history=history)
                    next_node = [cur_cube, history,
                                 self._cal_g_cost(cur_cube) + self._cal_h_cost(history)]
                    node_queue.append(next_node)
                    # print(f"[{next_node[0], next_node[2], next_node[3]}]")

        else:
            cur_node = [self.cube.cube, [], self._cal_g_cost(self.cube.cube)]
            rot_sides = range(6)

            # Reach solved state
            if self._cal_g_cost(cur_node[0]) == 0:
                for rot in cur_node[1]:
                    self.notion_to_rotation[rot](self.cube.cube, self.cube.history)
                return cur_node[1]

            # Generate next level nodes
            for i in range(3):
                for s in rot_sides:
                    cur_cube, history = deepcopy(cur_node[0]), deepcopy(cur_node[1])
                    self.rot_dict[s][i](cube=cur_cube, history=history)
                    next_node = [cur_cube, history,
                                 self._cal_g_cost(cur_cube) + self._cal_h_cost(history)]
                    node_queue.append(next_node)
                    # print(f"[{next_node[0], next_node[2], next_node[3]}]")
        try:
            return self.solve(node_queue=sorted(node_queue, key=lambda x: x[2], reverse=True))
        except RecursionError:
            print("Maximum recursion depth exceeded.")


class Kociemba:
    def __init__(self, state):
        # Initialize a list of 6 sub-arrays for each face of the Rubik's Cube
        list_of_lists = [[] for _ in range(6)]
        for i in range(54):
            # Divide the string 'st' into sub-arrays of 9 characters and add them to list_of_lists
            list_of_lists[i // 9].append(state[i])

        # Reorder the sub-arrays according to a specific order
        od = [0, 3, 2, 5, 1, 4]
        new_list = ''
        self.state = ''
        self.step = 0
        dict = {'W': 'D', 'G': 'F', 'R': 'L', 'O': 'R', 'B': 'B', 'Y': 'U'}
        for i in od:
            for j in range(9):
                new_list += list_of_lists[i][j]
        for char in new_list:
            self.state += dict[char]

    def solve(self):
        sol = sv.solve(self.state)
        sol = sol.replace('3', "'")
        sol = sol.replace('1', "")
        solution = sol.split()
        solution.pop()
        self.step = len(solution)
        return solution