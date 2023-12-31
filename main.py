from solver import LayerByLayer, BFSBB, Kociemba
from rubikcube import RubikCube, BFSBBCube
from colordetection import ColorDetector


def main():
    detector = ColorDetector()
    detector.color_detecting()

    state = detector.state
    cube = RubikCube(state=state)
    cube.show()
    solution = []

    while True:
        solver_choice = -1
        print("=============================== RUBIK CUBE SOLVER ===============================")
        print("1, LAYER BY LAYER.")
        print("2, BFS & BB.")
        print("3, KOCIEMBA.")
        print("4, KORF.")
        print("0, QUIT.")
        print("=================================================================================")
        try:
            solver_choice = int(input("CHOOSE A SOLVER (INT): "))
        except ValueError:
            print("INVALID INPUT! PLEASE TRY AGAIN!")
        if solver_choice == 1:
            solver = LayerByLayer(cube)
            solution = solver.solve()
            print("SOLUTION: ", end="")
            for move in solution:
                print(move, end=" ")
            break
        elif solver_choice == 2:
            cube = BFSBBCube(state=state)
            solver = BFSBB(cube=cube)
            solution = solver.solve()
            print("SOLUTION: ", end="")
            for move in solution:
                print(move, end=" ")
            break
        elif solver_choice == 3:
            solver = Kociemba(state=state)
            solver.solve()
            break
        elif solver_choice == 0:
            break
        else:
            print("INVALID INPUT! PLEASE TRY AGAIN!")

if __name__ == "__main__":
    main()
