import torch
import cv2
import pytesseract

if __name__ == "__main__":
    MODEL = "./yolov5/runs/train/exp9/weights/best.pt"
    IMAGE_PATH = (
        "./ig_dataset/test/images/ig_4_png.rf.90a9a717bda65742bcadc85ba29d05f3.jpg"
    )
    # set up model
    """
    model = torch.hub.load(
        "ultralytics/yolov5",
        "custom",
        path=MODEL,
        force_reload=True,
    )
    """
    model = torch.hub.load(
        "yolov5",
        "custom",
        path=MODEL,
        source="local",
        force_reload=True,
    )

    image = cv2.imread(IMAGE_PATH)
    info = model(IMAGE_PATH)
    info.show()
    info.print()

    # ocr
    # result_dict = ocr(image, info)

    # print("=========ANSWER==========")
    # for key, value in result_dict.items():
    #     print(f"{key}: {value}")
    # print("=========ANSWER==========")

# cv2.waitKey(0)
# cv2.destroyAllWindows()
