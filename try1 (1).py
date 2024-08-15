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
ocr = PaddleOCR(warm_up = True, use_angle_cls=False, lang='en', use_gpu= false, rec= True) # need to run only once to download and lddoad model into memory

# cuda_stream = cv2.cuda_Stream()
font = cv2.FONT_HERSHEY_SIMPLEX
org = (50, 50)
fontScale = 1
color = (0, 255, 0)
thickness = 4
dir1 = os.getcwd()
badcount = 0
ij = 0
#os.chdir('oral')
dir1 = os.path.join(os.getcwd(),"")
# dir1 = r'C:\Users\User\Desktop\metal\metal_ocr'
for filename in os.listdir(dir1):
    if (filename.endswith(".jpg")):
        ij += 1
        if ij % 100 == 0:
            print("Running", ij)
        img_path = os.path.join(dir1, filename)
        img = cv2.imread(img_path)
        x = img.shape
        orig_x = img.shape
        print("Before Image",img.shape)
        ###########h = 736 is the minimum height for the model###########
        h = 736
        w = int(h*x[1]/x[0])

        dim = (w,h)
        img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        print("After Image",img.shape)
        rec1 = True
        det1 = True
        #print(img.shape, "SHAPE")
        st = time.time()
        result = ocr.ocr(img, cls=False, rec= rec1, det = det1)
        print("All Info _____________________________",result)
        st2 = time.time()
        print("Model Time",st2-st)
        lines = []
        for idx in range(len(result)):
            res = result[idx]
            for line in res:
                # print("AAAAAAAA", line)
                lines.append(line)
        result = result[0]

        org_boxes = [line[0] for line in result]
        txts = [line[1][0] for line in result]
        scores = [line[1][1] for line in result]
        try:
            first_box = org_boxes[0][0][0]
            second_box = org_boxes[1][0][0]
        
            lines = []
            if int(first_box) > int(second_box):
                boxes = [org_boxes[1], org_boxes[0], org_boxes[2]]
                labels = [txts[1], txts[0], txts[2]]
                confidence = [scores[1], scores[0], scores[1]]
                for b,c,d in zip(boxes,labels,confidence):
                    final = [b,(c,d)]
                    lines.append(final)
            else:
                boxes = org_boxes
                labels = txts
                confidence = scores
                for b,c,d in zip(boxes,labels,confidence):
                    final = [b,(c,d)]
                    lines.append(final)
        except IndexError as e:
            pass
            
        y_first_center = 70
        string_rec = []
        if det1 == True and rec1 == True:
            for k in range(len(lines)):
                for j in range(len(lines[k][0])):
                    # print("Points:", lines[k][j][0], lines[k][j][1])
                    if j < len(lines[k][0])-1:
                        p = j+1
                    else:
                        p =0
                    x1 = (int(float(lines[k][0][j][0])), int(float(lines[k][0][j][1])))
                    x2 = (int(float(lines[k][0][p][0])), int(float(lines[k][0][p][1])))          
                    cv2.line(img, x1,x2, (255,0,0), 2)
                first_center = (20, y_first_center)
                y_first_center += 40
                cv2.putText(img, str(lines[k][1][0]), first_center, font, fontScale, color, thickness, cv2.LINE_AA)

                string_rec.append(str(lines[k][1][0]))
        elif det1 == True and rec1 == False:
      
            for k in range(len(lines)):
                for j in range(len(lines[k])):
                    if j < len(lines[k])-1:
                        p = j+1
                    else:
                        p =0
                    x1 = (int(float(lines[k][j][0])), int(float(lines[k][j][1])))
                    x2 = (int(float(lines[k][p][0])), int(float(lines[k][p][1])))    
                    cv2.line(img, x1,x2, (255,0,0), 2)
      
        h = 400
        w = int(h*orig_x[1]/orig_x[0])+100
        dim = (w,h)
        img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        print("Total Time",time.time() - st)
        cv2.imshow("Img", img)
        filename = str(time.time())
        # cv2.imwrite(dir1+filename+'.jpg',img)
        cv2.waitKey(0)    
        #time.sleep(0.01)d
        cv2.destroyAllWindows()
        
