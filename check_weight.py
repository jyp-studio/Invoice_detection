import torch
import cv2
import pytesseract


# yolo weights path
MODEL = "./weights/f25_1all_v3.pt"
# weights of crop position (left, top, right, bottom)
# f25_1 weight
WEIGHTS = [
    [-5, -10, 15, 10],  # data
    [13, -5, 5, 5],  # id
    [0, -5, 5, 5],  # invoice_number
    [0, -10, 5, 10],  # tax
    [-5, -10, 5, 10],  # total
    [0, -5, 5, 8],  # untaxed
]
NAME_LIST = ["date", "id", "invoice_number", "tax", "total", "untaxed"]

IMAGE_PATH = "./f25_1s/elec_invoice_6.jpg"


def ocr(image, info_loc) -> dict:
    # setup ans_list
    ans_dict = {}

    # extract yolo's result tensor
    for i in range(len(info_loc.xyxy[0])):
        # in each info find the correct label name
        which_tag = int(info_loc.xyxy[0][i][5])
        position_list = WEIGHTS[which_tag].copy()
        for j in range(len(info_loc.xyxy[0][0]) - 2):
            position_list[j] += int(info_loc.xyxy[0][i][j])

        key, value = word_recognize(image, position_list, NAME_LIST[which_tag])
        print(key, value)
        # add result to ans_dict
        ans_dict[f"{key}"] = value
        # clean the list for next info
        position_list.clear()
    return ans_dict


def crop(image, position):
    # crop
    img_crop = image[
        position[1] : position[3],
        position[0] : position[2],
    ]
    return img_crop


def word_recognize(image, position, tag_name):
    # crop
    img_crop = crop(image, position)
    cv2.imshow(tag_name, img_crop)

    # get words
    text = pytesseract.image_to_string(img_crop, lang="eng")

    print(f"{tag_name}: {text}")
    return tag_name, text


if __name__ == "__main__":
    # set up model
    model = torch.hub.load(
        "ultralytics/yolov5", "custom", path=MODEL, force_reload=True
    )
    image = cv2.imread(IMAGE_PATH)
    info = model(IMAGE_PATH)
    info.show()
    info.print()

    # ocr
    result_dict = ocr(image, info)

    print("=========ANSWER==========")
    for key, value in result_dict.items():
        print(f"{key}: {value}")
    print("=========ANSWER==========")

cv2.waitKey(0)
cv2.destroyAllWindows()
