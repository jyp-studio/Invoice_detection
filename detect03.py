# custom train
import torch
import os
import cv2
import numpy as np
import math
from PIL import Image
import pytesseract
import matplotlib.pyplot as plt

# global variables
FILEPATH = None
IMAGE = "./test/test6.jpg"

# variable used to change cv2 function
contrast = 100
brightness = 0

# weights of crop position
# left, top, right, bottom
WEIGHTS = [
    [0, -5, 0, 5],  # data
    [0, 0, 0, 0],  # id
    [0, 0, 0, 5],  # invoice_number
    [0, 0, 0, 0],  # tax
    [0, -8, 5, 10],  # total
    [0, -5, 5, 8],  # untaxed
]
NAME_LIST = ["data", "id", "invoice_number", "tax", "total", "untaxed"]


def initial_model():
    # user input weights path
    # PATH = input("path?")
    PATH = "yolov5/runs/train/exp6"

    # find weights
    if os.path.isfile(PATH + "/weights/best.pt"):
        print("best.pt is exist")
        FILEPATH = PATH + "/weights/best.pt"
    elif os.path.isfile(PATH + "/weights/last.pt"):
        print("best.pt is not exist, using last.pt")
        FILEPATH = PATH + "/weights/last.pt"
    else:
        print("no any weights")

    # initialize the model
    if FILEPATH != None:
        # Model
        model = torch.hub.load(
            "ultralytics/yolov5",
            "custom",
            path=FILEPATH,
            force_reload=True,
        )  # or yolov5n - yolov5x6, custom
    return model


def ocr_crop_img(image, position, tag_name):
    """crop image and print the text on image"""
    img = Image.open(image)
    img_crop = img.crop(position)  # (left, top, right, bottom)
    # img_crop.show()

    img = cv2.imread(image)
    img_crop = img[position[1] : position[3], position[0] : position[2]]
    # modifing img: change contrast and brightness
    # img_mod = cv2.medianBlur(img_crop, 5)
    # img_mod = cv2.GaussianBlur(img_crop, (5, 5), 0)
    img_mod = img_crop * (contrast / 127 + 1) - contrast + brightness
    img_mod = np.clip(img_mod, 0, 255)
    img_mod = np.uint8(img_mod)
    text = pytesseract.image_to_string(img_mod, lang="chi_tra+eng")
    text = text.replace("\n", "").replace(",", "").replace(" ", "")
    print(f"{tag_name}: {text}")


model = torch.hub.load(
    "ultralytics/yolov5",
    "custom",
    path="4best.pt",
    force_reload=True,
)

# Inference
# model = initial_model()
results = model(IMAGE)

# Results
results.show()
print(results.xyxy)  # or .show(), .save(), .crop(), .pandas(), etc.


def run():
    for i in range(len(results.xyxy[0])):
        which_tag = int(results.xyxy[0][i][5])
        position_list = WEIGHTS[which_tag]
        for j in range(len(results.xyxy[0][0]) - 2):
            position_list[j] += int(results.xyxy[0][i][j])

        ocr_crop_img(IMAGE, position_list, NAME_LIST[which_tag])
        position_list.clear()


run()

# %%
