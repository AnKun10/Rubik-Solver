# **Rubik's Cube Solver**

## Overview

The **Rubik's Cube Solver** project is designed to detect the colors of a Rubik's Cube and implement four distinct solving algorithms: Layer by Layer, BFS & BB (Breadth-First Search & Bi-Directional BFS), Kociemba, and Koft. These algorithms are implemented in Python. Subsequently, the project evaluates and compares the effectiveness of these algorithms in solving the Rubik's Cube.

## Usage

### Installation of Required Libraries

To install the necessary libraries, execute the following command:

```bash
pip install -r requirements.txt
```

Run file main.py.
From the UI screen, you have 2 options:
  - Use your camera to detect the state of the shuffled Rubik's Cube 
  - You can directly type the cube definition string. A solved cube has the string 'UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB'


FIND SOLVER FOR EXAMPLE STATE:
INPUT:
```bash
GOYBYYYYYWRRRRRGRBGGGGGGYGROOOOOOWYOBWRBBYBBWRWBWWBOWW
```

```bash
KOCIEMBA'S SOLUTION: F1 L2 U2 F1 R2 F1 D2 R1 F3 U2 F2 D2 L2 B3 L2 B1 D2 B1 (18f)
```

