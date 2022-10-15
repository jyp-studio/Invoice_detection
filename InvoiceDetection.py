import random
import torch
import cv2
import numpy as np
import pytesseract
import pandas as pd


class InvoiceDetection:
    def __init__(self, model_path, weights, name_list) -> None:
        # model
        self.model = torch.hub.load(
            "ultralytics/yolov5", "custom", path=model_path, force_reload=True
        )

        # name list and weights
        self.weights = weights
        self.name_list = name_list

        # image processing
        self.contrast = 0
        self.brightness = 0

    def info_detection(self, image):
        result = self.model(image)
        return result

    def img_contrast(self, image, contrast, brightness) -> None:
        result = image * (contrast / 127 + 1) - contrast + brightness
        result = np.clip(result, 0, 255)
        result = np.uint8(result)
        return result

    def img_blur(self, image, method, kernel_size):
        # check the kernel_size user input is odd
        if kernel_size % 2 == 0:
            kernel_size += 1

        # image blur with selected method
        if method == "gaussian":
            result = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
        elif method == "median":
            result = cv2.medianBlur(image, kernel_size)
        return result

    def ocr(self, image, info_loc) -> dict:
        # setup ans_list
        ans_dict = {}

        # extract yolo's result tensor
        for i in range(len(info_loc.xyxy[0])):
            # in each info find the correct label name
            which_tag = int(info_loc.xyxy[0][i][5])
            position_list = self.weights[which_tag].copy()
            for j in range(len(info_loc.xyxy[0][0]) - 2):
                position_list[j] += int(info_loc.xyxy[0][i][j])

            key, value = self.__word_recognize(
                image, position_list, self.name_list[which_tag]
            )
            # add result to ans_dict
            ans_dict[f"{key}"] = value
            # clean the list for next info
            position_list.clear()

        return ans_dict

    def __crop(self, image, position):
        # bias
        bias_left = random.randrange(-5, 5)
        bias_top = random.randrange(-5, 5)
        bias_right = random.randrange(-5, 5)
        bias_buttom = random.randrange(-5, 5)

        # crop
        img_crop = image[
            position[1] + bias_left : position[3] + bias_top,
            position[0] + bias_right : position[2] + bias_buttom,
        ]
        return img_crop

    def __word_recognize(self, image, position, tag_name):
        # initial ans
        text = "-1"
        best_text = ""
        max_iter = 100
        iter = 0

        while text != best_text and iter < max_iter:
            if text != "":
                best_text = text

            # crop
            img_crop = self.__crop(image, position)

            # get words
            text = pytesseract.image_to_string(img_crop, lang="eng")
            if tag_name == "date":
                new_text = "".join(filter(str.isdigit, text))
            elif tag_name == "id" or tag_name == "invoice_number":
                new_text = "".join(filter(str.isalnum, text))
            elif tag_name == "tax" or tag_name == "total" or tag_name == "untaxed":
                new_text = (
                    text.replace(",", "")
                    .replace(" ", "")
                    .strip("\n")
                    .strip("\t")
                    .strip()
                )

            # print(f"{tag_name}: {new_text}")

            iter += 1

        # convert the cost that with .00 to float
        if tag_name == "tax" or tag_name == "total" or tag_name == "untaxed":
            try:
                new_text = str(int(float(new_text)))
            except:
                print("tried convert the type of cost to float but failed")
            finally:
                new_text = "".join(filter(str.isdigit, new_text))
        return tag_name, new_text

    def __check_money(
        self,
    ):
        pass

    def save(self, ans_dict, columns):
        df = pd.DataFrame(ans_dict)
        df = df.T
        df.columns = columns
        df["確認(Y/N)"] = pd.Series(dtype=str)
        df = df.fillna("")
        df.to_excel("test.xlsx", index=False)


if __name__ == "__main__":
    # yolo weights path
    MODEL = "3best.pt"
    # weights of crop position (left, top, right, bottom)
    WEIGHTS = [
        [0, -5, 0, 5],  # data
        [0, 0, 0, 0],  # id
        [0, 0, 0, 5],  # invoice_number
        [0, -10, 0, 10],  # tax
        [0, -8, 5, 10],  # total
        [0, -5, 5, 8],  # untaxed
    ]
    NAME_LIST = ["date", "id", "invoice_number", "tax", "total", "untaxed"]

    # set up model
    invoice_det = InvoiceDetection(MODEL, WEIGHTS, NAME_LIST)

    # set up final results
    years = []
    months = []
    dates = []
    id = []
    invoice_num = []
    format_id = []
    untaxed = []
    FORMAT_ID = 25
    COLUMES = ["資料年", "月份", "發票日期", "對方統一編號", "發票號碼", "格式編號", "銷售金額"]

    for i in range(5):
        # load image and dectect infos' location
        image_path = f"./test/test{i}.jpg"
        image = cv2.imread(image_path)
        image_info_loc = invoice_det.info_detection(image_path)

        # image processing
        image_mod = invoice_det.img_contrast(image, contrast=100, brightness=0)

        # ocr
        result_dict = invoice_det.ocr(image_mod, image_info_loc)

        # fill up missing key and values
        for key in NAME_LIST:
            try:
                if result_dict[key] != None:
                    continue
            except:
                result_dict[key] = "x"

        print("=========ANSWER==========")
        for key, value in result_dict.items():
            print(f"{key}: {value}")
        print("=========ANSWER==========")

        # append to final list
        try:
            year = int(result_dict["date"][:4])
        except:
            yaer = "x"
        try:
            month = int(result_dict["date"][4:6])
        except:
            month = "x"
        try:
            day = int(result_dict["date"][6:8])
        except:
            day = "x"
        years.append(year)
        months.append(month)
        dates.append(f"{year}/{month}/{day}")
        id.append(result_dict["id"])
        invoice_num.append(result_dict["invoice_number"])
        format_id.append(FORMAT_ID)
        untaxed.append(int(result_dict["untaxed"]))

    # save to excel
    final = [years, months, dates, id, invoice_num, format_id, untaxed]
    invoice_det.save(final, COLUMES)
