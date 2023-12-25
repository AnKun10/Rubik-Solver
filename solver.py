from random import choice
from copy import deepcopy
from rubikcube import RubikCube


class LayerByLayer(object):
    def __init__(self, cube):
        self.cube = cube
        # history = list of resolved rotations
        self.history = []

    def form_cross(self):
        center_piece = self.cube.cube[5][1][1]
        for _ in range(4):
            s, r, c = self.find_edge(center_piece)
            if s != 5 and s != 0:
                if r == 2:
                    match s:
                        case 1:
                            neighbor_edge = self.cube.cube[5][1][0]
                            for side in range(1, 5):
                                if self.cube.cube[side][1][1] == neighbor_edge:
                                    # side-1 = D rotation direction (1: D F2, 0: L2, 3: Di B2, 2: D2 R2)
                                    match side - 1:
                                        case 0:
                                            self.cube.L2()
                                            self.history.append("L2")
                                            r = 0
                                        case 1:
                                            self.cube.D()
                                            self.cube.F2()
                                            self.history.append("D")
                                            self.history.append("F2")
                                            r, s = 0, 2
                                        case 2:
                                            self.cube.D2()
                                            self.cube.R2()
                                            self.history.append("D2")
                                            self.history.append("R2")
                                            r, s = 0, 3
                                        case 3:
                                            self.cube.Di()
                                            self.cube.B2()
                                            self.history.append("D'")
                                            self.history.append("B2")
                                            r, s = 0, 4
                                    break
                        case 2:
                            neighbor_edge = self.cube.cube[5][0][1]
                            for side in range(1, 5):
                                if self.cube.cube[side][1][1] == neighbor_edge:
                                    # side-2 = D rotation direction (-1: Di L2, 0: F2, 1: D R2, 2: D2 B2)
                                    match side - 2:
                                        case -1:
                                            self.cube.Di()
                                            self.cube.L2()
                                            self.history.append("D'")
                                            self.history.append("L2")
                                            r, s = 0, 1
                                        case 0:
                                            self.cube.F2()
                                            self.history.append("F2")
                                            r = 0
                                        case 1:
                                            self.cube.D()
                                            self.cube.R2()
                                            self.history.append("D")
                                            self.history.append("R2")
                                            r, s = 0, 3
                                        case 2:
                                            self.cube.D2()
                                            self.cube.B2()
                                            self.history.append("D2")
                                            self.history.append("B2")
                                            r, s = 0, 4
                                    break
                        case 3:
                            neighbor_edge = self.cube.cube[5][1][2]
                            for side in range(1, 5):
                                if self.cube.cube[side][1][1] == neighbor_edge:
                                    # side-3 = D rotation direction (-2: D2 L2, -1: Di F2, 0: R2, 1: D B2)
                                    match side - 3:
                                        case -2:
                                            self.cube.D2()
                                            self.cube.L2()
                                            self.history.append("D2")
                                            self.history.append("L2")
                                            r, s = 0, 1
                                        case -1:
                                            self.cube.Di()
                                            self.cube.F2()
                                            self.history.append("D'")
                                            self.history.append("F2")
                                            r, s = 0, 2
                                        case 0:
                                            self.cube.R2()
                                            self.history.append("R2")
                                            r = 0
                                        case 1:
                                            self.cube.D()
                                            self.cube.B2()
                                            self.history.append("D")
                                            self.history.append("B2")
                                            r, s = 0, 4
                                    break
                        case 4:
                            neighbor_edge = self.cube.cube[5][2][1]
                            for side in range(1, 5):
                                if self.cube.cube[side][1][1] == neighbor_edge:
                                    # side-4 = D rotation direction (-3: D L2, -2: D2 F2, -1: Di R2, 0: B2)
                                    match side - 4:
                                        case -3:
                                            self.cube.D()
                                            self.cube.L2()
                                            self.history.append("D")
                                            self.history.append("L2")
                                            r, s = 0, 1
                                        case -2:
                                            self.cube.D2()
                                            self.cube.F2()
                                            self.history.append("D2")
                                            self.history.append("F2")
                                            r, s = 0, 2
                                        case -1:
                                            self.cube.Di()
                                            self.cube.R2()
                                            self.history.append("D'")
                                            self.history.append("R2")
                                            r, s = 0, 3
                                        case 0:
                                            self.cube.B2()
                                            self.history.append("B2")
                                            r = 0
                                    break
                if r == 1:
                    match c:
                        case 0:
                            side_notions = {1: [self.cube.Li, "L'", self.cube.L, "L", 1, 0], 2: [self.cube.Fi, "F'", self.cube.F, "F", 2, 1], 3: [self.cube.Ri, "R'", self.cube.R, "R", 1, 2], 4: [self.cube.Bi, "B'", self.cube.B, "B", 0, 1]}
                            if s == 1:
                                neighbor_edge = self.cube.cube[4][1][2]
                                side_notions[4][0]()
                                self.cube.U()
                                side_notions[4][2]()
                                self.history.append(side_notions[4][1])
                                self.history.append("U")
                                self.history.append(side_notions[4][3])
                                r, c = side_notions[4][4], side_notions[4][5]
                            else:
                                neighbor_edge = self.cube.cube[s-1][1][2]
                                side_notions[s-1][0]()
                                self.cube.U()
                                side_notions[s-1][2]()
                                self.history.append(side_notions[s-1][1])
                                self.history.append("U")
                                self.history.append(side_notions[s-1][3])
                                r, c = side_notions[s-1][4], side_notions[s-1][5]
                        case 2:
                            side_notions = {1: [self.cube.Li, "L'", self.cube.L, "L", 1, 0], 2: [self.cube.Fi, "F'", self.cube.F, "F", 2, 1], 3: [self.cube.Ri, "R'", self.cube.R, "R", 1, 2], 4: [self.cube.Bi, "B'", self.cube.B, "B", 0, 1]}
                            if s == 4:
                                neighbor_edge = self.cube.cube[1][1][0]
                                side_notions[1][2]()
                                self.cube.U()
                                side_notions[1][0]()
                                self.history.append(side_notions[1][3])
                                self.history.append("U")
                                self.history.append(side_notions[1][1])
                                r, c = side_notions[1][4], side_notions[1][5]
                            else:
                                neighbor_edge = self.cube.cube[s+1][1][0]
                                side_notions[s+1][2]()
                                self.cube.U()
                                side_notions[s+1][0]()
                                self.history.append(side_notions[s+1][3])
                                self.history.append("U")
                                self.history.append(side_notions[s+1][1])
                                r, c = side_notions[s+1][4], side_notions[s+1][5]
                    s = 0
                if r == 0:
                    match s:
                        case 1:
                            neighbor_edge = self.cube.cube[0][1][0]
                            for side in range(1, 5):
                                if self.cube.cube[side][1][1] == neighbor_edge:
                                    # side-1 = U rotation direction (0: U B Li Bi, 1: Ui (U L Fi Li), 2: U2 (U F Ri Fi), 3: U (U R Bi Ri))
                                    match side - 1:
                                        case 0:
                                            self.cube.U()
                                            self.cube.B()
                                            self.cube.Li()
                                            self.cube.Bi()
                                            self.history.append("U")
                                            self.history.append("B")
                                            self.history.append("L'")
                                            self.history.append("B'")
                                        case 1:
                                            self.cube.L()
                                            self.cube.Fi()
                                            self.cube.Li()
                                            self.history.append("L")
                                            self.history.append("F'")
                                            self.history.append("L'")
                                        case 2:
                                            self.cube.Ui()
                                            self.cube.F()
                                            self.cube.Ri()
                                            self.cube.Fi()
                                            self.history.append("U'")
                                            self.history.append("F")
                                            self.history.append("R'")
                                            self.history.append("F'")
                                        case 3:
                                            self.cube.U2()
                                            self.cube.R()
                                            self.cube.Bi()
                                            self.cube.Ri()
                                            self.history.append("U2")
                                            self.history.append("R")
                                            self.history.append("B'")
                                            self.history.append("R'")
                                    break
                        case 2:
                            neighbor_edge = self.cube.cube[0][2][1]
                            for side in range(1, 5):
                                if self.cube.cube[side][1][1] == neighbor_edge:
                                    # side-2 = U rotation direction (-1: U (U B Li Bi), 0: U L Fi Li, 1: Ui (U F Ri Fi), 2: U2 (U R Bi Ri))
                                    match side - 2:
                                        case -1:
                                            self.cube.U2()
                                            self.cube.B()
                                            self.cube.Li()
                                            self.cube.Bi()
                                            self.history.append("U2")
                                            self.history.append("B")
                                            self.history.append("L'")
                                            self.history.append("B'")
                                        case 0:
                                            self.cube.U()
                                            self.cube.L()
                                            self.cube.Fi()
                                            self.cube.Li()
                                            self.history.append("U")
                                            self.history.append("L")
                                            self.history.append("F'")
                                            self.history.append("L'")
                                        case 1:
                                            self.cube.F()
                                            self.cube.Ri()
                                            self.cube.Fi()
                                            self.history.append("F")
                                            self.history.append("R'")
                                            self.history.append("F'")
                                        case 2:
                                            self.cube.Ui()
                                            self.cube.R()
                                            self.cube.Bi()
                                            self.cube.Ri()
                                            self.history.append("U'")
                                            self.history.append("R")
                                            self.history.append("B'")
                                            self.history.append("R'")
                                    break
                        case 3:
                            neighbor_edge = self.cube.cube[0][1][2]
                            for side in range(1, 5):
                                if self.cube.cube[side][1][1] == neighbor_edge:
                                    # side-3 = U rotation direction (-2: U2 (U B Li Bi), -1: U (U L Fi Li), 0: U F Ri Fi, 1: Ui (U R Bi Ri))
                                    match side - 3:
                                        case -2:
                                            self.cube.Ui()
                                            self.cube.B()
                                            self.cube.Li()
                                            self.cube.Bi()
                                            self.history.append("U'")
                                            self.history.append("B")
                                            self.history.append("L'")
                                            self.history.append("B'")
                                        case -1:
                                            self.cube.U2()
                                            self.cube.L()
                                            self.cube.Fi()
                                            self.cube.Li()
                                            self.history.append("U2")
                                            self.history.append("L")
                                            self.history.append("F'")
                                            self.history.append("L'")
                                        case 0:
                                            self.cube.U()
                                            self.cube.F()
                                            self.cube.Ri()
                                            self.cube.Fi()
                                            self.history.append("U")
                                            self.history.append("F")
                                            self.history.append("R'")
                                            self.history.append("F'")
                                        case 1:
                                            self.cube.R()
                                            self.cube.Bi()
                                            self.cube.Ri()
                                            self.history.append("R")
                                            self.history.append("B'")
                                            self.history.append("R'")
                                    break
                        case 4:
                            neighbor_edge = self.cube.cube[0][0][1]
                            for side in range(1, 5):
                                if self.cube.cube[side][1][1] == neighbor_edge:
                                    # side-4 = U rotation direction (-3: Ui (U B Li Bi), -2: U2 (U L Fi Li), -1: U (U F Ri Fi), 0: U R Bi Ri)
                                    match side - 4:
                                        case -3:
                                            self.cube.B()
                                            self.cube.Li()
                                            self.cube.Bi()
                                            self.history.append("B")
                                            self.history.append("L'")
                                            self.history.append("B'")
                                        case -2:
                                            self.cube.Ui()
                                            self.cube.L()
                                            self.cube.Fi()
                                            self.cube.Li()
                                            self.history.append("U'")
                                            self.history.append("L")
                                            self.history.append("F'")
                                            self.history.append("L'")
                                        case -1:
                                            self.cube.U2()
                                            self.cube.F()
                                            self.cube.Ri()
                                            self.cube.Fi()
                                            self.history.append("U2")
                                            self.history.append("F")
                                            self.history.append("R'")
                                            self.history.append("F'")
                                        case 0:
                                            self.cube.U()
                                            self.cube.R()
                                            self.cube.Bi()
                                            self.cube.Ri()
                                            self.history.append("U")
                                            self.history.append("R")
                                            self.history.append("B'")
                                            self.history.append("R'")
                                    break
            if s == 5:
                match r:
                    case 0:
                        # neighbor_edge = the 2nd color of the edge
                        neighbor_edge = self.cube.cube[2][2][1]
                        for side in range(1, 5):
                            if self.cube.cube[side][1][1] == neighbor_edge:
                                # side-2 = D rotation direction (-1: Di, 0: N/A, 1: D, 2: D2)
                                match side-2:
                                    case -1:
                                        self.cube.Di()
                                        self.history.append("D'")
                                    case 1:
                                        self.cube.D()
                                        self.history.append("D")
                                    case 2:
                                        self.cube.D2()
                                        self.history.append("D2")
                                break
                    case 1:
                        if c == 0:
                            neighbor_edge = self.cube.cube[1][2][1]
                            for side in range(1, 5):
                                if self.cube.cube[side][1][1] == neighbor_edge:
                                    # side-1 = D rotation direction (3: Di, 0: N/A, 1: D, 2: D2)
                                    match side - 1:
                                        case 1:
                                            self.cube.D()
                                            self.history.append("D")
                                        case 2:
                                            self.cube.D2()
                                            self.history.append("D2")
                                        case 3:
                                            self.cube.Di()
                                            self.history.append("D'")
                                    break
                        elif c == 2:
                            neighbor_edge = self.cube.cube[3][2][1]
                            for side in range(1, 5):
                                if self.cube.cube[side][1][1] == neighbor_edge:
                                    # side-3 = D rotation direction (-1: Di, 0: N/A, 1: D, -2: D2)
                                    match side - 3:
                                        case -1:
                                            self.cube.Di()
                                            self.history.append("D'")
                                        case -2:
                                            self.cube.D2()
                                            self.history.append("D2")
                                        case 1:
                                            self.cube.D()
                                            self.history.append("D")
                                    break
                    case 2:
                        neighbor_edge = self.cube.cube[4][2][1]
                        for side in range(1, 5):
                            if self.cube.cube[side][1][1] == neighbor_edge:
                                # side-4 = D rotation direction (-1: Di, 0: N/A, -3: D, -2: D2)
                                match side - 4:
                                    case -1:
                                        self.cube.Di()
                                        self.history.append("D'")
                                    case -2:
                                        self.cube.D2()
                                        self.history.append("D2")
                                    case -3:
                                        self.cube.D()
                                        self.history.append("D")
                                break
            elif s == 0:
                match r:
                    case 0:
                        neighbor_edge = self.cube.cube[4][0][1]
                        for side in range(1, 5):
                            if self.cube.cube[side][1][1] == neighbor_edge:
                                # side-4 = U rotation direction (-1: U R2, 0: B2, -3: Ui L2, -2: U2 F2)
                                match side - 4:
                                    case -3:
                                        self.cube.Ui()
                                        self.cube.L2()
                                        self.history.append("U'")
                                        self.history.append("L2")
                                    case -2:
                                        self.cube.U2()
                                        self.cube.F2()
                                        self.history.append("U2")
                                        self.history.append("F2")
                                    case -1:
                                        self.cube.U()
                                        self.cube.R2()
                                        self.history.append("U")
                                        self.history.append("R2")
                                    case 0:
                                        self.cube.B2()
                                        self.history.append("B2")
                                break
                    case 1:
                        if c == 0:
                            neighbor_edge = self.cube.cube[1][0][1]
                            for side in range(1, 5):
                                if self.cube.cube[side][1][1] == neighbor_edge:
                                    # side-1 = U rotation direction (3: U B2, 0: L2, 1: Ui F2, 2: U2 R2)
                                    match side - 1:
                                        case 0:
                                            self.cube.L2()
                                            self.history.append("L2")
                                        case 1:
                                            self.cube.Ui()
                                            self.cube.F2()
                                            self.history.append("U'")
                                            self.history.append("F2")
                                        case 2:
                                            self.cube.U2()
                                            self.cube.R2()
                                            self.history.append("U2")
                                            self.history.append("R2")
                                        case 3:
                                            self.cube.U()
                                            self.cube.B2()
                                            self.history.append("U")
                                            self.history.append("B2")
                                    break
                        elif c == 2:
                            neighbor_edge = self.cube.cube[3][0][1]
                            for side in range(1, 5):
                                if self.cube.cube[side][1][1] == neighbor_edge:
                                    # side-1 = U rotation direction (-1: U R2, 0: R2, 1: Ui F2, -2: U2 R2)
                                    match side - 3:
                                        case -2:
                                            self.cube.U2()
                                            self.cube.L2()
                                            self.history.append("U2")
                                            self.history.append("L2")
                                        case -1:
                                            self.cube.U()
                                            self.cube.F2()
                                            self.history.append("U")
                                            self.history.append("F2")
                                        case 0:
                                            self.cube.R2()
                                            self.history.append("R2")
                                        case 1:
                                            self.cube.Ui()
                                            self.cube.B2()
                                            self.history.append("U'")
                                            self.history.append("B2")
                                    break
                    case 2:
                        neighbor_edge = self.cube.cube[2][0][1]
                        for side in range(1, 5):
                            if self.cube.cube[side][1][1] == neighbor_edge:
                                # side-2 = U rotation direction (-1: U L2, 0: F2, 1: Ui R2, 2: U2 B2)
                                match side - 2:
                                    case 1:
                                        self.cube.Ui()
                                        self.cube.R2()
                                        self.history.append("U'")
                                        self.history.append("R2")
                                    case 2:
                                        self.cube.U2()
                                        self.cube.B2()
                                        self.history.append("U2")
                                        self.history.append("B2")
                                    case -1:
                                        self.cube.U()
                                        self.cube.L2()
                                        self.history.append("U")
                                        self.history.append("L2")
                                    case 0:
                                        self.cube.F2()
                                        self.history.append("F2")
                                break





    # Return coordinate of the first edge with given color
    def find_edge(self, color):
        for s in range(len(self.cube.cube)):
            for r in range(self.cube.n):
                if r % 2 == 0 and self.cube.cube[s][r][1] == color:
                    return s, r, 1
                elif r % 2 != 0:
                    if self.cube.cube[s][r][0] == color:
                        return s, r, 0
                    elif self.cube.cube[s][r][2] == color:
                        return s, r, 2
