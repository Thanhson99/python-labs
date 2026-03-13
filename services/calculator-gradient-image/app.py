import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the source image
image = cv2.imread("images.jpg")
if image is None:
    raise ValueError("Unable to read image. Please check the file path.")

# Convert image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Compute gradients with the Sobel operator
grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

# Compute gradient magnitude and direction
magnitude = np.sqrt(grad_x**2 + grad_y**2)
direction = np.arctan2(grad_y, grad_x)

# Normalize values to the [0, 255] range
magnitude = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
direction = cv2.normalize(direction, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

# Build a colorized gradient image in HSV space
hsv_image = np.zeros_like(image, dtype=np.uint8)
hsv_image[..., 0] = direction  # Hue from gradient direction
hsv_image[..., 1] = magnitude  # Saturation from gradient magnitude
hsv_image[..., 2] = 255        # Keep maximum brightness

# Convert HSV back to BGR for OpenCV display
gradient_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

# Display images
plt.figure(figsize=(12, 6))
plt.subplot(1, 3, 1), plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)), plt.title("Original Image")
plt.subplot(1, 3, 2), plt.imshow(magnitude, cmap="gray"), plt.title("Gradient Magnitude")
plt.subplot(1, 3, 3), plt.imshow(cv2.cvtColor(gradient_image, cv2.COLOR_BGR2RGB)), plt.title("Color Gradient Image")
plt.show()

# Save output image
cv2.imwrite("images_gradient_output.jpg", gradient_image)
