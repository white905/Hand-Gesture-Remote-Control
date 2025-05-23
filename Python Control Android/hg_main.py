import cv2
import time
import mediapipe as mp
import hg_function, hg_global
from cv2 import FONT_HERSHEY_SIMPLEX
from ppadb.client import Client as AdbClient

# 變數區域
ctime = 0
ptime = 0
output_word = '?'
mpHands = mp.solutions.hands
video = cv2.VideoCapture(0)
hands = mpHands.Hands()

# 連線至裝置
def connect():
    client = AdbClient(host="127.0.0.1", port=5037) # Default is "127.0.0.1" and 5037
    devices = client.devices()

    if len(devices) == 0:
        print('No devices')
        quit()

    hg_global.device = devices[0]
    print(f'Connected to {hg_global.device}')
    return hg_global.device, client

if __name__ == '__main__':
    hg_global.device, client = connect()

# 主程式
while True:
    ret, img = video.read()
    ctime = time.time()
    cv2.putText(img, hg_global.mode_kind[hg_global.mode], (50, 50), FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0))
    cv2.putText(img, f'{output_word}', (50, 20), FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0))

    # 投影畫面
    cv2.imshow('img', img)

    # 每隔1秒判斷一次
    if (ctime - ptime >= 2):
        ptime = ctime

        if ret:
            imgHeight = img.shape[0]
            imgWidth = img.shape[1]

            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            result = hands.process(imgRGB)
            if result.multi_hand_landmarks:
                for handLms in result.multi_hand_landmarks:

                    # 取得第0, 1, 5節點座標
                    for l in [0, 1, 5]:
                        hg_global.x_train[l, 0] = int(handLms.landmark[l].x * imgWidth)
                        hg_global.x_train[l, 1] = int(handLms.landmark[l].y * imgHeight)

                    x0 = hg_global.x_train[0, 0]
                    y0 = hg_global.x_train[0, 1]

                    # 取得預處理所需參數
                    hg_function.get_parameters()

                    # 各節點處理
                    for i, lm in enumerate(handLms.landmark):
                        xPos = int(lm.x * imgWidth)
                        yPos = int(lm.y * imgHeight)

                        # 紀錄節點0座標並設為為基準
                        xPos = xPos - x0
                        yPos = yPos - y0

                        # 節點預先處理並儲存
                        hg_function.node_preprocess(i, xPos, yPos)

                    # 導入模型進行預測
                    hg_function.model_predict()

                    # 準確率
                    # print(predict[0][predict_max[0]])

                    # 去除雜訊
                    noise = hg_function.remove_noise()
                    if noise == True:
                        continue

                    # mode切換
                    hg_function.mode_change()

                    # 顯示辨識結果
                    if (hg_global.mode == 0 or hg_global.mode == 1):
                        output_word = chr(hg_global.predict_max + 97)
                    elif (hg_global.mode == 2):
                        output_word = chr(hg_global.predict_max + 48)

                    # 對應模式執行指令
                    hg_function.correspond_mode()

                    # 輸出指令
                    hg_function.output_command()

                    # 還原初始值
                    hg_function.restore_initial_value()

    # 停止程式
    if cv2.waitKey(1) == ord('q'):
        break
