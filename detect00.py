import torch
import cv2
import numpy as np

# Model
model = torch.hub.load("ultralytics/yolov5", "yolov5s")  # or yolov5n - yolov5x6, custom

# Images
img = "https://ultralytics.com/images/zidane.jpg"  # or file, Path, PIL, OpenCV, numpy, list

# Inference
results = model(img)

# Results
results.show()  # show images
results.print()  # or .show(), .save(), .crop(), .pandas(), etc.
print(results.xyxy)
