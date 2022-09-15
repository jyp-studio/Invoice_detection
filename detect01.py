import torch
import cv2
import numpy as np

# Model
model = torch.hub.load("ultralytics/yolov5", "yolov5s")  # or yolov5n - yolov5x6, custom

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue
    results = model(frame)
    cv2.imshow("YOLO COCO 01", np.squeeze(results.render()))
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cap.destroyAllWindows()
