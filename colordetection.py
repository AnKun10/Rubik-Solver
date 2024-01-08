import cv2


class ColorDetector:
    def __init__(self) -> None:
        self.state = ""

    def write_to_file(self, scramble_data):
        try:
            with open('scramble.txt', 'w') as file:
                file.write(scramble_data)
        except Exception as e:
            print("Failed to write", str(e))

    def get_color_name(self, hsv_color):
        h, s, v = hsv_color
        if s < 50:
            return 'W'
        if h < 6 or h > 170:
            return 'R'
        elif 6 <= h < 18:
            return 'O'
        elif 18 <= h <= 35:
            return 'Y'
        elif 35 < h <= 83:
            return 'G'
        elif 83 < h < 130:
            return 'B'
        else:
            return 'unknown'

    def color_detecting(self):
        cap = cv2.VideoCapture(0)
        cube_size = 3  # Rubik's Cube grid size 3x3
        desired_frame_size = 240  # Camera frame size
        colors_list = []  # List to store color lists for each 'R' press
        avg_list = []  # List to store average value lists for each 'R' press

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Get current camera frame size
            height, width, _ = frame.shape

            # Calculate start and end coordinates to crop smaller central part
            start_x = int((width - desired_frame_size) / 2)
            end_x = start_x + desired_frame_size
            start_y = int((height - desired_frame_size) / 2)
            end_y = start_y + desired_frame_size

            # Crop a smaller central part of the camera frame
            cropped_frame = frame[start_y:end_y, start_x:end_x]

            # Create a copy of the frame to draw a color grid
            grid_frame = cropped_frame.copy()

            # Calculate the size of each square in the 3x3 grid
            big_square_size = desired_frame_size // cube_size  # Size of each large square
            small_square_size = 3 * big_square_size // 5  # Size of each small square

            # Draw a 3x3 grid on the camera frame and smaller squares within each large square
            for i in range(cube_size):
                for j in range(cube_size):
                    # Coordinates of large square
                    big_square_start_x = j * big_square_size
                    big_square_end_x = big_square_start_x + big_square_size
                    big_square_start_y = i * big_square_size
                    big_square_end_y = big_square_start_y + big_square_size

                    # Coordinates of small square
                    small_square_start_x = i * big_square_size + big_square_size // 4
                    small_square_end_x = (i + 1) * big_square_size - big_square_size // 4
                    small_square_start_y = j * big_square_size + big_square_size // 4
                    small_square_end_y = (j + 1) * big_square_size - big_square_size // 4

                    # Draw the large square
                    cv2.rectangle(grid_frame, (big_square_start_x, big_square_start_y),
                                  (big_square_end_x, big_square_end_y), (255, 255, 255), 1)

                    # Draw the small square inside the large square
                    cv2.rectangle(grid_frame, (small_square_start_x, small_square_start_y),
                                  (small_square_end_x, small_square_end_y), (255, 255, 255), 1)

            # Show the cropped camera frame and the 3x3 grid with small squares
            cv2.imshow('CameraFrame', grid_frame)
            cnt = 1
            key = cv2.waitKey(1)
            if key == ord('t'):
                colors = []
                avg = []
                for i in range(cube_size):
                    for j in range(cube_size):
                        small_square = cropped_frame[i * big_square_size + big_square_size // 4: (
                                                                                                             i + 1) * big_square_size - big_square_size // 4,
                                       j * big_square_size + big_square_size // 4: (
                                                                                               j + 1) * big_square_size - big_square_size // 4]

                        small_square_hsv = cv2.cvtColor(small_square, cv2.COLOR_BGR2HSV)
                        avg_color = cv2.mean(small_square_hsv)[:3]  # Calculate average color

                        color_name = self.get_color_name(avg_color)
                        colors.append(color_name)
                        avg.append(avg_color)
                print(colors)
                # print(avg)
                cv2.imshow('Average Colors', grid_frame)

            if cv2.waitKey(1) == ord('s'):
                colors_list.append(colors.copy())
                avg_list.append(avg.copy())
                print('Data saved')
                colors = []
            if cv2.waitKey(1) == ord('q'):
                for lst in colors_list:
                    for char in lst:
                        self.state += char
                self.write_to_file(self.state)
                break

        cap.release()
        cv2.destroyAllWindows()

    def validate_state(self):
        if len(self.state) == 54:
            color_counter_dict = {'W': 0, 'R': 0, 'G': 0, 'B': 0, 'O': 0, 'Y': 0}
            for color in self.state:
                color_counter_dict[color] += 1
            if list(color_counter_dict.values()).count(9) != 6:
                return False
            return True
        return False

if __name__ == "__main__":
    detector = ColorDetector()
    detector.color_detecting()
'''
Note for camera usage:
    - F-face orientation towards a person opposite the camera
       Y
    R  G   O   B
       W

       U
    L  F   R   B
       D
'''
