from paddleocr import PaddleOCR,draw_ocr
from PIL import Image
import time
import cv2
import os
import time
import glob
start = time.time()
import re
ocr = PaddleOCR(use_angle_cls=False, lang='en', det = True, use_gpu= False, rec= True )
path = 'C:/Users/User/Desktop/Batch_Code_Updated/One_click_training/Recognition/recognition_working_directory/tuesday_front/cropped'
dir1 = sorted(glob.glob( os.path.join(path, '*.jpg') ),key=lambda x:float(re.findall("([0-9]+?)\.jpg",x)[0]))
for img_path in dir1:
    start = time.time()
    path,filename = img_path.split('\\')
    result = ocr.ocr(img_path, cls=False, rec= True, det = False)
    for res in result:
        for re in res:
            new_text = str(filename) + ',' + '"' + re[0] + '"'
            print(new_text)
            print("Total time taken",time.time() - start)
            img = cv2.imread(img_path)
            # cv2.imshow("Image",img)     
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            


        with open('C:/Users/User/Desktop/Batch_Code_Updated/One_click_training/Recognition/recognition_working_directory/tuesday_front/cropped/result.txt','a') as f:
            f.writelines(new_text)
            f.write('\n')
            f.close()



