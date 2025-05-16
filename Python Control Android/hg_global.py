import numpy as np

global cmd
global mode
global device
global x_turn
global y_turn
global x_train
global mode_kind
global predict_max
global predict_result
global length_standard

cmd = -1
mode = 1
device = None
x_turn = False
y_turn = False
predict_max = 100
length_standard = 0
predict_result = None
x_train = np.empty([21, 2])
mode_kind = ['tool mode', 'English mode', 'Number mode']
