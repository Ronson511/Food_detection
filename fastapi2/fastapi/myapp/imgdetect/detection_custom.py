#================================================================
#
#   File name   : detection_custom.py
#   Author      : PyLessons
#   Created date: 2020-09-17
#   Website     : https://pylessons.com/
#   GitHub      : https://github.com/pythonlessons/TensorFlow-2.x-YOLOv3
#   Description : object detection image and video example
#
#================================================================
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
import cv2
import numpy as np
import tensorflow as tf
from yolov3.utils import detect_image,Load_Yolo_model
from yolov3.configs import *


def load_cnn_data(double_check_list):
    w, h = 128, 128
    x=[]
    
    for fp in double_check_list:

        img = cv2.resize(fp,(w,h),interpolation = cv2.INTER_AREA)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        x.append(img_rgb)
        x_arr = np.asarray(x).astype('float32')
        x_arr = x_arr/255
        x_arr = x_arr.reshape(x_arr.shape[0],w,h,3)
    return x_arr

def food_name(food):
    ret = []

    for i in food:
        if i == 0:
            ret.append("牛肉")
        elif i == 1:
            ret.append("水煮蛋")
        elif i == 2:
            ret.append("花椰菜")
        elif i == 3:
            ret.append("高麗菜")
        elif i == 4:
            ret.append("雞肉")
        elif i == 5:
            ret.append("鯖魚")
        elif i == 6:
            ret.append("番薯")
        elif i == 7:
            ret.append("鮭魚")
        elif i == 8:
            ret.append("番茄")
    return ret


block_image_path = "./block"
image_path   = "./test10.jpg"
video_path   = "./IMAGES/test2.mp4"

yolo = Load_Yolo_model()
image = cv2.imread(image_path)
ret_image,cord = detect_image(yolo, image_path, output_path ="./answer.jpg", input_size=YOLO_INPUT_SIZE, show=True, CLASSES=TRAIN_CLASSES, rectangle_colors=(255,0,0))

double_check_list = []
for i,block in enumerate(cord):
    x1 = block[0][0]
    x2 = block[1][0]
    y1 = block[0][1]
    y2 = block[1][1]
    crop_img = image[y1:y2, x1:x2]
    double_check_list.append(crop_img)
    #cv2.imwrite(f"./block/block_{i}.jpg", crop_img)
    
x_test = load_cnn_data(double_check_list)
reload_model = tf.keras.models.load_model('./cnn_model/resNet_model3_w128_h128.h5')

predict_class = reload_model.predict(x_test)
predict_class = np.argmax(predict_class,axis=1)

ret = food_name(predict_class)
print(ret)

