import torch
from PIL import Image
import matplotlib.pyplot as plt
import cv2
import numpy as np

# Load YOLOv5 small model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Load an image
img_path = 'C:/Users/louis/Dropbox/URIS Data/jats_incline_20250110/processed_skyview_20250110/20250110_154720.jpg'
img = Image.open(img_path)
img = np.array(img)

# Fisheye camera parameters (example values, you need to replace these with your actual camera parameters)
K = np.array([[300, 0, img.shape[1] / 2],
              [0, 300, img.shape[0] / 2],
              [0, 0, 1]])
D = np.array([-0.1, 0.12, 0.001, 0.001])  # Distortion coefficients

# Undistort the fisheye image
h, w = img.shape[:2]
new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(K, D, (w, h), np.eye(3), balance=1)
map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), new_K, (w, h), cv2.CV_16SC2)
undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

# Check if the undistorted image is valid
if undistorted_img is None or undistorted_img.size == 0:
    raise ValueError("Undistorted image is invalid. Check the camera parameters and undistortion process.")

# Convert back to PIL Image
undistorted_img = Image.fromarray(undistorted_img)
plt.imshow(undistorted_img)
plt.axis('off')
plt.show()

# Get detection results
results = model(undistorted_img)  # Prediction
results.show()  # Show the results