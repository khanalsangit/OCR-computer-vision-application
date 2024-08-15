from paddleocr import PaddleOCR,draw_ocr
from PIL import Image
import time
import cv2
import os
import labelme 
import base64
import json
import tools.infer.predict_rec as predict_rec
from tools.infer.utility import draw_ocr_box_txt, get_rotate_crop_image, get_minarea_rect_crop

json_dict = {
    'version': '5.1.1',
    'flags': {},
    'shapes': [],
    'imagePath': 0,
    'imageData': 0,
    'imageHeight': 0,
    'imageWidth': 0
}

label_dict = {
    'label': "",
    'points': [],
    'group_id': None,
    'description': None,
    'shape_type': 'polygon',
    'flags': {}
}

ocr = PaddleOCR(lang='en', use_gpu= True, rec= True, use_angle = False)
font = cv2.FONT_HERSHEY_SIMPLEX
org = (50, 50)
fontScale = 1
color = (0, 255, 0)
thickness = 4
ij = 0
dir1 = 'C:/Users/dell/Desktop/overall_ocr_system/sample/'
start = time.time()
for filename in os.listdir(dir1):
    if filename.endswith(".jpg" or ".png"):
        filename = os.path.join(dir1,filename)
        result = ocr.ocr(filename)
        lines = []
        for idx in range(len(result)):
            res = result[idx]
            for line in res:
                lines.append(line)

        result2 = result[0]
        coordinates = []
        labels = []
        image_json_info = json_dict
        xy_coordinate = []
        for recog_values in result2:
            rec_coord = str((recog_values[0])).replace('[[','').replace('[','').replace(']]','').replace(']','').replace('.0','') #### bbox coordinates
            rec_label2 = recog_values[1][0]  ##### labels or characters
            final_coord = rec_coord + ', ' + rec_label2
            line_info = final_coord.replace(' ', '').strip('\n').split(',')
            points, label = [ int(x) for x in line_info[:-1]], line_info[-1]
            xy_coordinate = []
            for i in range(0, len(points), 2):
                xy_coordinate.append([points[i], points[i+1]])
            line_label_dict = label_dict.copy()
            line_label_dict['label'] = label
            line_label_dict['points'] = xy_coordinate
            image_json_info['shapes'].append(line_label_dict)
            line_label_dict = {}
       
        image_path = os.path.join(dir1,filename)
        if os.path.exists(image_path):
            image_json_info['imagePath'] = image_path
            image_json_info['imageData'] = base64.b64encode(
            labelme.LabelFile.load_image_file(image_path)).decode('utf-8')
            image = cv2.imread(image_path)
            height, width, channel = image.shape 
            image_json_info['imageHeight'] = height
            image_json_info['imageWidth'] = width
            with open(os.path.join(dir1,filename.replace('.jpg','.json')), 'w+') as json_file:
                json.dump(image_json_info, json_file)
            print("File has saved")    
        else:
            print('[-] could not generate file for : ',filename)
        image_json_info['shapes'] = []
        del image_json_info 

