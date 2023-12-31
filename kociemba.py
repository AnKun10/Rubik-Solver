import twophase.solver as sv
#import twophase.client_gui
class Kociemba:
    def __init__(self, st):
        # Initialize a list of 6 sub-arrays for each face of the Rubik's Cube
        list_of_lists = [[] for _ in range(6)]
        for i in range(54):
            # Divide the string 'st' into sub-arrays of 9 characters and add them to list_of_lists
            list_of_lists[i // 9].append(st[i])
        
        # Reorder the sub-arrays according to a specific order
        od = [0, 3, 2, 5, 1, 4] 
        new_list = ''
        self.st = ''
        dict = {'W': 'D', 'G': 'F', 'R': 'L', 'O': 'R', 'B': 'B', 'Y': 'U'}
        for i in od:
            for j in range(9):
                new_list += list_of_lists[i][j]
        for char in new_list:
            self.st += dict[char]

    def solve_cube(self):
        print(sv.solve(self.st,19,2))

# Example usage
cubestring = 'WBYWYYYYWBROGROYOGBRGBGYRBORGBBOOBWWRRRYBWGGGYWWGWOORO'
kociemba_cube = Kociemba(cubestring)
kociemba_cube.solve_cube()
#print(sv.solve('DDUFUUDLBDBBLRDURDFBRUFFFDFLFRDDFRBFBURLLRBLULBLRBULRU'))

#DDUFUUDLBDBBLRDURDFBRUFFFDFLFRDDFRBFBURLLRBLULBLRLULRU
#DDUFUUDLBDBBLRDURDFBRUFFFDFLFRDDFRBFBURLLRBLULBLRBULRU
#URFDLB
#032514
'''def change():
    st = 'DDUFUUDLBDBBLRDURDFBRUFFFDFLFRDDFRBFBURLLRBLULBLRBULRU'
    dic = {'D': 'W', 'F': 'G', 'L': 'R', 'R': 'O', 'B': 'B', 'U': 'Y'}
    #dict = {'W': 'D', 'G': 'F', 'R': 'L', 'O': 'R', 'B': 'B', 'Y': 'U'}
    str = ''
    for i in st:
        str += dic[i]
    print(str)
change()'''
        
        
        
        
        
                
        
