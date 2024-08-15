from paddleocr import PaddleOCR
from PIL import Image
import time
import cv2
import os

# Create PaddleOCR instance with warm-up enabled
ocr = PaddleOCR(warm_up=True, use_angle_cls=False, lang='en', use_gpu=True, rec=True)

font = cv2.FONT_HERSHEY_SIMPLEX
color = (0, 255, 0)
thickness = 4
fontScale = 1
dir1 = os.getcwd()
badcount = 0
ij = 0
dir1 = r'C:/Users/User/Desktop/OCR/GUI/test'

def perform_gpu_processing(image):
    # Perform some GPU-accelerated processing here
    # Example: Resize the image using OpenCV's CUDA module
    dsize = (800, 600)
    img_gpu = cv2.cuda_GpuMat()
    img_gpu.upload(image)
    img_resized_gpu = cv2.cuda.resize(img_gpu, dsize, interpolation=cv2.INTER_LINEAR)
    img_resized = img_resized_gpu.download()
    return img_resized

for filename in os.listdir(dir1):
    if (filename.endswith(".jpg")):
        ij += 1
        if ij % 100 == 0:
            print("Running", ij)
        img_path = os.path.join(dir1, filename)
        img = cv2.imread(img_path)
        x = img.shape
        orig_x = img.shape
        h = 736
        w = int(h * x[1] / x[0])
        dim = (w, h)
        img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        rec1 = True
        det1 = True
        st = time.time()
        result = ocr.ocr(img, cls=False, rec=rec1, det=det1)
        st2 = time.time()
        print("Total Time Taken 11111111", st2 - st)

        # Process the OCR result as needed (e.g., draw bounding boxes, text)
        
        lines = []
        for idx in range(len(result)):
            res = result[idx]
            for line in res:
                #print("AAAAAAAA", line)
                lines.append(line)

        result = result[0]

        boxes = [line[0] for line in result]
        txts = [line[1][0] for line in result]
        scores = [line[1][1] for line in result]
        #print("Txt ",txts, "Scores ", scores)
        #print("Lines ", lines[0])
        
        #img = cv2.imread(img_path)
        y_first_center = 70
        string_rec = []
        if det1 == True and rec1 == True:
            for k in range(len(lines)):
                for j in range(len(lines[k][0])):
                    # print("Points 1: ", lines[k][j][0], lines[k][j][1])
                    if j < len(lines[k][0])-1:
                        p = j+1
                    else:
                        p =0
                    x1 = (int(float(lines[k][0][j][0])), int(float(lines[k][0][j][1])))
                    x2 = (int(float(lines[k][0][p][0])), int(float(lines[k][0][p][1])))          
                    cv2.line(img, x1,x2, (255,0,0), 2)
                first_center = (70, y_first_center)
                y_first_center += 40
                cv2.putText(img, str(lines[k][1][0]), first_center, font, fontScale, color, thickness, cv2.LINE_AA)

                string_rec.append(str(lines[k][1][0]))
        elif det1 == True and rec1 == False:
            #print(lines)
            for k in range(len(lines)):
                for j in range(len(lines[k])):
                    print("Points 2: ", lines[k][j][0], lines[k][j][1])
                    if j < len(lines[k])-1:
                        p = j+1
                    else:
                        p =0
                    x1 = (int(float(lines[k][j][0])), int(float(lines[k][j][1])))
                    x2 = (int(float(lines[k][p][0])), int(float(lines[k][p][1])))    
                    cv2.line(img, x1,x2, (255,0,0), 2)
        print("L1",string_rec)
        h = 400
        w = int(h*orig_x[1]/orig_x[0])
        dim = (w,h)
        img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        cv2.imshow("Img", img)
        cv2.waitKey(0)    
        # cv2.destroyAllWindows()

        # Perform GPU-accelerated processing to keep the GPU busy
        img_processed = perform_gpu_processing(img)

        # Display the processed image
        print(img_processed)

        # If needed, introduce a small delay to prevent the GPU from going idle
        time.sleep(0.1)

cv2.destroyAllWindows()
