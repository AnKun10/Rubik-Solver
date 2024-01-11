# **Rubik's Cube Solver**

## Table of Contents
* [Overview](#overview)
* [Usage](#usage)
* [Contributors](#contributors)

## Overview <a name="overview"></a>

The **Rubik's Cube Solver** project is designed to detect the colors of a Rubik's Cube and implement four distinct solving algorithms: Layer by Layer, BFS & BB (Breadth-First Search & Bi-Directional BFS), Kociemba, and Koft. These algorithms are implemented in Python. Subsequently, the project evaluates and compares the effectiveness of these algorithms in solving the Rubik's Cube.

## Usage <a name="usage"></a>

### Installation of Required Libraries

To install the necessary libraries, execute the following command:

```bash
pip install -r requirements.txt
```

To run the program, execute the following command:
```bash
python main.py
```
From the UI screen, you have 2 options:
  - Use your camera to detect the state of the shuffled Rubik's Cube 
  - You can directly type the cube definition string. A solved cube has the string 'UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB'


SOLVING FOR EXAMPLE STATE:  

INPUT:
```bash
GOYBYYYYYWRRRRRGRBGGGGGGYGROOOOOOWYOBWRBBYBBWRWBWWBOWW
```

OUTPUT:
```bash
KOCIEMBA SOLUTION: "F1 L2 U2 F1 R2 F1 D2 R1 F3 U2 F2 D2 L2 B3 L2 B1 D2 B1 (18f)"
LAYER BY LAYER SOLUTION: "B' R B U2 L U L' F U F' U' F' U' F U2 B' U B U L U' L' U L' U L U F U' F' R U R' U' F' U' F U' R U' R' U' F' U F R U R' U R U2 R' F U F' U F U2 F' U2 L U' R' U L' U' R B' D' B D B' D' B D B' D' B D B' D' B D U2 B' D' B D B' D' B D B' D' B D B' D' B D U B' D' B D B' D' B D B' D' B D B' D' B D U"
```
### Usage for Korf:
- Run file **bfs_corner_db.cpp** to create a database in file **cornerDB.bin** 
- Next, run **dls_edgeDB.cpp** to create the second and the third database in files **edge1DB.bin** and **edge2DB.bin**, respectively
- Finally, run the file **KorfSolver.cpp** to get solution from the Korf algorithm.

### Run solver with the display screen. 
- Run file **display.py**
- On the display window, choose the button "scramble" to generate a random state of Rubik's cube or choose the button "color detection" if you want our program to detects your rubik state
- Then, click the button that corresponds to the solver you want to use
  
