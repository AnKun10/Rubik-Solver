from rubikcube import RubikCube, BFSBBCube
import timeit
from solver import LayerByLayer, BFSBB, Kociemba

cube = RubikCube()

# while True:
#     rot_nums = []
#     try:
#         rot_nums = [int(x) for x in input("Number of rotations = ").split()]
#     except ValueError:
#         print("Invalid Input! Please Try again!")
#         continue
#     break
# configs = []
# rot_nums = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
#             2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
#             30, 30, 30, 30, 30, 30, 30, 30, 30, 30,
#             40, 40, 40, 40, 40, 40, 40, 40, 40, 40]
# f = open("test_set.txt", "w")
# for rot_num in rot_nums:
#     cube.shuffle(min_rot=rot_num, max_rot=rot_num)
#     configs.append(cube.state)
#     f.write(f"{rot_num} {cube.state}\n")
#     cube.reset()
# f.close()


def LBLTime(state):
    cube = RubikCube(state=state)
    solver = LayerByLayer(cube)
    start = timeit.default_timer()
    solver.solve()
    end = timeit.default_timer()
    return end - start


def BFSBBTime(state):
    cube = BFSBBCube(state=state)
    solver = BFSBB(cube)
    start = timeit.default_timer()
    solution = solver.solve()
    end = timeit.default_timer()
    if solution:
        return end - start
    return -1


def KociembaTime(state):
    solver = Kociemba(state=state)
    start = timeit.default_timer()
    solver.solve()
    end = timeit.default_timer()
    return end - start

def LBLLength(state):
    lbl_cube = RubikCube(state=state)
    solver = LayerByLayer(lbl_cube)
    solver.solve()
    print(lbl_cube.history)
    return len(lbl_cube.history)

def BFSBBLength(state):
    solver = BFSBB(BFSBBCube(state=state))
    solution = solver.solve()
    if solution:
        return len(solution)
    return -1

def KociembaLength(state):
    solver = Kociemba(state=state)
    return solver.solve()

# file = open("test_solution.txt", "w")
# f = open("test_set.txt", "r")
# for line in f.readlines():
#     rot_num, state = int(line.split()[0]), line.split()[1]
#     file.write(f"{rot_num} {LBLLength(state)} {BFSBBLength(state)}\n")
# file.close()
# f.close()
print(len(LayerByLayer(cube = RubikCube(state="WYYWYYWYYOOORRRRRRGBBGGBGGBRRROOOOOOGGBGBBGBBWWYWWYWWY")).solve()))