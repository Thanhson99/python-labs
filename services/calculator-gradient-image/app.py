import cv2
import numpy as np
import matplotlib.pyplot as plt

# Đọc ảnh gốc
image = cv2.imread("images.jpg")
if image is None:
    raise ValueError("Không thể đọc ảnh. Hãy kiểm tra đường dẫn!")

# Chuyển ảnh sang thang xám
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Tính toán gradient bằng toán tử Sobel
grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

# Tính độ lớn và hướng của gradient
magnitude = np.sqrt(grad_x**2 + grad_y**2)
direction = np.arctan2(grad_y, grad_x)

# Chuẩn hóa giá trị về khoảng [0, 255]
magnitude = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
direction = cv2.normalize(direction, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

# Tạo ảnh màu từ gradient bằng không gian HSV
hsv_image = np.zeros_like(image, dtype=np.uint8)
hsv_image[..., 0] = direction  # Hue từ hướng gradient
hsv_image[..., 1] = magnitude  # Saturation từ độ lớn gradient
hsv_image[..., 2] = 255        # Giữ độ sáng tối đa

# Chuyển từ HSV sang BGR để hiển thị bằng OpenCV
gradient_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

# Hiển thị ảnh
plt.figure(figsize=(12, 6))
plt.subplot(1, 3, 1), plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)), plt.title("Ảnh gốc")
plt.subplot(1, 3, 2), plt.imshow(magnitude, cmap="gray"), plt.title("Gradient Magnitude")
plt.subplot(1, 3, 3), plt.imshow(cv2.cvtColor(gradient_image, cv2.COLOR_BGR2RGB)), plt.title("Ảnh Gradient Màu")
plt.show()

# Lưu ảnh kết quả
cv2.imwrite("images_gradient_output.jpg", gradient_image)
