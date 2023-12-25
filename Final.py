import cv2
def flip_image(frame):
    # Lật hình ảnh theo chiều ngang (đổi -1 thành 1 để lật theo chiều dọc)
    flipped_frame = cv2.flip(frame, 1)
    return flipped_frame

def get_color_name(hsv_color):
    h, s, v = hsv_color
    if s<30:
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
def color_detecting():
    # ... (các biến và khởi tạo camera)
    cap = cv2.VideoCapture(0)
    cube_size = 3  # Kích thước lưới Rubik 3x3
    desired_frame_size = 300  # Kích thước khung hình camera

    while True:
        ret, frame = cap.read()
        if not ret:
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
        big_square_size = desired_frame_size // cube_size  # Kích thước của mỗi ô vuông lớn
        small_square_size = 3 * big_square_size // 5  # Kích thước của mỗi ô vuông nhỏ

        # Vẽ lưới 3x3 trên khung hình camera và vẽ hình vuông nhỏ trong mỗi ô vuông lớn
        for i in range(cube_size):
            for j in range(cube_size):
                # Tọa độ của ô vuông lớn
                big_square_start_x = j * big_square_size
                big_square_end_x = big_square_start_x + big_square_size
                big_square_start_y = i * big_square_size
                big_square_end_y = big_square_start_y + big_square_size

                # Tọa độ của ô vuông nhỏ
                small_square_start_x = i * big_square_size + big_square_size // 4
                small_square_end_x = (i + 1) * big_square_size - big_square_size // 4
                small_square_start_y = j * big_square_size + big_square_size // 4
                small_square_end_y = (j + 1) * big_square_size - big_square_size // 4

                # Vẽ ô vuông lớn
                cv2.rectangle(grid_frame, (big_square_start_x, big_square_start_y),
                              (big_square_end_x, big_square_end_y), (255, 255, 255), 1)

                # Vẽ ô vuông nhỏ trong ô vuông lớn
                cv2.rectangle(grid_frame, (small_square_start_x, small_square_start_y),
                              (small_square_end_x, small_square_end_y), (255, 255, 255), 1)

        # Hiển thị khung hình camera đã được cắt và lưới 3x3 với ô vuông nhỏ
        flipped_grid_frame = flip_image(grid_frame)
        cv2.imshow('Camera Frame', flipped_grid_frame)
        cnt = 0
        key = cv2.waitKey(1)
        if key == ord('r'):
            cnt += 1
            colors = []
            avg = []
            for i in range(cube_size):
                for j in range(cube_size-1,-1,-1):
                    small_square = cropped_frame[i * big_square_size + big_square_size // 4: (i + 1) * big_square_size - big_square_size // 4,
                                                j * big_square_size + big_square_size // 4: (j + 1) * big_square_size - big_square_size // 4]

                    small_square_hsv = cv2.cvtColor(small_square, cv2.COLOR_BGR2HSV)
                    for x in range(small_square_hsv.shape[0]):
                        for y in range(small_square_hsv.shape[1]):
                            if small_square_hsv[x, y, 1] >= 50:  # Kiểm tra giá trị S
                                small_square_hsv[x, y, 1] = 255  # Gán giá trị S thành 255
                    avg_color = cv2.mean(small_square_hsv)[:3]  # Tính màu trung bình
                    

                    color_name = get_color_name(avg_color)
                    colors.append(color_name)
                    avg.append(avg_color)
            print('Mat so',cnt,': ',colors)
            # Hiển thị khung hình với thông tin đã tính toán
            cv2.imshow('Average Colors', flipped_grid_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    color_detecting()
