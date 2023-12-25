import cv2
import numpy as np

def flip_image(frame):
    # Lật hình ảnh theo chiều ngang (đổi -1 thành 1 để lật theo chiều dọc)
    flipped_frame = cv2.flip(frame, 1)
    return flipped_frame

def get_color_name(hsv_color):
    h, s, v = hsv_color
    if s<50:
        return 'white'
    if h < 6.5 or h>170 :
        return 'red'
    elif h <18 and h>=6.5:
        return 'orange'
    elif h <= 35 and h>=18:
        return 'yellow'
    elif h>35 and h<= 83:
        return 'green'
    elif h > 83 and h< 130:
        return 'blue'
    else:
        return 'unknown'

def read_colors_once_using_color_ranges():
    cap = cv2.VideoCapture(0)  # Sử dụng camera mặc định, có thể thay đổi index để chọn camera khác

    if not cap.isOpened():
        print("Không thể mở camera")
        return

    desired_frame_size = 270  # Kích thước khung hình camera mong muốn (nhỏ hơn 300x300 pixels để chia thành 9 ô)
    cube_size = 3  # Kích thước mỗi ô trên mặt Rubik
    read_colors = False
    colors_read = False

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Không thể đọc dữ liệu từ camera")
            break

        # Lấy kích thước của khung hình camera hiện tại
        height, width, _ = frame.shape

        # Tính toán tọa độ bắt đầu và kết thúc để cắt phần trung tâm nhỏ hơn
        start_x = int((width - desired_frame_size) / 2)
        end_x = start_x + desired_frame_size
        start_y = int((height - desired_frame_size) / 2)
        end_y = start_y + desired_frame_size

        # Cắt phần trung tâm nhỏ hơn của khung hình camera
        cropped_frame = frame[start_y:end_y, start_x:end_x]

        # Tạo một bản sao của khung hình để vẽ lưới màu
        grid_frame = cropped_frame.copy()

        # Tính kích thước của mỗi ô vuông trong lưới 3x3
        square_size = desired_frame_size // cube_size

        for i in range(cube_size):
            for j in range(cube_size):
                # Tính toán tọa độ của hình vuông nhỏ trong ô vuông lớn
                small_square_start_x = i * square_size + square_size // 4
                small_square_end_x = (i + 1) * square_size - square_size // 4
                small_square_start_y = j * square_size + square_size // 4
                small_square_end_y = (j + 1) * square_size - square_size // 4

                # Vẽ hình vuông nhỏ trong ô vuông lớn
                cv2.rectangle(grid_frame, (small_square_start_x, small_square_start_y), (small_square_end_x, small_square_end_y), (255, 255, 255), 1)

                # Vẽ lưới 3x3 trên khung hình camera
                if i < cube_size - 1:
                    cv2.line(grid_frame, ((i + 1) * square_size, 0), ((i + 1) * square_size, desired_frame_size), (255, 255, 255), 1)
                if j < cube_size - 1:
                    cv2.line(grid_frame, (0, (j + 1) * square_size), (desired_frame_size, (j + 1) * square_size), (255, 255, 255), 1)
            
        # Nếu phím 'r' được nhấn và chưa đọc màu
        key = cv2.waitKey(1)
        if key == ord('r') and not colors_read:
            read_colors = True

        # Nếu đang trong trạng thái đọc màu và chưa đọc màu trước đó
        if read_colors and not colors_read:
            colors = []
            avg = []

            for i in range(cube_size):
                for j in range(cube_size):
                    small_square = cropped_frame[i * square_size + square_size // 4: (i + 1) * square_size - square_size // 4,
                                                j * square_size + square_size // 4: (j + 1) * square_size - square_size // 4]

                    small_square_hsv = cv2.cvtColor(small_square, cv2.COLOR_BGR2HSV)
                    for x in range(small_square_hsv.shape[0]):
                        for y in range(small_square_hsv.shape[1]):
                            if small_square_hsv[x, y, 1] >= 50:  # Kiểm tra giá trị S
                                small_square_hsv[x, y, 1] = 255  # Gán giá trị S thành 255
                    avg_color = cv2.mean(small_square_hsv)[:3]  # Tính màu trung bình
                    

                    color_name = get_color_name(avg_color)
                    colors.append(color_name)
                    avg.append(avg_color)

            print("Các màu trong 9 ô vuông (theo thứ tự):", colors)
            print(avg)
            colors_read = True  # Đã đọc màu

        # Hiển thị khung hình camera đã được cắt và lưới 3x3
        #cv2.imshow('Camera Frame', grid_frame)
        # Hiển thị khung hình camera đã được cắt và lưới 3x3 (lật hình ảnh trước khi hiển thị)
        flipped_grid_frame = flip_image(grid_frame)
        cv2.imshow('Camera Frame', flipped_grid_frame)


        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

read_colors_once_using_color_ranges()
