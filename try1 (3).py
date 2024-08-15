from paddleocr import PaddleOCR,draw_ocr
# Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# You can set the parameter `lang` as `ch`, `en`, `fr`, `german`, `korean`, `japan`
# to switch the language model in order.
from PIL import Image
import time
import cv2
import os

import tools.infer.predict_rec as predict_rec
from tools.infer.utility import draw_ocr_box_txt, get_rotate_crop_image, get_minarea_rect_crop
ocr = PaddleOCR(lang='en', use_gpu= True, rec= True, use_angle = False) # need to run only once to download and load model into memory

font = cv2.FONT_HERSHEY_SIMPLEX
org = (50, 50)
fontScale = 1
color = (0, 255, 0)
thickness = 4
ij = 0
dir1 = 'C:/Users/User/Desktop/New_Batch_Code/sample/'
# dir1 = os.path.join(os.getcwd(),'laser')
start = time.time()
for filename in os.listdir(dir1):
        img_name = filename
        filename = os.path.join(dir1,filename)
        print(filename)
      
        result = ocr.ocr(filename)
        print("Total Time Taken",time.time()-start)
        lines = []
        for idx in range(len(result)):
            res = result[idx]
            for line in res:
                #print("AAAAAAAA", line)
                lines.append(line)

        result2 = result[0]
        
        fi = open(dir1 + img_name.replace('.jpg','.txt'),'a')
        for recog_values in result2:
            rec_coord = str((recog_values[0])).replace('[[','').replace('[','').replace(']]','').replace(']','').replace('.0','')
            rec_label2 = recog_values[1][0]
            final_result = str(rec_coord) + ', ' + str(rec_label2)
            fi.write(final_result)
            fi.write('\n')
        # fi.close()
#         boxes = [line[0] for line in result]
#         txts = [line[1][0] for line in result]
#         scores = [line[1][1] for line in result]
#         #print("Txt ",txts, "Scores ", scores)
#         #print("Lines ", lines[0])
        
#         #img = cv2.imread(img_path)
#         y_first_center = 30
#         if det1 == True and rec1 == True:
#             for k in range(len(lines)):
#                 #print("Lines 1: ", lines[k][0])
#                 for j in range(len(lines[k][0])):
#                     #print("Points: ", lines[k][j][0], lines[k][j][1])
#                     if j < len(lines[k][0])-1:
#                         p = j+1
#                     else:
#                         p =0
#                     x1 = (int(float(lines[k][0][j][0])), int(float(lines[k][0][j][1])))
#                     x2 = (int(float(lines[k][0][p][0])), int(float(lines[k][0][p][1])))          
#                     cv2.line(img, x1,x2, (255,0,0), 2)
#                 first_center = (10, y_first_center)
#                 y_first_center += 40
#                 cv2.putText(img, str(lines[k][1][0]), first_center, font, fontScale, color, thickness, cv2.LINE_AA)
#         elif det1 == True and rec1 == False:
#             #print(lines)
#             for k in range(len(lines)):
#                 for j in range(len(lines[k])):
#                     # print("Points: ", lines[k][j][0], lines[k][j][1])
#                     if j < len(lines[k])-1:
#                         p = j+1
#                     else:
#                         p =0
#                     x1 = (int(float(lines[k][j][0])), int(float(lines[k][j][1])))
#                     x2 = (int(float(lines[k][p][0])), int(float(lines[k][p][1])))    
#                     cv2.line(img, x1,x2, (255,0,0), 2)
                    
        
# cv2.destroyAllWindows()

