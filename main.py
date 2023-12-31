from solver import LayerByLayer, BFSBB, Kociemba
from rubikcube import RubikCube, BFSBBCube
from colordetection import ColorDetector
from copy import deepcopy


def detect_new_state():
    detector = ColorDetector()
    detector.color_detecting()
    return detector.state


def show_detector_notes():
    print("=============================== RUBIK COLOR DETECTOR ===============================")
    print("1, PRESS 't' TO CAPTURE A SIDE FACELETS' COLOR.")
    print("2, PRESS 's' TO SAVE THAT SIDE FACELETS' COLOR.")
    print("3, PRESS 'q' TO END DETECTING PROCESS.")
    print("====================================================================================")


def show_options():
    print("=============================== RUBIK CUBE SOLVER ===============================")
    print("1, COLOR DETECTING NEW RUBIK CUBE.")
    print("2, LAYER BY LAYER.")
    print("3, BFS & BB.")
    print("4, KOCIEMBA.")
    print("5, KORF.")
    print("0, QUIT.")
    print("=================================================================================")


def main():
    show_detector_notes()

    state = detect_new_state()
    cube = RubikCube(state=state)
    cube.show()
    solution = []

    show_options()
    while True:
        solver_choice = -1
        try:
            solver_choice = int(input("CHOOSE A SOLVER (INT): "))
        except ValueError:
            print("INVALID INPUT! PLEASE TRY AGAIN!")
        if solver_choice == 1:
            state = detect_new_state()
            cube = RubikCube(state=state)
            cube.show()
        elif solver_choice == 2:
            temp_cube = deepcopy(cube)
            solver = LayerByLayer(temp_cube)
            solution = solver.solve()
            print("SOLUTION: ", end="")
            for move in solution:
                print(move, end=" ")
        elif solver_choice == 3:
            temp_cube = BFSBBCube(state=state)
            solver = BFSBB(cube=cube)
            solution = solver.solve()
            print("SOLUTION: ", end="")
            for move in solution:
                print(move, end=" ")
        elif solver_choice == 4:
            solver = Kociemba(state=state)
            print("SOLUTION: ", end="")
            solver.solve()
        elif solver_choice == 0:
            break
        else:
            print("INVALID INPUT! PLEASE TRY AGAIN!")


if __name__ == "__main__":
    main()
