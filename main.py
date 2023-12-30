from solver import LayerByLayer
from rubikcube import RubikCube
from colordetection import ColorDetector

if __name__ == "__main__":
    detector = ColorDetector()
    detector.color_detecting()

    state = detector.state
    cube = RubikCube(state=state)
    cube.show()

    solver = LayerByLayer(cube=cube)
    solver.solve()
    cube.show()
    cube.show_history()
