'''涵式'''
import time
import hg_global
import numpy as np
from math import sqrt
from keras.models import load_model

'''參數'''
# 下載model
model_english = load_model('0320_2+9+12+13+生物+物理-english_lr=0.5-2-100-40.h5')
model_number = load_model('0320_2+9+12+13+生物+物理-number_lr=0.3-2-100-40.h5')

# 拍攝照片座標
shot = '550 2035'

# 中心點座標
center = '550 1200'

# 滑動座標
upswipe = '500 300 500 600'
downswipe = '500 600 500 300'
leftswipe = '100 800 1000 800'
rightswipe = '1000 800 100 800'

# 搜尋座標
search_bar_num = 0
search_bar = ['870 160', '440 200']
youtube_coordinate = ['500 650', '500 1700']
phone_coordinate = ['790 2050 790 1000', '550 2050', '300 2050 300 1000']

'''主程式涵式區'''
# 取得預處理所需參數
def get_parameters():
    # 節點1為基準，x值固定正
    if hg_global.x_train[1, 0] - hg_global.x_train[0, 0] >= 0:
        hg_global.x_turn = False
    else:
        hg_global.x_turn = True

    # 節點1為基準，y值固定正
    if hg_global.x_train[1, 1] - hg_global.x_train[0, 1] >= 0:
        hg_global.y_turn = False
    else:
        hg_global.y_turn = True

    # 取得節點0 ~ 5距離
    x5 = hg_global.x_train[5, 0] - hg_global.x_train[0, 0]
    y5 = hg_global.x_train[5, 1] - hg_global.x_train[0, 1]
    hg_global.length_standard = sqrt(x5 * x5 + y5 * y5)

# 對節點進行預先處理並儲存
def node_preprocess(i, xPos, yPos):
    # 翻正
    if hg_global.x_turn == True:
        xPos = -xPos
    if hg_global.y_turn == True:
        yPos = -yPos

    # 以0 ~ 5座標距離為準進行縮放並存入x_train
    hg_global.x_train[i, 0] = (xPos / hg_global.length_standard)
    hg_global.x_train[i, 1] = (yPos / hg_global.length_standard)

# 導入模型預測
def model_predict():
    hg_global.x_train = hg_global.x_train.reshape((1, 42))
    if hg_global.mode == 0 or hg_global.mode == 1:
        hg_global.predict_result = model_english.predict(hg_global.x_train)
    elif hg_global.mode == 2:
        hg_global.predict_result = model_number.predict(hg_global.x_train)
    predict_order = np.argmax(hg_global.predict_result, axis = -1)
    hg_global.predict_max = predict_order[0]

# 移除雜訊
def remove_noise():
    if hg_global.predict_result[0][hg_global.predict_max] < 0.7:
        hg_global.predict_max = 100
        print("Recognition failed!")
        restore_initial_value()
        return True

# 切換模式
def mode_change():
    if hg_global.predict_max == 26:
        print('切換模式')
        hg_global.mode = (hg_global.mode + 1) % len(hg_global.mode_kind)

# 對應模式處理
def correspond_mode():
    if hg_global.mode == 0:
        tool_cmd(hg_global.predict_max)
    elif hg_global.mode == 1:
        english_cmd(hg_global.predict_max)
    elif hg_global.mode == 2:
        number_cmd(hg_global.predict_max)

# 執行指令
def output_command():
    if hg_global.cmd != '-1':
        print("execute command!")
        hg_global.device.shell(f'input keyevent {hg_global.cmd}')
        hg_global.cmd = '-1'

# 初始化設置
def restore_initial_value():
    # 將陣列歸零
    hg_global.x_train = np.delete(hg_global.x_train, slice(0, 42))
    hg_global.x_train = np.zeros([21, 2])

'''功能'''
# 搜尋
def search():
    query = input('你想搜尋(英文)：\n')
    search_query = f'{query}'
    hg_global.device.shell(f'input tap {search_bar[search_bar_num]}')
    hg_global.device.shell(f'input text "{search_query}"')
    time.sleep(1)
    hg_global.device.shell('input keyevent 66')
    time.sleep(1)

# 螢幕截圖
def screenshot():
    screenshot = hg_global.device.screencap()
    with open('result.png', 'wb') as f:
        f.write(screenshot)
        print('截圖已存檔！')

# 開啟程式
def appOpen():
    global search_bar_num
    command = {"youtube" : 'com.google.android.youtube/.HomeActivity',
           "line" : 'jp.naver.line.android/.activity.SplashActivity',
           "facebook" : 'com.facebook.katana/.LoginActivity',
           "google play" : 'com.android.vending/.AssetBrowserActivity',
           "google" : 'com.android.chrome/org.chromium.chrome.browser.ChromeTabbedActivity',
           "arknights" : 'tw.txwy.and.arknights/com.u8.sdk.U8UnityContext',
           "camera" : 'com.android.camera/.Camera'}
    print(command.keys())
    Input = input('which app do you want to open?\n')
    if Input == 'youtube':
        search_bar_num = 0
    elif Input == 'google':
        search_bar_num = 1
    hg_global.device.shell(f'am start -n {command[Input]}')

# youtube選擇影片
def choose():
    choose = input('Which one?')
    hg_global.device.shell(f'input tap {youtube_coordinate[int(choose) - 1]}')

'''模式'''
# 工具模式
def tool_cmd(predict_max):
    # a
    if predict_max == 0:
        hg_global.cmd = '26'
    # b
    elif predict_max == 1:
        hg_global.cmd = '3'
    # c
    elif predict_max == 2:
        hg_global.cmd = '4'
    # d
    elif predict_max == 3:
        hg_global.cmd = '221'
    # e
    elif predict_max == 4:
        hg_global.cmd = '220'
    # f
    elif predict_max == 5:
        hg_global.cmd = '24'
    # g
    elif predict_max == 6:
        hg_global.cmd = '25'
    # h
    elif predict_max == 7:
        hg_global.cmd = '19'
    # i
    elif predict_max == 8:
        hg_global.cmd = '20'
    # j
    elif predict_max == 9:
        hg_global.cmd = '21'
    # k
    elif predict_max == 10:
        hg_global.cmd = '22'
    # l
    elif predict_max == 11:
        hg_global.cmd = '66'
    # m
    elif predict_max == 12:
        hg_global.cmd = '67'
    # n
    elif predict_max == 13:
        hg_global.device.shell(f'input swipe {phone_coordinate[0]}')
    # o
    elif predict_max == 14:
        hg_global.device.shell(f'input tap {phone_coordinate[1]}')
    # p
    elif predict_max == 15:
        hg_global.device.shell(f'input swipe {phone_coordinate[2]}')
    # q
    elif predict_max == 16:
        hg_global.device.shell(f'input tap {shot}')
    # r
    elif predict_max == 17:
        screenshot()
    # s
    elif predict_max == 18:
        appOpen()
    # t
    elif predict_max == 19:
        search()
    # u
    elif predict_max == 20:
        choose()
    # v
    elif predict_max == 21:
        hg_global.device.shell('input keyevent --longpress KEYCODE_POWER')
    # w
    elif predict_max == 22:
        hg_global.device.shell(f'input tap {center}')
        hg_global.device.shell(f'input tap {center}')
    # x
    elif predict_max == 23:
        hg_global.device.shell('input getevent')
    # y
    elif predict_max == 24:
        hg_global.device.shell('input sendevent')
    # z
    elif predict_max == 25:
        hg_global.device.shell('input wm density reset')

# 英文模式
def english_cmd(predict_max):
    hg_global.cmd = f'{predict_max + 29}'

# 數字模式
def number_cmd(predict_max):
    hg_global.cmd = f'{predict_max + 7}'
