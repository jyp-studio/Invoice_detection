# weight
# f25_1
WEIGHTS_F25_1 = [
    [-5, -10, 15, 10],  # data
    [5, -8, 5, 10],  # id
    [0, -5, 5, 5],  # invoice_number
    [0, -10, 5, 10],  # tax
    [-5, -10, 5, 10],  # total
    [0, -5, 5, 8],  # untaxed
]

# best
WEIGHTS = [
    [0, -5, 0, 5],  # data
    [0, 0, 0, 0],  # id
    [0, 0, 0, 5],  # invoice_number
    [0, -10, 0, 10],  # tax
    [0, -8, 5, 10],  # total
    [0, -5, 5, 8],  # untaxed
]

# weight dict
ALL_WEIGHTS = {"25": WEIGHTS_F25_1, "25 long": WEIGHTS_F25_1}
VERIFY_WEIGHTS = {"25": WEIGHTS, "25 long": WEIGHTS_F25_1}

# format
INVOICE_FORMAT = ["25", "25 long", "25 block"]

# model
ALL_MODELS = {"25": "./weights/f25_1all_v4.pt", "25 long": "./weights/f25_1.pt"}
VERIFY_MODELS = {"25": "./weights/best.pt", "25 long": "./weights/f25_1all_v4.pt"}

NAME_LIST = ["date", "id", "invoice_number", "tax", "total", "untaxed"]

COLUMES = ["資料年", "月份", "發票日期", "對方統一編號", "發票號碼", "格式編號", "銷售金額"]

ALL_FORMATS = {"25": 25, "25 long": 25, "25 block": 25}
