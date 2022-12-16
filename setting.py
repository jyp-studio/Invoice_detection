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
WEIGHTS_1 = {"25": WEIGHTS_F25_1, "25 block": WEIGHTS_F25_1}
WEIGHTS_2 = {"25": WEIGHTS_F25_1, "25 block": WEIGHTS_F25_1}
WEIGHTS_3 = {"25": WEIGHTS_F25_1, "25 block": WEIGHTS_F25_1}
WEIGHTS_4 = {"25": WEIGHTS, "25 block": WEIGHTS_F25_1}
WEIGHTS_5 = {"25": WEIGHTS, "25 block": WEIGHTS_F25_1}

# format
INVOICE_FORMAT = ["25", "25 block"]

# model
pt_f25_1all_v2 = "./weights/f25_1all_v2.pt"
pt_f25_1all_v3 = "./weights/f25_1all_v3.pt"
pt_f25_1all_v4 = "./weights/f25_1all_v4.pt"
pt_f25_1 = "./weights/f25_1.pt"
pt_best = "./weights/best.pt"
pt_best_v2 = "./weights/best_v2.pt"
pt_f25_1_500_v1 = "./weights/f25_1_500_v1.pt"

MODELS_1 = {"25": pt_f25_1all_v4, "25 block": pt_f25_1}
MODELS_2 = {"25": pt_f25_1_500_v1, "25 block": pt_f25_1all_v4}
MODELS_3 = {"25": pt_f25_1all_v3, "25 block": pt_f25_1all_v4}
MODELS_4 = {"25": pt_best, "25 block": pt_f25_1all_v4}
MODELS_5 = {"25": pt_best_v2, "25 block": pt_f25_1all_v4}

NAME_LIST = ["date", "id", "invoice_number", "tax", "total", "untaxed"]

COLUMES = ["資料年", "月份", "發票日期", "對方統一編號", "發票號碼", "格式編號", "銷售金額"]

ALL_FORMATS = {"25": 25, "25 block": 25}
