'''
将labelme打完标签后的json格式，代码处理为png格式
'''
import os
import json
import cv2
import numpy as np
from PIL import Image, ImageDraw

CLASS_NAMES = ['/Users/yangjing/Desktop/machine-vision/exa4_code/bag']  # 根据实际改


# 创造一个和数据图片大小一样的二值化图片

def make_mask(image_dir, save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    data = os.listdir(image_dir)
    temp_data = []
    for i in data:
        if i.split('.')[1] == 'json':
            temp_data.append(i)
        else:
            continue
    for js in temp_data:
        json_data = json.load(open(os.path.join(image_dir, js), 'r'))
        # shapes[{},{},{}]
        shapes_ = json_data['shapes']
        # 原始图像格式（本项目是png）
        mask = Image.new('P', Image.open(os.path.join(image_dir, js.replace('json', 'png'))).size)
        for shape_ in shapes_:
            label = shape_['label']
            points = shape_['points']
            points = tuple(tuple(i) for i in points)
            # mask = Image.new('P', Image.open(os.path.join(image_dir, js.replace('json', 'jpg'))).size)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.polygon(points, fill=CLASS_NAMES.index(label) + 1)  # fill参数为整数时默认为灰度图
        '''查看高亮之后的图片，默认不查看
        mask_test=np.array(mask)*255
        cv2.imshow('mask_test',mask_test)
        cv2.waitKey(0)
        '''
        # 输出图像格式（本项目是png）
        mask.save(os.path.join(save_dir, js.replace('json', 'png')))


def vis_label_classs(img_path):
    img = keep_image_size_open(img_path)
    img = np.array(img)
    print('图片类别（0表示背景，1,2,3...表示类别）：')
    print(set(img.reshape(-1).tolist()))


if __name__ == '__main__':
    make_mask('/Users/yangjing/Desktop/machine-vision/exa4_code/bag', './Segmentationmask')
