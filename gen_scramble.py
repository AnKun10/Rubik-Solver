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
configs = []
rot_nums = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
            4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
            5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
            7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
            10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
            20, 20, 20, 20, 20, 20, 20, 20, 20, 20,
            50, 50, 50, 50, 50, 50, 50, 50, 50, 50,
            80, 80, 80, 80, 80, 80, 80, 80, 80, 80,
            100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
f = open("test_set.txt", "w")
for rot_num in rot_nums:
    cube.shuffle(min_rot=rot_num, max_rot=rot_num)
    configs.append(cube.state)
    f.write(f"{rot_num} {cube.state}\n")
    cube.reset()
f.close()


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


file = open("test_solution.txt", "w")
f = open("")