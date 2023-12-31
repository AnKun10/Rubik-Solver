import pygame
import sys

# Khởi tạo Pygame
pygame.init()

# Kích thước màn hình
screen_width = 840
screen_height = 630
square_size = 210
num_cols = screen_width // square_size
num_rows = screen_height // square_size

# Tạo ma trận lưu trữ thông tin về mỗi ô vuông
grid_data = [[0 for _ in range(num_cols)] for _ in range(num_rows)]

# Tạo màn hình
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Multiple Clicks to Change Color")

# Màu sắc
colors = {
    0: (0, 0, 0),     # black
    1: (255, 255, 0), # yellow
    2: (255, 0, 0),   # red
    3: (0, 255, 0),   # green
    4: (255, 165, 0), # orange
    5: (0, 0, 255),   # blue
    6: (255, 255, 255) # white
}

# Vòng lặp chính
running = True
while running:
    screen.fill(colors[0])  # Fill màn hình với màu đen
    
    # Vẽ lưới ô vuông và thực hiện thao tác trên mỗi ô
    for row in range(num_rows):
        for col in range(num_cols):
            square_x = col * square_size
            square_y = row * square_size
            pygame.draw.rect(screen, colors[6], (square_x, square_y, square_size, square_size), 1)  # Vẽ ô vuông
            
            # Kiểm tra sự kiện nhấp chuột để thay đổi màu sắc của ô vuông
            
            if pygame.mouse.get_pressed()[0]:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if square_x <= mouse_x < square_x + square_size and square_y <= mouse_y < square_y + square_size:
                    if not mouse_clicked:  # Chỉ tăng giá trị khi chuột được nhấn một lần
                        grid_data[row][col] += 1
                        if grid_data[row][col] > 6:
                            grid_data[row][col] = 0
                        mouse_clicked = True  # Đánh dấu rằng chuột đã được nhấn

            # Nếu chuột không được nhấn thì đặt lại biến mouse_clicked
            else:
                mouse_clicked = False
                    
            # Chỉnh sửa màu sắc của ô vuông dựa trên giá trị trong ma trận
            if grid_data[row][col] != 0:  
                pygame.draw.rect(screen, colors[grid_data[row][col]], (square_x, square_y, square_size, square_size))
                
    # Vòng lặp sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

# Kết thúc Pygame
pygame.quit()
sys.exit()
