import os, pathlib
import cv2
import numpy as np
import tensorflow as tf
from .yolov3.utils import detect_image, Load_Yolo_model
from .yolov3.configs import *

mod_path = os.path.relpath(os.path.dirname(__file__))
mod_parent =  os.path.relpath(pathlib.Path(mod_path).parent)

os.environ['CUDA_VISIBLE_DEVICES'] = 'cpu'

tf.compat.v1.reset_default_graph()
yolo = Load_Yolo_model()
reload_model = tf.keras.models.load_model(os.path.join(mod_path, 'cnn_model','resNet_34_batch_size_10_w128_h128.h5'))

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

_name = ["牛肉", "水煮蛋", "花椰菜", "高麗菜", "雞肉", "鯖魚", "番薯", "鮭魚", "番茄"]
_nutrion = {
    "牛肉": ['I0100201','肉類','牛肋條','225','63.3','18.6','16.2','1.1','0','81','347','10','15','2.7','6.7','6','0.11','0.06','0.17','2.64','0.17','0.2'],
    "水煮蛋": ['K01001','蛋類','雞蛋平均值','134','75.9','12.5','8.8','1.8','0','140','136','43','11','1.9','1.3','548','1.81','0.09','0.49','0.12','0.11','0.6'],
    "花椰菜": ['E5800101','蔬菜類','花椰菜','19','93.0','1.8','0.1','4.5','2.0','14','266','21','12','0.6','0.3','9','0.18','0.04','0.05','0.42','0.21','62.2'],
    "高麗菜": ['E30001','蔬菜類','甘藍平均值','21','93.2','1.3','0.1','4.8','1.1','11','187','47','12','0.4','0.3','52','0.24','0.03','0.02','0.24','0.17','37.2'],
    "雞肉": ['I04024','肉類','去皮清肉平均值','119','74.1','23.3','2.1','0','0','50','314','4','30','0.7','0.8','25','0.28','0.15','0.09','10.01','0.56','2.4'],
    "鯖魚": ['J0414101','魚貝類','花腹鯖','144','70.5','23.9','4.6','0','0','36','368','27','36','2.8','0.7','110','0.13','0.13','0.27','9.40','0.33','0.0'],
    "番薯": ['B0400601','澱粉類','黃肉甘薯','115','70','1.3','0.2','27.8','2.5','51','276','46','24','0.3','0.2','116','0.50','0.13','0.04','0.51','0.23','19.8'],
    "鮭魚": ['J0402301','魚貝類','紅肉鮭魚切片','158','69.6','24.3','6.0','0','0','72','440','8','34','0','1.1','205','1.12','0.22','0.18','6.80','0.78','2.7'],
    "番茄": ['E74001','蔬菜類','大番茄平均值(紅色系)','17','94.5','0.8','0.1','4.1','1.0','2','217','10','9','0.3','0.3','1692','0.69','0.04','0.02','0.37','0.11','14.0'],
}
def food_name(food):
    return [_name[i] for i in food]

def aiPredict(image_path):
    # block_image_path = "./block"
    # image_path   = "./test10.jpg"
    # video_path   = "./IMAGES/test2.mp4"

    # image = cv2.imread(image_path)
    opath = os.path.join(mod_path, "answer.jpg")
    image, _, cord = detect_image(yolo, image_path, output_path=opath , input_size=YOLO_INPUT_SIZE, show=False, CLASSES=TRAIN_CLASSES, rectangle_colors=(255,0,0))

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

    predict_class = reload_model.predict(x_test)
    predict_class = np.argmax(predict_class,axis=1)

    result = set(food_name(predict_class))
    # ret = [["每百公克", "熱量(kcal)","蛋白質(g)","脂肪(g)","碳水化合物(g)","膳食纖維(g)","鈉(mg)"]]
    # ret.extend( [[i, _nutrion[i][3], _nutrion[i][5], _nutrion[i][6], _nutrion[i][7], _nutrion[i][8], _nutrion[i][9]] for i in result ] )
    ret = [["每百克", "熱量","蛋白質","脂肪","碳水化合", "膳食纖維", "鈉"]]
    ret.extend( [[i, _nutrion[i][3]+'kcal', _nutrion[i][5]+'g', _nutrion[i][6]+'g',
                     _nutrion[i][7]+'g', _nutrion[i][8]+'g', _nutrion[i][9]+'mg'] for i in result ] )
    # for i in ret:
    #     print(",".join(i))
    # print(ret)
    return ret


