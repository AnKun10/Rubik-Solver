from copy import deepcopy
from collections import deque

def permu(List, cycle_chain, index):
    copied_list = List[:]
    mod = len(cycle_chain)
    for i in range(mod):
        new = (i + index) % mod
        List[cycle_chain[new]] = copied_list[cycle_chain[i]]

def flatten_nested_list(nested_list):
    result = []
    for item in nested_list:
        if callable(item):  # Check if it's a method
            result.append(item)
        elif isinstance(item, list):
            result.extend(flatten_nested_list(item))
    return result

from math import factorial

class PermutationIndexer:
    def __init__(self, N: int, K: int = None):
        if K is None:
            K = N
        self.N = N
        self.K = K
        # Precomputed table containing the number of ones in the binary
        # representation of each number. The largest N-bit number is
        # 2^N-1 = (1 << N) - 1.
        self.ones_count_lookup = [bin(i).count('1') for i in range(0, 2 ** N)]
        # Precomputed table of factorials (or "picks" if N != K). They're in
        # reverse order.
        self.factorials = [factorial(N - 1 - i) // factorial(N - K) for i in range(K)]

    def rank(self, perm) -> int:
        # This will hold the Lehmer code (in a factorial number system).
        lehmer = [0] * self.K
        # Set of "seen" digits in the permutation.
        seen = 0

        # The first digit of the Lehmer code is always the first digit of
        # the permutation.
        lehmer[0] = perm[0]
        # Mark the digit as seen (bitset uses right-to-left indexing).
        seen |= 1 << (self.N - 1 - perm[0])

        for i in range(1, self.K):
            seen |= 1 << (self.N - 1 - perm[i])
            # The number of "seen" digits to the left of this digit is the
            # count of ones left of this digit.
            num_ones = self.ones_count_lookup[seen >> (self.N - perm[i])]
            lehmer[i] = perm[i] - num_ones

        # Convert the Lehmer code to base-10.
        index = sum(lehmer[i] * self.factorials[i] for i in range(self.K))
        return index

class Korf_Cube():
    def __init__(self):
        #corner cubies
        self.corner = []
        #orientation of corner cubies
        self.corner_o = [None]*8
        #edge cubies
        self.edge = []
        #orientation of corner cubies
        self.edge_o = [None]*12

    def string_handle(self, state):
        colors = []
        for i in range(6):
            colors.append(state[4 + 9*i])
        #hash each color with a 2^i
        color_value = dict()
        color_value[colors[0]] = 2**4
        color_value[colors[-1]] = -2**4
        for i in range(1, 5):
            color_value[colors[i]] = 2**(i - 1)
        #then we can map each cubie with an unique number (called a value)
        value_corner = {
            25: 0,
            28: 1,
            22: 2,
            19: 3,
            -7: 4,
            -4: 5,
            -10: 6,
            -13: 7
        }
        value_edge = {
            24: 0,
            20: 1,
            18: 2,
            17: 3,
            9: 4,
            12: 5,
            6: 6,
            3: 7,
            -8: 8,
            -12: 9,
            -14: 10,
            -15: 11
        }

        self.corner = [[0, 9, 38], [2, 29, 36], [8, 20, 27], [6, 11, 18], [51, 15, 44], [53, 35, 42], [47, 26, 33], [45, 17, 24]]
        self.edge = [[1, 37], [5, 28], [7, 19], [3, 10], [12, 41], [32, 39], [30, 23], [14, 21], [52, 43], [50, 34], [46, 25], [48, 16]]
        #corner processing
        for i in range(8):
            #compute self.corner[i]
            corner_indices = deepcopy(self.corner[i])
            corner = [color_value[state[index]] for index in corner_indices]
            value = sum(_ for _ in corner)
            self.corner[i] = value_corner[value]
            
            #Now we compute self.corner_o[i]
            pivot = corner[0] #the side decides the orientation of the corner cubie
            if value > 0: #the corner belongs to UP side
                if pivot == 16:
                    self.corner_o[i] = 0
                else:
                    other_side = value - 16 - pivot
                    if (other_side + pivot) != 9: #don't fall into the case of L, B
                        if pivot > other_side:
                            self.corner_o[i] = 1
                        else:
                            self.corner_o[i] = 2
                    if (other_side + pivot) == 9: #falls into the case of L, B
                        if pivot > other_side:
                            self.corner_o[i] = 2
                        else:
                            self.corner_o[i] = 1
            elif value < 0: #the corner belongs to DOWN side
                if pivot == -16:
                    self.corner_o[i] = 0
                else:
                    other_side = value + 16 - pivot
                    if (other_side + pivot) != 9: #don't fall into the case of L, B
                        if pivot > other_side:
                            self.corner_o[i] = 2
                        else:
                            self.corner_o[i] = 1
                    if (other_side + pivot) == 9: #falls into the case of L, B
                        if pivot > other_side:
                            self.corner_o[i] = 1
                        else:
                            self.corner_o[i] = 2
        #edge processing
        for i in range(12):
            #compute self.edge[i]
            edge_indices = deepcopy(self.edge[i])
            edge = [color_value[state[index]] for index in edge_indices]
            value = sum(_ for _ in edge)
            self.edge[i] = value_edge[value]
            
            #Now we compute self.edge_o[i]
            pivot = edge[0] #the side decides the orientation of the edge cubie
            if 16 in edge: #the edge belongs to UP side
                if pivot == 16:
                    self.edge_o[i] = 0
                else:
                    self.edge_o[i] = 1
            elif -16 in edge: #the edge belongs to DOWN side
                if pivot == -16:
                    self.edge_o[i] = 0
                else:
                    self.edge_o[i] = 1
            else: #the edge belongs to the second floor
                if pivot == 1 or pivot == 4:
                    self.edge_o[i] = 0
                else:
                    self.edge_o[i] = 1

    def show(self):
        print(self.corner)
        print(self.corner_o)
        print(self.edge)
        print(self.edge_o)

        #Each state of a Rubik Cube was uniquely represented by 4 attributes above.
    def U(self):
        permu(self.corner, range(4), 1)
        permu(self.edge, range(4), 1)
        permu(self.corner_o, range(4), 1)
        permu(self.edge_o, range(4), 1)  

    def U2(self):
        permu(self.corner, range(4), 2)
        permu(self.edge, range(4), 2)
        permu(self.corner_o, range(4), 2)
        permu(self.edge_o, range(4), 2)  

    def Ui(self):
        permu(self.corner, range(4), -1)
        permu(self.edge, range(4), -1)
        permu(self.corner_o, range(4), -1)
        permu(self.edge_o, range(4), -1)  
    
    def D(self):
        permu(self.corner, [4, 5, 6, 7], -1)
        permu(self.edge, [8, 9, 10, 11], -1)
        permu(self.corner_o, [4, 5, 6, 7], -1)
        permu(self.edge_o, [8, 9, 10, 11], -1)  

    def D2(self):
        permu(self.corner, [4, 5, 6, 7], -2)
        permu(self.edge, [8, 9, 10, 11], -2)
        permu(self.corner_o, [4, 5, 6, 7], -2)
        permu(self.edge_o, [8, 9, 10, 11], -2)  

    def Di(self):
        permu(self.corner, [4, 5, 6, 7], 1)
        permu(self.edge, [8, 9, 10, 11], 1)
        permu(self.corner_o, [4, 5, 6, 7], 1)
        permu(self.edge_o, [8, 9, 10, 11], 1)  

    
    def F(self):
        permu(self.corner, [3, 2, 6, 7], 1)
        permu(self.edge, [2, 6, 10, 7], 1)
        permu(self.edge_o, [2, 6, 10, 7], 1)
        corner_o = self.corner_o[:]
        self.corner_o[6] = (corner_o[2] + 1) % 3
        self.corner_o[7] = (corner_o[6] + 2) % 3
        self.corner_o[3] = (corner_o[7] + 1) % 3
        self.corner_o[2] = (corner_o[3] + 2) % 3

    def F2(self):
        permu(self.corner, [3, 2, 6, 7], 2)
        permu(self.edge, [2, 6, 10, 7], 2)
        permu(self.edge_o, [2, 6, 10, 7], 2)
        corner_o = self.corner_o[:]
        self.corner_o[6] = corner_o[3]
        self.corner_o[3] = corner_o[6]
        self.corner_o[7] = corner_o[2]
        self.corner_o[2] = corner_o[7]

    def Fi(self):
        permu(self.corner, [3, 2, 6, 7], -1)
        permu(self.edge, [2, 6, 10, 7], -1)
        permu(self.edge_o, [2, 6, 10, 7], -1)
        corner_o = self.corner_o[:]
        self.corner_o[2] = (corner_o[6] + 2) % 3
        self.corner_o[7] = (corner_o[3] + 2) % 3
        self.corner_o[3] = (corner_o[2] + 1) % 3
        self.corner_o[6] = (corner_o[7] + 1) % 3

    def B(self):
        permu(self.corner, [1, 0, 4, 5], 1) 
        permu(self.edge, [0, 4, 8, 5], 1)
        permu(self.edge_o, [0, 4, 8, 5], 1)
        corner_o = self.corner_o[:]
        self.corner_o[4] = (corner_o[0] + 1) % 3     
        self.corner_o[5] = (corner_o[4] + 2) % 3
        self.corner_o[1] = (corner_o[5] + 1) % 3
        self.corner_o[0] = (corner_o[1] + 2) % 3

    def B2(self):
        permu(self.corner, [1, 0, 4, 5], 2) 
        permu(self.edge, [0, 4, 8, 5], 2)
        permu(self.edge_o, [0, 4, 8, 5], 2)
        corner_o = self.corner_o[:]
        self.corner_o[1] = corner_o[4]
        self.corner_o[4] = corner_o[1]
        self.corner_o[0] = corner_o[5]
        self.corner_o[5] = corner_o[0]

    def Bi(self):
        permu(self.corner, [1, 0, 4, 5], -1) 
        permu(self.edge, [0, 4, 8, 5], -1)
        permu(self.edge_o, [0, 4, 8, 5], -1)
        corner_o = self.corner_o[:]
        self.corner_o[0] = (corner_o[4] + 2) % 3     
        self.corner_o[4] = (corner_o[5] + 1) % 3
        self.corner_o[5] = (corner_o[1] + 2) % 3
        self.corner_o[1] = (corner_o[0] + 1) % 3

    def R(self):
        permu(self.corner, [2, 1, 5, 6], 1)
        permu(self.edge, [1, 5, 9, 6], 1)
        corner_o = self.corner_o[:]
        self.corner_o[1] = (corner_o[2] + 2) % 3
        self.corner_o[5] = (corner_o[1] + 1) % 3
        self.corner_o[6] = (corner_o[5] + 2) % 3
        self.corner_o[2] = (corner_o[6] + 1) % 3

        edge_o = self.edge_o[:]
        self.edge_o[1] = (edge_o[6] + 1) % 2
        self.edge_o[5] = (edge_o[1] + 1) % 2
        self.edge_o[9] = (edge_o[5] + 1) % 2
        self.edge_o[6] = (edge_o[9] + 1) % 2

    def R2(self):
        permu(self.corner, [2, 1, 5, 6], 2)
        permu(self.edge, [1, 5, 9, 6], 2)
        corner_o = self.corner_o[:]
        self.corner_o[1] = corner_o[6]
        self.corner_o[6] = corner_o[1]
        self.corner_o[2] = corner_o[5]
        self.corner_o[5] = corner_o[2]

        edge_o = self.edge_o[:]
        self.edge_o[1] = edge_o[9]
        self.edge_o[9] = edge_o[1]
        self.edge_o[5] = edge_o[6]
        self.edge_o[6] = edge_o[5] 

    def Ri(self):
        permu(self.corner, [2, 1, 5, 6], -1)
        permu(self.edge, [1, 5, 9, 6], -1)
        corner_o = self.corner_o[:]
        self.corner_o[2] = (corner_o[1] + 1) % 3
        self.corner_o[6] = (corner_o[2] + 2) % 3
        self.corner_o[5] = (corner_o[6] + 1) % 3
        self.corner_o[1] = (corner_o[5] + 2) % 3

        edge_o = self.edge_o[:]
        self.edge_o[6] = (edge_o[1] + 1) % 2
        self.edge_o[9] = (edge_o[6] + 1) % 2
        self.edge_o[5] = (edge_o[9] + 1) % 2
        self.edge_o[1] = (edge_o[5] + 1) % 2
        
    def L(self):
        permu(self.corner, [0, 3, 7, 4], 1) 
        permu(self.edge, [3, 7, 11, 4], 1)
        corner_o = self.corner_o[:]
        self.corner_o[3] = (corner_o[0] + 2) % 3
        self.corner_o[7] = (corner_o[3] + 1) % 3
        self.corner_o[4] = (corner_o[7] + 2) % 3
        self.corner_o[0] = (corner_o[4] + 1) % 3

        edge_o = self.edge_o[:]
        self.edge_o[7] = (edge_o[3] + 1) % 2
        self.edge_o[11] = (edge_o[7] + 1) % 2
        self.edge_o[4] = (edge_o[11] + 1) % 2
        self.edge_o[3] = (edge_o[4] + 1) % 2

    def L2(self):
        permu(self.corner, [0, 3, 7, 4], 2)
        permu(self.edge, [3, 7, 11, 4], 2)
        corner_o = self.corner_o[:]
        self.corner_o[0] = corner_o[7]
        self.corner_o[7] = corner_o[0]
        self.corner_o[3] = corner_o[4]
        self.corner_o[4] = corner_o[3]

        edge_o = self.edge_o[:]
        self.edge_o[3] = edge_o[11]
        self.edge_o[11] = edge_o[3]
        self.edge_o[7] = edge_o[4]
        self.edge_o[4] = edge_o[7] 

    def Li(self):
        permu(self.corner, [0, 3, 7, 4], -1)
        permu(self.edge, [3, 7, 11, 4], -1)
        corner_o = self.corner_o[:]
        self.corner_o[0] = (corner_o[3] + 1) % 3
        self.corner_o[4] = (corner_o[0] + 2) % 3
        self.corner_o[7] = (corner_o[4] + 1) % 3
        self.corner_o[3] = (corner_o[7] + 2) % 3

        edge_o = self.edge_o[:]
        self.edge_o[3] = (edge_o[7] + 1) % 2
        self.edge_o[4] = (edge_o[3] + 1) % 2
        self.edge_o[11] = (edge_o[4] + 1) % 2
        self.edge_o[7] = (edge_o[11] + 1) % 2

class GenerateDB:
    """The abstract class for a formal problem. You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions."""

    def __init__(self):
        #number of database's elements
        self.length = None
        #number of indexed elements
        self.indexed = None
        self.lookup_table = []
        solved_state = "y"*9 + "r"*9 + "g"*9 + "o"*9 + "b"*9 + "w"*9
        initial_state = Korf_Cube()
        initial_state.string_handle(solved_state)
        self.initial = Node(initial_state)
        
    def goal_test(self):
        """Return True if the state is a goal. """
        if self.length and self.indexed:
            if self.indexed > self.length:
                raise ValueError("Number of indexed state should not be greater than length")
            else:
                return self.indexed == self.length

class CornerDB(GenerateDB):
    def __init__(self):
        super().__init__()
        self.length = 88179840 # = 8!*3^7 the number of cases to be generated
        self.lookup_table = [None]*88179840


        
class Node:
    def __init__(self, state: Korf_Cube, parent = None, action = None, depth = 0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = depth
        if parent:
            self.depth = parent.depth + 1
        self.child = []

    def expand(self):
        """List the nodes reachable in one step from this node.
        Twisting the same face twice in a row is redundant.
        Furthermore, twists of opposite faces of the cube are independent and commutative.
        We choose this order when there are two opposite consecutive moves.
        F --> B, L --> R, U --> D"""
        #list of all moves
        MoveList = [[Korf_Cube.F, Korf_Cube.F2, Korf_Cube.Fi], [Korf_Cube.B, Korf_Cube.B2, Korf_Cube.Bi], [Korf_Cube.L, Korf_Cube.L2, Korf_Cube.Li], [Korf_Cube.R, Korf_Cube.R2, Korf_Cube.Ri], [Korf_Cube.U, Korf_Cube.U2, Korf_Cube.Ui], [Korf_Cube.D, Korf_Cube.D2, Korf_Cube.Di]] 
        FeasibleMoveList = deepcopy(MoveList)
        for index in range(6):
            if self.action in MoveList[index]:
                FeasibleMoveList.pop(index)
                if index % 2 == 1:
                    FeasibleMoveList.pop(index - 1)
                break
        FeasibleMoveList = flatten_nested_list(FeasibleMoveList) #flatten the FeasibleMoveList
        for move in FeasibleMoveList:
            child_node = Node(deepcopy(self.state), self, move, self.depth + 1)
            move(child_node.state)
            self.child.append(child_node)
        return self.child   

    # We want for a queue of nodes in breadth_first_graph_search or
    # A_star_search to have no duplicated states, so we treat nodes
    # with the same state as equal. 


def breadth_first_corner_search(problem: CornerDB):
    frontier = deque([problem.initial])
    corner_permu_ranking = PermutationIndexer(8)
    while frontier:
        node = frontier.popleft()
        corner_permu_rank = corner_permu_ranking.rank(node.state.corner)
        corner_index = (3**7)*corner_permu_rank
        for i in range(7):
            corner_index += node.state.corner_o[i]*(3**i)
        if problem.lookup_table[corner_index] == None:
            problem.lookup_table[corner_index] = node.depth
            print(f"{corner_index}: {node.depth}")
            if problem.goal_test():
                return
            else:
                for child in node.expand():
                    if child not in frontier:
                        frontier.append(child)
  
    return None
class EdgeDB(GenerateDB):
    def __init__(self):
        super().__init__()
        self.length = 510935040 # = 2^7*12!/5! the number of cases to be generated
        self.lookup_table_first = [None]*510935040 #first 7 edges
        self.lookup_table_last = [None]*510935040 #last 7 edges
        self.indexed_first = 0
        self.indexed_last = 0
    def goal_test(self):
        """Return True if the state is a goal."""
        return (self.indexed_first == self.length) and (self.indexed_last == self.length)

def depth_limited_search(problem, limit = 21):
    """[Figure 3.17]"""

    def recursive_dls(node, problem, limit):
        if problem.goal_test(node.state):
            return node
        elif limit == 0:
            return 'cutoff'
        else:
            cutoff_occurred = False
            for child in node.expand(problem):
                result = recursive_dls(child, problem, limit - 1)
                if result == 'cutoff':
                    cutoff_occurred = True
                elif result is not None:
                    return result
            return 'cutoff' if cutoff_occurred else None

    # Body of depth_limited_search:
    return recursive_dls(Node(problem.initial), problem, limit)


def iterative_deepening_search(problem):
    """[Figure 3.18]"""
    for depth in range(21):
        result = depth_limited_search(problem, depth)
        if result != 'cutoff':
            return result


def main():
    MoveList = [[Korf_Cube.F, Korf_Cube.F2, Korf_Cube.Fi], [Korf_Cube.B, Korf_Cube.B2, Korf_Cube.Bi], [Korf_Cube.L, Korf_Cube.L2, Korf_Cube.Li], [Korf_Cube.R, Korf_Cube.R2, Korf_Cube.Ri], [Korf_Cube.U, Korf_Cube.U2, Korf_Cube.Ui], [Korf_Cube.D, Korf_Cube.D2, Korf_Cube.Di]]
    MoveList = flatten_nested_list(MoveList)
    for move in MoveList:
        a = Korf_Cube()
        a.string_handle("y"*9 + "r"*9 + "g"*9 + "o"*9 + "b"*9 + "w"*9)
        print(move)
        move(a)
        a.show()
    
    indexer1 = PermutationIndexer(8)
    print(indexer1.rank([0, 1, 3, 4, 7, 5, 6, 2]))
    
    problem = CornerDB()
    breadth_first_corner_search(problem)

if __name__ == "__main__":
    main()
