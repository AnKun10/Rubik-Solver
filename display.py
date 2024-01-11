import pygame
from sys import exit
from math import sqrt
from rubikcube import RubikCube, BFSBBCube
from solver import LayerByLayer, BFSBB, Kociemba
from colordetection import ColorDetector
from copy import deepcopy


class Button:
    def __init__(self, font, text, width, height, pos, bg_color):
        self.pressed = False

        # Top rect
        self.rect = pygame.Rect(pos, (width, height))
        self.bg_color = bg_color
        self.org_bg_color = bg_color

        # Text
        self.text_surf = font.render(text, True, "White")
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self):
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=3)
        screen.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
                self.bg_color = "#0F1035"
            else:
                if self.pressed:
                    self.pressed = False
                    self.bg_color = self.org_bg_color


def get_up_side_colors(side, arrow_counter, flipped):
    if arrow_counter < 0:
        dir = (-arrow_counter) % 4
    else:
        dir = arrow_counter % 4
    if flipped:
        colors = [color for color in cube.state[(side + 1) * 9 - 1:side * 9 - 1:-1]]
    else:
        colors = [color for color in cube.state[side * 9:(side + 1) * 9]]
    match dir:
        case 3:
            colors[0], colors[1], colors[2], colors[3], colors[5], colors[6], colors[7], colors[8] = colors[2], \
                colors[5], colors[8], colors[1], colors[7], colors[0], colors[3], colors[6]
        case 2:
            colors[0], colors[1], colors[2], colors[3], colors[5], colors[6], colors[7], colors[8] = colors[8], \
                colors[7], colors[6], colors[5], colors[3], colors[2], colors[1], colors[0]
        case 1:
            colors[0], colors[1], colors[2], colors[3], colors[5], colors[6], colors[7], colors[8] = colors[6], \
                colors[3], colors[0], colors[7], colors[1], colors[8], colors[5], colors[2]
    return colors


def validate_state(state):
    if len(state) == 54:
        color_counter_dict = {'W': 0, 'R': 0, 'G': 0, 'B': 0, 'O': 0, 'Y': 0}
        for color in state:
            color_counter_dict[color] += 1
        if list(color_counter_dict.values()).count(9) != 6:
            return False
        return True
    return False


cube = RubikCube()
cube.show()
color_dict = {'W': 'White', 'R': 'Red', 'G': 'Green', 'B': 'Blue', 'O': 'Orange', 'Y': 'Yellow'}
side_to_text_dict = {0: 'U', 1: 'L', 2: 'F', 3: 'R', 4: 'B', 5: 'D'}
opposite_side_dict = {0: 5, 5: 0, 1: 3, 3: 1, 2: 4, 4: 2}
rot_dict = {"U": cube.U, "U'": cube.Ui, "U2": cube.U2,
            "L": cube.L, "L'": cube.Li, "L2": cube.L2,
            "F": cube.F, "F'": cube.Fi, "F2": cube.F2,
            "R": cube.R, "R'": cube.Ri, "R2": cube.R2,
            "B": cube.B, "B'": cube.Bi, "B2": cube.B2,
            "D": cube.D, "D'": cube.Di, "D2": cube.D2}
solution = []
solution_steps = 0
front_side = 2
right_side = 3
up_side = 0
right_arrow_dict = {1: 2, 2: 3, 3: 4, 4: 1}
left_arrow_dict = {1: 4, 2: 1, 3: 2, 4: 3}
# Press right arrow = +1, Press left arrow = -1
arrow_counter = 0
flipped = False

N = 48
FRONT_SKEW = 15
RIGHT_SKEW = 25
FPS = 10

pygame.init()
pygame.display.set_caption("RUBIK SOLVER")

screen = pygame.display.set_mode((1200, 700))
clock = pygame.time.Clock()
background_surf = pygame.image.load('graphics/background.png').convert_alpha()
background_rect = background_surf.get_rect(center=(600, 350))
setting_surf = pygame.image.load('graphics/setting.png').convert_alpha()
setting_rect = setting_surf.get_rect(topleft=(800, 0))


def get_front_points(x, y):
    """
    :param x: starting x position
    :param y: starting y position
    :return: (list) contains all vertices of the facelet
    """
    return [(x, y), (x, y + N), (x + sqrt(N ** 2 - FRONT_SKEW ** 2), y + N + FRONT_SKEW),
            (x + sqrt(N ** 2 - FRONT_SKEW ** 2), y + FRONT_SKEW)]


def get_right_points(x, y):
    """
    :param x: starting x position
    :param y: starting y position
    :return: (list) contains all vertices of the facelet
    """
    return [(x, y), (x, y + N), (x + sqrt(N ** 2 - RIGHT_SKEW ** 2), y + N - RIGHT_SKEW),
            (x + sqrt(N ** 2 - RIGHT_SKEW ** 2), y - RIGHT_SKEW)]


def get_last_up_point(point1, point2, point3):
    """
    :param point1: left vertex of the facelet
    :param point2: down vertex of the facelet
    :param point3: right vertex of the facelet
    :return: (tuple) coordinate of the up vertex of the facelet
    """
    return (point3[0] - point2[0] + point1[0], point1[1] - (point2[1] - point3[1]))


# FRD point = (500, 450)
start = (400 - sqrt((3 * N) ** 2 - (3 * FRONT_SKEW) ** 2), 450 - 3 * (FRONT_SKEW + N))
front_start_points = [start,
                      (start[0] + sqrt(N ** 2 - FRONT_SKEW ** 2), start[1] + FRONT_SKEW),
                      (start[0] + sqrt((2 * N) ** 2 - (2 * FRONT_SKEW) ** 2), start[1] + 2 * FRONT_SKEW),
                      (start[0], start[1] + N),
                      (start[0] + sqrt(N ** 2 - FRONT_SKEW ** 2), start[1] + N + FRONT_SKEW),
                      (start[0] + sqrt((2 * N) ** 2 - (2 * FRONT_SKEW) ** 2), start[1] + N + 2 * FRONT_SKEW),
                      (start[0], start[1] + 2 * N),
                      (start[0] + sqrt(N ** 2 - FRONT_SKEW ** 2), start[1] + 2 * N + FRONT_SKEW),
                      (start[0] + sqrt((2 * N) ** 2 - (2 * FRONT_SKEW) ** 2), start[1] + 2 * N + 2 * FRONT_SKEW)]
start = (400, 450 - 3 * N)
right_start_points = [start,
                      (start[0] + sqrt(N ** 2 - RIGHT_SKEW ** 2), start[1] - RIGHT_SKEW),
                      (start[0] + sqrt((2 * N) ** 2 - (2 * RIGHT_SKEW) ** 2), start[1] - 2 * RIGHT_SKEW),
                      (start[0], start[1] + N),
                      (start[0] + sqrt(N ** 2 - RIGHT_SKEW ** 2), start[1] + N - RIGHT_SKEW),
                      (start[0] + sqrt((2 * N) ** 2 - (2 * RIGHT_SKEW) ** 2), start[1] + N - 2 * RIGHT_SKEW),
                      (start[0], start[1] + 2 * N),
                      (start[0] + sqrt(N ** 2 - RIGHT_SKEW ** 2), start[1] + 2 * N - RIGHT_SKEW),
                      (start[0] + sqrt((2 * N) ** 2 - (2 * RIGHT_SKEW) ** 2), start[1] + 2 * N - 2 * RIGHT_SKEW)]
# Key = coordinate of a point on the up face
# Value = coordinate of that point on the screen
up_start_points_dict = {(3, 0): front_start_points[0], (3, 1): front_start_points[1], (3, 2): front_start_points[2],
                        (3, 3): right_start_points[0], (2, 3): right_start_points[1], (1, 3): right_start_points[2],
                        (0, 3): (right_start_points[2][0] + sqrt(N ** 2 - RIGHT_SKEW ** 2),
                                 right_start_points[2][1] - RIGHT_SKEW)}
for row in range(3, 0, -1):
    for col in range(2, -1, -1):
        point1, point2, point3 = up_start_points_dict[(row, col)], up_start_points_dict[(row, col + 1)], \
            up_start_points_dict[(row - 1, col + 1)]
        up_start_points_dict[(row - 1, col)] = get_last_up_point(point1, point2, point3)
up_facelet_points = []
for row in range(3):
    for col in range(3):
        point1, point2, point3, point4 = up_start_points_dict[(row, col)], up_start_points_dict[(row + 1, col)], \
            up_start_points_dict[(row + 1, col + 1)], up_start_points_dict[(row, col + 1)]
        up_facelet_points.append([point1, point2, point3, point4])

arrow_surf = pygame.image.load('graphics/curved-arrow-icon.png').convert_alpha()
arrow_right_surf = pygame.transform.rotozoom(arrow_surf, 0, 0.15)
arrow_right_rect = arrow_right_surf.get_rect(center=(515, 520))
arrow_left_surf = pygame.transform.flip(arrow_right_surf, True, False)
arrow_left_rect = arrow_left_surf.get_rect(center=(275, 520))
arrow_surf = pygame.image.load('graphics/flip-arrow.png').convert_alpha()
arrow_flip_surf = pygame.transform.rotozoom(arrow_surf, 0, 0.3)
arrow_flip_rect = arrow_flip_surf.get_rect(center=(395, 580))

setting_icon_surf = pygame.image.load('graphics/setting-icon.png').convert_alpha()
setting_icon_surf = pygame.transform.rotozoom(setting_icon_surf, 0, 0.1)
setting_icon_rect = setting_icon_surf.get_rect(topleft=(815, 15))
font_side = pygame.font.Font('font/Sidenotion.ttf', 50)
font_setting = pygame.font.Font('font/Setting.ttf', 30)
detection_button = Button(font_setting, "Color Detection", 300, 50, (850, 200), "#EF4040")
scramble_button = Button(font_setting, "Scramble", 150, 50, (850, 125), "#EF4040")
scramble_text = ''
scramble_text_rect = pygame.Rect((1020, 125), (50, 50))
scramble_text_active = False
font_state = pygame.font.Font('font/Setting.ttf', 12)
state_button = Button(font_setting, "State", 100, 50, (950, 300), "#EF4040")
state_text = ''
state_text_rect = pygame.Rect((810, 375), (380, 20))
state_active = False
# LBL_button = Button(font_setting, "LBL", 75, 50, (1050, 525), "#365486")
LBL_button = Button(font_setting, "LBL", 100, 50, (875, 525), "#365486")
# BFSBB_button = Button(font_setting, "BFSBB", 100, 50, (1150, 525), "#365486")
BFSBB_button = Button(font_setting, "BFSBB", 100, 50, (1025, 525), "#365486")
# Korf_button = Button(font_setting, "Korf", 75, 50, (1275, 525), "#365486")
Kociemba_button = Button(font_setting, "Kociemba", 150, 50, (925, 600), "#365486")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (arrow_right_rect.collidepoint(event.pos) and not flipped) or \
                    (arrow_left_rect.collidepoint(event.pos) and flipped):
                front_side = right_arrow_dict[front_side]
                right_side = right_arrow_dict[right_side]
                arrow_counter += 1
            if (arrow_left_rect.collidepoint(event.pos) and not flipped) or \
                    (arrow_right_rect.collidepoint(event.pos) and flipped):
                front_side = left_arrow_dict[front_side]
                right_side = left_arrow_dict[right_side]
                arrow_counter -= 1
            if arrow_flip_rect.collidepoint(event.pos):
                flipped = not flipped
                up_side = opposite_side_dict[up_side]
                right_side = opposite_side_dict[right_side]
            if scramble_text_rect.collidepoint(event.pos):
                scramble_text_active = True
            else:
                scramble_text_active = False
            if scramble_button.rect.collidepoint(event.pos):
                if scramble_text != '':
                    validate_scramble = True
                    scramble_num = 0
                    try:
                        scramble_num = int(scramble_text)
                    except ValueError:
                        validate_scramble = False
                    if validate_scramble:
                        cube.shuffle(min_rot=scramble_num, max_rot=scramble_num)
                        state_text = cube.state
                        cube.show()
            if state_text_rect.collidepoint(event.pos):
                state_active = True
            else:
                state_active = False
            if state_button.rect.collidepoint(event.pos):
                if validate_state(state_text):
                    cube.update_state(state=state_text)
            if detection_button.rect.collidepoint(event.pos):
                detector = ColorDetector()
                detector.color_detecting()
                if detector.validate_state():
                    state_text = detector.state
                    solution = []
                    solution_steps = 0
            if LBL_button.rect.collidepoint(event.pos):
                temp_cube = deepcopy(cube)
                solver = LayerByLayer(temp_cube)
                solver.solve()
                solution = temp_cube.history
                solution_steps = len(solution)
            if Kociemba_button.rect.collidepoint(event.pos):
                solver = Kociemba(cube.state)
                solution = solver.solve()
                solution_steps = len(solution)
            if BFSBB_button.rect.collidepoint(event.pos):
                temp_cube = BFSBBCube(state=cube.state)
                solver = BFSBB(temp_cube)
                solution = solver.solve()
                solution_steps = len(solution)
        if event.type == pygame.KEYDOWN:
            if scramble_text_active:
                if event.key == pygame.K_BACKSPACE:
                    scramble_text = scramble_text[:-1]
                else:
                    scramble_text += event.unicode
            if state_active:
                if event.key == pygame.K_BACKSPACE:
                    state_text = state_text[:-1]
                else:
                    state_text += event.unicode

    if solution:
        print(solution)
        rot_dict[solution.pop(0)]()
    # Get color for cube
    if flipped:
        front_colors = [color for color in cube.state[(front_side + 1) * 9 - 1:front_side * 9 - 1:-1]]
        right_colors = [color for color in cube.state[(right_side + 1) * 9 - 1:right_side * 9 - 1:-1]]
    else:
        front_colors = [color for color in cube.state[front_side * 9:(front_side + 1) * 9]]
        right_colors = [color for color in cube.state[right_side * 9:(right_side + 1) * 9]]
    up_colors = get_up_side_colors(up_side, arrow_counter, flipped)

    screen.blit(background_surf, background_rect)
    screen.blit(setting_surf, setting_rect)
    screen.blit(setting_icon_surf, setting_icon_rect)
    screen.blit(arrow_left_surf, arrow_left_rect)
    screen.blit(arrow_right_surf, arrow_right_rect)
    screen.blit(arrow_flip_surf, arrow_flip_rect)
    solution_steps_surf = font_setting.render(f"Solution Steps: {solution_steps}", True, "#A1EEBD")
    solution_steps_rect = solution_steps_surf.get_rect(center=(1000, 490))
    screen.blit(solution_steps_surf, solution_steps_rect)
    pygame.draw.rect(screen, "White", state_text_rect)
    state_text_surf = font_state.render(state_text, True, "Black")
    screen.blit(state_text_surf, (state_text_rect.x + 5, state_text_rect.y + 5))
    state_text_rect.w = max(380, state_text_surf.get_width() + 10)
    pygame.draw.rect(screen, "White", scramble_text_rect)
    scramble_text_surf = font_setting.render(scramble_text, True, "Black")
    screen.blit(scramble_text_surf, (scramble_text_rect.x + 5, scramble_text_rect.y + 5))
    scramble_text_rect.w = max(50, scramble_text_surf.get_width() + 10)
    state_button.draw()
    scramble_button.draw()
    detection_button.draw()
    LBL_button.draw()
    BFSBB_button.draw()
    # Korf_button.draw()
    Kociemba_button.draw()

    # Side notion text
    front_side_notion_color = cube.state[9 * front_side + 4]
    front_side_notion_surf = font_side.render(f"{side_to_text_dict[front_side]}", True,
                                              color_dict[front_side_notion_color])
    front_side_notion_rect = front_side_notion_surf.get_rect(center=(100, 350))
    right_side_notion_color = cube.state[9 * right_side + 4]
    right_side_notion_surf = font_side.render(f"{side_to_text_dict[right_side]}", True,
                                              color_dict[right_side_notion_color])
    right_side_notion_rect = right_side_notion_surf.get_rect(center=(700, 350))
    up_side_notion_color = cube.state[9 * up_side + 4]
    up_side_notion_surf = font_side.render(f"{side_to_text_dict[up_side]}", True, color_dict[up_side_notion_color])
    up_side_notion_rect = up_side_notion_surf.get_rect(center=(400, 100))
    screen.blit(front_side_notion_surf, front_side_notion_rect)
    screen.blit(right_side_notion_surf, right_side_notion_rect)
    screen.blit(up_side_notion_surf, up_side_notion_rect)

    # Draw cube
    for i in range(9):
        front_point = front_start_points[i]
        pygame.draw.polygon(screen, color_dict[front_colors[i]], get_front_points(front_point[0], front_point[1]))
        pygame.draw.polygon(screen, 'Black', get_front_points(front_point[0], front_point[1]), 3)
        right_point = right_start_points[i]
        pygame.draw.polygon(screen, color_dict[right_colors[i]], get_right_points(right_point[0], right_point[1]))
        pygame.draw.polygon(screen, 'Black', get_right_points(right_point[0], right_point[1]), 3)
        up_facelet = up_facelet_points[i]
        pygame.draw.polygon(screen, color_dict[up_colors[i]], up_facelet)
        pygame.draw.polygon(screen, 'Black', up_facelet, 3)

    pygame.display.update()
    clock.tick(FPS)
