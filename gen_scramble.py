from rubikcube import RubikCube

cube = RubikCube()

# while True:
#     rot_nums = []
#     try:
#         rot_nums = [int(x) for x in input("Number of rotations = ").split()]
#     except ValueError:
#         print("Invalid Input! Please Try again!")
#         continue
#     break

rot_nums = [3, 4, 5, 7, 10, 20, 50, 80, 100]
f = open("test_set.txt", "w")
for rot_num in rot_nums:
    cube.shuffle(min_rot=rot_num, max_rot=rot_num)
    f.write(f"{rot_num} {cube.state}\n")
    cube.reset()
