import pandas as pd
import openpyxl
import matplotlib.pyplot as plt

# 讀取excel檔案
df = pd.read_excel("test.xlsx", header=0)
df2 = pd.read_excel("right_invoice.xlsx", header=0)

k = 0
fr = 0
h = 0
m = 0
l = 0
for i in range(0, df2.shape[0]):
    for j in range(0, df2.shape[1]):
        y = str(df.iat[i, j])
        y = y.replace(".0", "")
        y = y.replace("2022/", "2022/0")
        z = str(df2.iat[i, j])
        z = z.replace("00:00:00", "")
        z = z.replace("-", "/")
        y = y.strip()
        z = z.strip()
        # print(z) #查看資料內容時，取消井字(同下)
        # print(y)

        if z == y:
            k += 1
    fr = (k / 7) * 100  # 計算各發票百分比
    k = 0

    # print("%.2f" % fr ,"%\n") #打印各張發票辨識率百分比時，取消井字

    # 判斷百分比
    if fr > 80:
        h += 1
    elif 50 < fr < 80:
        m += 1
    else:
        l += 1
# 打印結果
print("高於80%:", h, "張，佔", int(h / df2.shape[0] * 100), "%")
print("高於50%低於80%:", m, "張，佔", int((m) / df2.shape[0] * 100), "%")
print("低於50%:", l, "張，佔", int(l / df2.shape[0] * 100), "%")

# 將結果畫成圓餅圖
labels = "80%↑", "80%↓,50%↑", "50%↓"
size = [
    int(h / df2.shape[0] * 100),
    int((m) / df2.shape[0] * 100),
    int(l / df2.shape[0] * 100),
]
plt.pie(size, labels=labels, autopct="%1.1f%%")
plt.axis("equal")
plt.show()
