######################### Developed By Crimson Tech Pvt. Ltd. #####################################
################# Diwash Poudel , Chhabi Lal Tamang , Samvandha Pathak ############################

###### python libraries ###################
import sys
import threading
import numpy as np
import cv2
import pickle
import time
import sys, os
import datetime
import inspect
import ctypes
import random
import PIL.Image
from PIL import Image,ImageTk
from collections import deque
from ctypes import *
import re
import datetime
import nepali_datetime
import pkg_resources

###### tkinter libraries #################
import tkinter as tk
import tkinter.messagebox
from tkinter import * 
from tkinter.messagebox import *
from tkinter import messagebox

########### camera libraries
sys.path.append("../MvImport")
from MvCameraControl_class import *

############### ocr libraries ###############
from paddleocr import PaddleOCR, draw_ocr
import tools.infer.predict_rec as predict_rec
from tools.infer.utility import draw_ocr_box_txt, get_rotate_crop_image, get_minarea_rect_crop

############### Initial color for last ten colors #################
color = deque(['white', 'white', 'white','white','white',
               'white', 'white', 'white','white','white'], maxlen=10)

################ Loading existing pickle file ######################
dir_file = os.path.join(os.getcwd() +'\Pickle')
brand_values = pickle.load(open(dir_file + '\\' +os.listdir(dir_file)[0],'rb'))
print("Brand Values",brand_values)

def check_license_key():
    # x= os.popen('wmic bios get serialnumber').read().replace('\n','').replace("	","").replace(" ","")[12:]
    #x= os.popen('wmic csproduct get uuid').read().replace('\n','').replace("	","").replace(" ","")
    for package in pkg_resources.working_set:
        if "numpy" in str(package):
            x = str(time.ctime(os.path.getctime(package.location)))
    print(os.getcwd())
    text_file = open("license.txt", "r")
    lines = text_file.readlines()[0]
    lines = lines.replace('[', '')
    lines = lines.replace(']', '')
    lines = lines.replace(' ', '')
    xlines = lines.split(',')
    license1 = []
    length =len(x)
    for k in range(len(x[:length])):
        #print(int(ord(x[k])), "ORD")
        y = len(x)-k-1
        z = ((int(ord(x[k])))**2+3*int(ord(x[k]))+2)*(int(ord(x[y])))**2+3*int(ord(x[y]))
        license1.append(z)
    license1 = np.array(license1)
    pass1 = 1
    for j in range(len(license1)):
        #print(int(license1[j]), int(xlines[j]))
        if int(license1[j]) == int(xlines[j]):
            pass1 = 1
        else:
            print('License Failed.')
            quit()
    print("License Passed")

# check_license_key()

def Async_raise(tid, exctype):
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

def Stop_thread(thread):
    Async_raise(thread.ident, SystemExit)


class CameraOperation():
    ocr = PaddleOCR(use_angle_cls=False, lang='en')
    global dec
    dec=0
    def __init__(self,obj_cam,st_device_list,n_connect_num=0,b_open_device=False,b_start_grabbing = False,h_thread_handle=None,\
                b_thread_closed=False,st_frame_info=None,b_exit=False,b_save_bmp=False,b_save_jpg=False,buf_save_image=None,\
                n_save_image_size=0,n_win_gui_id=0,frame_rate=0,exposure_time=0,gain=0,data_good=0,data_not_good=0,data_reset=0):

        self.obj_cam = obj_cam
        self.st_device_list = st_device_list
        self.n_connect_num = n_connect_num
        self.b_open_device = b_open_device
        self.b_start_grabbing = b_start_grabbing 
        self.b_thread_closed = b_thread_closed
        self.st_frame_info = st_frame_info
        self.b_exit = b_exit
        self.b_save_bmp = b_save_bmp
        self.b_save_jpg = b_save_jpg
        self.buf_save_image = buf_save_image
        self.h_thread_handle = h_thread_handle
        self.n_win_gui_id = n_win_gui_id
        self.n_save_image_size = n_save_image_size
        self.b_thread_closed
        self.frame_rate = frame_rate
        self.exposure_time = exposure_time
        self.gain = gain
        self.data_good = data_good
        self.data_not_good = data_not_good
        self.data_reset = data_reset

    def rotate_image(self,image, angle):
    # Get the current value of the variable (rotation angle
        if angle == 90:
            rotated_image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        elif angle == -90:
            rotated_image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        elif angle == 180:
            rotated_image = cv2.rotate(image, cv2.ROTATE_180)
        else:
            rotated_image = image 
        return rotated_image      
    
    def To_hex_str(self,num):
        chaDic = {10: 'a', 11: 'b', 12: 'c', 13: 'd', 14: 'e', 15: 'f'}
        hexStr = ""
        if num < 0:
            num = num + 2**32
        while num >= 16:
            digit = num % 16
            hexStr = chaDic.get(digit, str(digit)) + hexStr
            num //= 16
        hexStr = chaDic.get(num, str(num)) + hexStr   
        return hexStr

    def Open_device(self):
        if False == self.b_open_device:
            # ch:选择设备并创建句柄 | en:Select device and create handle
            nConnectionNum = int(self.n_connect_num)
            stDeviceList = cast(self.st_device_list.pDeviceInfo[int(nConnectionNum)], POINTER(MV_CC_DEVICE_INFO)).contents
            self.obj_cam = MvCamera()
            ret = self.obj_cam.MV_CC_CreateHandle(stDeviceList)
            if ret != 0:
                self.obj_cam.MV_CC_DestroyHandle()
                tkinter.messagebox.showerror('show error','create handle fail! ret = '+ self.To_hex_str(ret))
                return ret

            ret = self.obj_cam.MV_CC_OpenDevice(MV_ACCESS_Exclusive, 0)
            if ret != 0:
                tkinter.messagebox.showerror('show error','open device fail! ret = '+ self.To_hex_str(ret))
                return ret
            print ("open device successfully!")
            self.b_open_device = True
            self.b_thread_closed = False

            # ch:探测网络最佳包大小(只对GigE相机有效) | en:Detection network optimal package size(It only works for the GigE camera)
            if stDeviceList.nTLayerType == MV_GIGE_DEVICE:
                nPacketSize = self.obj_cam.MV_CC_GetOptimalPacketSize()
                if int(nPacketSize) > 0:
                    ret = self.obj_cam.MV_CC_SetIntValue("GevSCPSPacketSize",nPacketSize)
                    if ret != 0:
                        print ("warning: set packet size fail! ret[0x%x]" % ret)
                else:
                    print ("warning: set packet size fail! ret[0x%x]" % nPacketSize)

            stBool = c_bool(False)
            ret =self.obj_cam.MV_CC_GetBoolValue("AcquisitionFrameRateEnable", stBool)
            if ret != 0:
                print ("get acquisition frame rate enable fail! ret[0x%x]" % ret)

            # ch:设置触发模式为off | en:Set trigger mode as off
            ret = self.obj_cam.MV_CC_SetEnumValue("TriggerMode", MV_TRIGGER_MODE_OFF)
            if ret != 0:
                print ("set trigger mode fail! ret[0x%x]" % ret)
            return 0

    def Start_grabbing(self,root,panel,ltc,wr,dt,gng,rtc,wtc,lngiD,cl):
        if False == self.b_start_grabbing and True == self.b_open_device:
            self.b_exit = False
            ret = self.obj_cam.MV_CC_StartGrabbing()
            if ret != 0:
                tkinter.messagebox.showerror('show error','start grabbing fail! ret = '+ self.To_hex_str(ret))
                return
            self.b_start_grabbing = True
            print ("start grabbing successfully!")
            try:
                self.n_win_gui_id = random.randint(1,10000)
                self.h_thread_handle = threading.Thread(target=CameraOperation.Work_thread, args=(self,root,panel,ltc,wr,dt,gng,rtc,wtc,lngiD,cl))
                self.h_thread_handle.start()
                self.b_thread_closed = True
            except:
                tkinter.messagebox.showerror('show error','error: unable to start thread')
                False == self.b_start_grabbing
            
            

    def Stop_grabbing(self):
        if True == self.b_start_grabbing and self.b_open_device == True:
            #退出线程
            if True == self.b_thread_closed:
                Stop_thread(self.h_thread_handle)
                self.b_thread_closed = False
            ret = self.obj_cam.MV_CC_StopGrabbing()
            if ret != 0:
                tkinter.messagebox.showerror('show error','stop grabbing fail! ret = '+self.To_hex_str(ret))
                return
            print ("stop grabbing successfully!")
            self.b_start_grabbing = False
            self.b_exit  = True      

    def Close_device(self):
        if True == self.b_open_device:
            #退出线程
            if True == self.b_thread_closed:
                Stop_thread(self.h_thread_handle)
                self.b_thread_closed = False
            ret = self.obj_cam.MV_CC_CloseDevice()
            if ret != 0:
                tkinter.messagebox.showerror('show error','close deivce fail! ret = '+self.To_hex_str(ret))
                return
                
        # ch:销毁句柄 | Destroy handle
        self.obj_cam.MV_CC_DestroyHandle()
        self.b_open_device = False
        self.b_start_grabbing = False
        self.b_exit  = True
        print ("close device successfully!")

    def Set_trigger_mode(self,strMode):
        if True == self.b_open_device:
            if "continuous" == strMode: 
                ret = self.obj_cam.MV_CC_SetEnumValue("TriggerMode",0)
                if ret != 0:
                    tkinter.messagebox.showerror('show error','set triggermode fail! ret = '+self.To_hex_str(ret))
            if "triggermode" == strMode:
                ret = self.obj_cam.MV_CC_SetEnumValue("TriggerMode",1)
                if ret != 0:
                    tkinter.messagebox.showerror('show error','set triggermode fail! ret = '+self.To_hex_str(ret))
                ret = self.obj_cam.MV_CC_SetEnumValue("TriggerSource",0)
                if ret != 0:
                    tkinter.messagebox.showerror('show error','set triggersource fail! ret = '+self.To_hex_str(ret))

    def Trigger_once(self,nCommand):
        if True == self.b_open_device:
            if 1 == nCommand: 
                ret = self.obj_cam.MV_CC_SetCommandValue("TriggerSoftware")
                if ret != 0:
                    tkinter.messagebox.showerror('show error','set triggersoftware fail! ret = '+self.To_hex_str(ret))

    def Get_parameter(self):
        if True == self.b_open_device:
            stFloatParam_FrameRate =  MVCC_FLOATVALUE()
            memset(byref(stFloatParam_FrameRate), 0, sizeof(MVCC_FLOATVALUE))
            stFloatParam_exposureTime = MVCC_FLOATVALUE()
            memset(byref(stFloatParam_exposureTime), 0, sizeof(MVCC_FLOATVALUE))
            stFloatParam_gain = MVCC_FLOATVALUE()
            memset(byref(stFloatParam_gain), 0, sizeof(MVCC_FLOATVALUE))
            ret = self.obj_cam.MV_CC_GetFloatValue("AcquisitionFrameRate", stFloatParam_FrameRate)
            if ret != 0:
                tkinter.messagebox.showerror('show error','get acquistion frame rate fail! ret = '+self.To_hex_str(ret))
            self.frame_rate = stFloatParam_FrameRate.fCurValue
            ret = self.obj_cam.MV_CC_GetFloatValue("ExposureTime", stFloatParam_exposureTime)
            if ret != 0:
                tkinter.messagebox.showerror('show error','get exposure time fail! ret = '+self.To_hex_str(ret))
            self.exposure_time = stFloatParam_exposureTime.fCurValue
            ret = self.obj_cam.MV_CC_GetFloatValue("Gain", stFloatParam_gain)
            if ret != 0:
                tkinter.messagebox.showerror('show error','get gain fail! ret = '+self.To_hex_str(ret))
            self.gain = stFloatParam_gain.fCurValue
            tkinter.messagebox.showinfo('show info','get parameter success!')

    def Set_parameter(self,exposureTime,gain):    
        # if '' == frameRate or '' == exposureTime or '' == gain:
        #     tkinter.messagebox.showinfo('show info','please type in the text box !')
        #     return
        if True == self.b_open_device:
            ret = self.obj_cam.MV_CC_SetFloatValue("ExposureTime",float(exposureTime))
            # if ret != 0:
            #     tkinter.messagebox.showerror('show error','set exposure time fail! ret = '+self.To_hex_str(ret))

            ret = self.obj_cam.MV_CC_SetFloatValue("Gain",float(gain))
            # if ret != 0:
            #     tkinter.messagebox.sho werror('show error','set gain fail! ret = '+self.To_hex_str(ret))

            # ret = self.obj_cam.MV_CC_SetFloatValue("AcquisitionFrameRate",float(frameRate))
            # if ret != 0:
            #     tkinter.messagebox.showerror('show error','set acquistion frame rate fail! ret = '+self.To_hex_str(ret))

            #tkinter.messagebox.showinfo('show info','set parameter success!')
            
    def rejection_trend(w:str)->None:
        '''
        This function is used to increase value of different headings in rejection trend bar graph.
        '''
        pass
         
    def green_rectangle(self,rectangle_box)->None:
        rectangle_box.configure(bg='green',text='Good',font = ('Inter',9,'bold'))
        color.appendleft('green')
        self.data_good= self.data_good+1


    def orange_rectangle(self,rectangle_box,img_save_d,w:int,h:int,scale:float)->None:
        rectangle_box.configure(bg='orange',text='Not Good',font = ('Inter',9,'bold'))
        color.appendleft('orange')
        dim = (int(w*scale),int(h*scale))
        img_save_d = cv2.resize(img_save_d, dim, interpolation = cv2.INTER_NEAREST)
        cv2.imwrite("PNGI/PNGID.jpg",img_save_d) # save not good detected image
        self.data_good = self.data_good + 1

    def red_blinking(self,rectangle_box,img_save_d,w:int,h:int,scale:float) -> None:
        rectangle_box.configure(bg='red',text='Not Good',font = ('Inter',9, 'bold'))
        color.appendleft('red')
        dim = (int(w*scale),int(h*scale))
        img_save_d1 = cv2.resize(img_save_d, dim, interpolation = cv2.INTER_AREA)
        cv2.imwrite("PNGI/PNGID.jpg",img_save_d1) 
        self.data_not_good = self.data_not_good + 1

    def last_ten_color(canvas,o,color)-> None:
        '''
        This function places color of circles according to result. Red for critical error,
        yellow for minor error, green for no error
        '''
        canvas[0].itemconfig(o[0], fill=color[0])
        canvas[1].itemconfig(o[1], fill=color[1])
        canvas[2].itemconfig(o[2], fill=color[2])
        canvas[3].itemconfig(o[3], fill=color[3])
        canvas[4].itemconfig(o[4], fill=color[4])
        canvas[5].itemconfig(o[5], fill=color[5])
        canvas[6].itemconfig(o[6], fill=color[6])
        canvas[7].itemconfig(o[7], fill=color[7])
        canvas[8].itemconfig(o[8], fill=color[8])
        canvas[9].itemconfig(o[9], fill=color[9])

    
    def detect_time(dt,detection_time):
        dt.configure(text = str(round(detection_time,2))+' sec', height = 1, font = ('Inter',8,'bold'),bg='#ffffff')

    def count_last_nd(gng,LNG):
        gng[2].configure(text =LNG , height = 1, font = ('Inter',8,'bold'),bg='#ffffff')

    def time_nd(cl,last_time,start_time):
        def update_clock(label, start_time,last_time):
            if last_time==0:
                current_time = 0
            else:
                current_time = int(time.time() - start_time)
            cl.config(text=str(current_time)+" sec", font =('Inter',8,'bold'))
        update_clock(cl, start_time,last_time)

    def G_NG_update(gng,G,NG):
        gng[0].configure(text=G, height = 1, font = ('Inter',8,'bold'))
        gng[1].configure(text=NG, height = 1, font = ('Inter',8,'bold'))

    def change_last_image(lngiD):
        try:
            img_cv_Ng = cv2.imread("PNGI/PNGID.jpg")
            img_cv_Ng_w, img_cv_NG_h = img_cv_Ng.shape[1], img_cv_Ng.shape[0]
            ratio_NG = img_cv_Ng_w/img_cv_NG_h
            NG_width = 250
            NG_height = 200
            if img_cv_Ng_w>= img_cv_NG_h:
                width1 = NG_width
                height1 = NG_width/ratio_NG
            else:
                height1 = NG_height
                width1 = NG_height*ratio_NG
            img_NGD = ImageTk.PhotoImage(PIL.Image.open("PNGI/PNGID.jpg").resize((int(width1),int(height1))))
            lngiD.configure(image = img_NGD)
            lngiD.image=img_NGD 
        except Exception as e:
            print(e)                 

    def levenshtein_distance(str1:str, str2:str) -> float:
        '''
        This function calculates difference between two string and gives distance how much they vary. The main 
        feature of this function is it takes order of letter into account. Eg, abce is not equal to acbe
        ''' 
        length_str1= len(str1)
        length_str2 = len(str2)
        dp = np.zeros((length_str1+1, length_str2+1))
        for i in range(length_str1+1):
            dp[i][0] = i

        for j in range(length_str2+1):
            dp[0][j] = j

        for i in range(1, length_str1+1):
            for j in range(1, length_str2+1):
                if str1[i-1] == str2[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = 1 + min(dp[i][j-1], dp[i-1][j], dp[i-1][j-1])

        return dp[length_str1][length_str2]

    def levenshtein_similarity(str1:str, str2:str)-> float:
        '''
        This function gives difference in terms of percentage similarity. Eg, is all elements are similar
        than gives output 100.
        '''
        dist = CameraOperation.levenshtein_distance(str1, str2)
        return (1.0 - (dist / max(len(str1), len(str2)))) * 100.0
    def length_similarity(Thresh,str1:str,str2:str)-> float:
        if Thresh=='LT':
            pattern = r"\[(.*?)\]"
            str3 = re.findall(pattern, str1)
            str3=str(str3).replace('[','').replace(']','').replace("'","")
            if len(str3)>len(str2):
                return (len(str2)/len(str3))*100
            elif len(str3)<len(str2):
                return (len(str3)/len(str2))*100
            else:
                return 100.0

        else:
            str3=str1
            if len(str3)>len(str2):
                return (len(str2)/len(str3))*100
            elif len(str3)<len(str2):
                return (len(str3)/len(str2))*100
            else:
                return 100.0

    def RecogComparison(str1:str,str2:str) -> bool:
        
        if '{' and '}' in str1: #It considers only string inside {}
            str2=str2.replace(" ","")

            if '%time' in str1: #If string given as {%time}
                current_time = datetime.datetime.now().time()
                time_str = current_time.strftime("%H:%M")
                str1=str1.replace("%time",time_str)

            if '%tdatenm'  in str1:
                current_date=nepali_datetime.datetime.now().strftime("%m")
                str1=str1.replace("%tdatenm",current_date)

            if '%tdateny' in str1:
                current_date=nepali_datetime.datetime.now().strftime("%Y")
                str1=str1.replace("%tdateny",current_date)

            if '%tdatem'  in str1:
                current_date=datetime.datetime.now().strftime("%m")
                str1=str1.replace("%tdatem",current_date)

            if '%tdatey' in str1:
                current_date=datetime.datetime.now().strftime("%Y")
                str1=str1.replace("%tdatey",current_date)
            
            str3=str1.replace('{','').replace('}','').replace(' ','')
            
            pattern = r"\{(.*?)\}"
            results = re.findall(pattern, str1)
            all_elements_present=True
            for elements in results:
                if elements not in str2 and elements:
                    all_elements_present=False
                    break

            if all_elements_present:
                #if str3!=str2:
                if CameraOperation.levenshtein_similarity(str1,str2)<float(brand_values['line_per_thresh']):
                    return None
                else:
                    return True
            else:
                return NotImplemented
        
        elif '[' and ']' in str1:
            str2=str2.replace(" ","")
            if CameraOperation.length_similarity('LT',str1,str2)>=float(brand_values['line_per_thresh']):
                
                return True
            
            else:
                
                return False 
         
        else:
            str1=str1.replace(" ","")
            str2=str2.replace(" ","")
            if str1==str2:
                return True
            else:
                #if CameraOperation.levenshtein_similarity(str1,str2)>=float(brand_values['line_per_thresh']):
                if CameraOperation.levenshtein_similarity(str1,str2)>=float(brand_values['line_per_thresh']):
                    return True
                else:
                    return None  # false in other cases # none 
    
    global window_open
    reject_count=0
    window_open=False
    start_time=time.time()

    def reset_counter_values(self):
        self.data_good = 0 
        self.data_not_good = 0 
        self.count_last_nd = 0
    
     ################### Function to delete the images after certain number
    def delete_img(dir_name):
        img_path = os.path.join(brand_values['img_dir'],dir_name)
        img_length = len(os.listdir(img_path))
        if int(img_length) > 10000:
            for i,img in enumerate(os.listdir(img_path)):
                os.remove(os.path.join(img_path,img))
                if i >= 500:
                    break
    
    def Work_thread(self,root,panel,ltc,wr,dt,gng,rtc,wtc,lngiD,cl):
        stOutFrame = MV_FRAME_OUT()  
        img_buff = None
        buf_cache = None
        numArray = None
        global odd_even
        odd_even = 0
        display_width=900
        display_height = 600
        scale=0.3

        #blink_duration=100 #duration of blinking in no detection
        less_than_no_color="black" 
        no_det_color="#FF8C00" #orange
        Line1_error_color="brown"
        Line2_error_color="#800080" #purple
        Line3_error_color="#FF1493" #pink
        Line4_error_color="#808080" #grey
        mean_thres_error_color="yellow"
        

        line_color=[less_than_no_color,no_det_color,Line1_error_color,
                    Line2_error_color,Line3_error_color,Line4_error_color,mean_thres_error_color]
        
        with open("system_pickles/ocr_values.pkl","rb") as file:
            param_values = pickle.load(file)
           
        left_x=420 # reference bar graph of less than no. of lines
        right_x=912 #reference rectangular alert box
        upper_y=30
        rej_coord=480 #y coordinate of rejection coord 
        

        while True:
            y_first_center=80
            dir_file =os.getcwd()+'\Pickle'
            brand_values = pickle.load(open('Pickle\\'+os.listdir(dir_file)[0],'rb'))
            self.Set_parameter(exposureTime=brand_values['exposure_time'],gain=brand_values['camera_gain'])
            
            #self.Set_parameter(TriggerDelay= 40000.0)
            #ret = self.obj_cam.MV_CC_SetFloatValue("TriggerDelay", 22000)
            ret = self.obj_cam.MV_CC_SetFloatValue("TriggerDelay", int(brand_values['trigger_delay']))
            #ret = self.obj_cam.MV_CC_SetFloatValue("ExposureTime", 200)
            if 0 == ret:
                pass
            else:
                print("Error")
            
            ret = self.obj_cam.MV_CC_GetImageBuffer(stOutFrame, 10)
            if 0 == ret:
                if None == buf_cache:
                    buf_cache = (c_ubyte * stOutFrame.stFrameInfo.nFrameLen)()
                #获取到图像的时间开始节点获取到图像的时间开始节点
                self.st_frame_info = stOutFrame.stFrameInfo
                cdll.msvcrt.memcpy(byref(buf_cache), stOutFrame.pBufAddr, self.st_frame_info.nFrameLen)
                self.n_save_image_size = self.st_frame_info.nWidth * self.st_frame_info.nHeight * 3 + 2048
                if img_buff is None:
                    img_buff = (c_ubyte * self.n_save_image_size)()
                
                if True == self.b_save_jpg:
                    self.Save_jpg(buf_cache) #ch:保存Jpg图片 | en:Save Jpg
                if True == self.b_save_bmp:
                    self.Save_Bmp(buf_cache) #ch:保存Bmp图片 | en:Save Bmp
            else:
                continue

            #转换像素结构体赋值
            stConvertParam = MV_CC_PIXEL_CONVERT_PARAM()
            memset(byref(stConvertParam), 0, sizeof(stConvertParam))
            stConvertParam.nWidth = self.st_frame_info.nWidth
            stConvertParam.nHeight = self.st_frame_info.nHeight
            stConvertParam.pSrcData = cast(buf_cache, POINTER(c_ubyte))
            stConvertParam.nSrcDataLen = self.st_frame_info.nFrameLen
            stConvertParam.enSrcPixelType = self.st_frame_info.enPixelType 

            # RGB直接显示
            if PixelType_Gvsp_RGB8_Packed == self.st_frame_info.enPixelType:
                numArray = CameraOperation.Color_numpy(self,buf_cache,self.st_frame_info.nWidth,self.st_frame_info.nHeight)

            #如果是彩色且非RGB则转为RGB后显示
            else:
                nConvertSize = self.st_frame_info.nWidth * self.st_frame_info.nHeight * 3
                stConvertParam.enDstPixelType = PixelType_Gvsp_RGB8_Packed
                stConvertParam.pDstBuffer = (c_ubyte * nConvertSize)()
                stConvertParam.nDstBufferSize = nConvertSize
                ret = self.obj_cam.MV_CC_ConvertPixelType(stConvertParam)
                if ret != 0:
                    tkinter.messagebox.showerror('show error','convert pixel fail! ret = '+self.To_hex_str(ret))
                    continue
                cdll.msvcrt.memcpy(byref(img_buff), stConvertParam.pDstBuffer, nConvertSize)
                numArray = CameraOperation.Color_numpy(self,img_buff,self.st_frame_info.nWidth,self.st_frame_info.nHeight)
            #合并OpenCV到Tkinter界面中
            start = time.time() #program start time
            # print("numaarray",numArray)
            
            number_of_lines=brand_values['no_of_lines']
            # camera_h = self.st_frame_info.nHeight
            # camera_w = self.st_frame_info.nWidth
            # image_ratio=camera_w/camera_h
            canvas=[ltc[0],ltc[2],ltc[4],ltc[6],ltc[8],ltc[10],ltc[12],ltc[14],ltc[16],ltc[18]]
            oval=[ltc[1],ltc[3],ltc[5],ltc[7],ltc[9],ltc[11],ltc[13],ltc[15],ltc[17],ltc[19]]
            image_name= datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
            roi=brand_values['roi'].split(',')
            x11=int(roi[1].split(':')[0])
            x22=int(roi[1].split(':')[1])
            y11=int(roi[0].split(':')[0])
            y22=int(roi[0].split(':')[1])
            
            radio_value = brand_values['image_rotation']
            numArray = self.rotate_image(numArray, radio_value)
            # numArray = cv2.rotate(numArray, cv2.ROTATE_90_CLOCKWISE)
            # img = cv2.rotate(numArray, cv2.ROTATE_90_COUNTERCLOCKWISE)
            img = numArray.copy()
            original_image = numArray.copy()
            
            img = img[y11:y22, x11:x22]
            # img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)   
            h = 736 #height of image this is the minimum height of the image for paddleocr
            w = int(h*img.shape[1]/img.shape[0]) #
            img=cv2.resize(img,(w,h),interpolation = cv2.INTER_AREA)
            fimg=img.copy()  
            time1 = time.time()-start
            if len(os.listdir('brands/'+brand_values['brand_name']+'/detection/'))!=0:
                # img_save=img.copy()





                if param_values[0]==1:
                    result = CameraOperation.ocr.ocr(img, cls=False)#For detection with recognition
                    result_save=result
                    rec_result=[]
                    for v in range(0,len(result[0])):
                        rec_result.append(result[0][v][1][0]) #store recognition output
                    lines = []
                    for idx in range(len(result)):
                        # res = result[idx]
                        for line in result[idx]:
                            lines.append(line[0])
                    result = result[0]
                    boxes = [line[0] for line in result]
                    txts = [line[1][0] for line in result]
                    scores = [line[1][1] for line in result]
                    ########### For sorting lines ##################
                    
                    ######################################
                    for k in range(len(lines)):# to show detection boxes
                        for j in range(len(lines[k])):
                            if j < len(lines[k])-1:
                                p = j+1
                            else:
                                p =0
                            x1 = (int(float(lines[k][j][0])), int(float(lines[k][j][1])))
                            x2=(int(lines[k][p][0]), int(lines[k][p][1]))
                            cv2.line(img, x1,x2, (255, 0, 0), 2) #pink color
                        first_center = (50, y_first_center)
                        y_first_center += 60
                        cv2.putText(img, rec_result[k], first_center, cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv2.LINE_AA)
                    time2 = time.time()-start        
                else:
                    bothocr = time.time()
                    result = CameraOperation.ocr.ocr(img, cls=False,rec=False) # For detection only
                    result_save=result
                    lines = result[0] 
                    for k in range(len(lines)): # to show detection boxes 
                        for j in range(len(lines[k])):
                            if j < len(lines[k])-1:
                                p = j+1
                            else:
                                p =0
                            x1 = (int(float(lines[k][j][0])), int(float(lines[k][j][1])))     
                            cv2.line(img, x1,(int(lines[k][p][0]), int(lines[k][p][1])), (0,255,0), 2)
                # fimg=img.copy()               
                detection_time=time.time()-start
                
                def single_reject():
                    print("Rejection Triggered")
                    global NG_GOOD
                    NG_GOOD = 0
                    global time_taken_all, detection_time
                    if int(brand_values['reject_enable'])==1:
                        # if int(brand_values['line1_enable'])==1:
                            print("Purple Line Rejection")
                            # time_delay_rejection = float(brand_values[9])
                            ret = self.obj_cam.MV_CC_SetEnumValue("LineSelector", 2)
                            if ret != 0:
                                tkinter.messagebox.showerror('show error',
                                                                'Selector failed1! ret = '
                                                                +self.To_hex_str(ret))
                                
                            ret = self.obj_cam.MV_CC_SetEnumValue("LineMode",8)

                            if ret != 0:
                                tkinter.messagebox.showerror('Strobe OP error',
                                                                'Line Mode failed1!' )
                                
                            ret = self.obj_cam.MV_CC_SetCommandValue("LineTriggerSoftware")
                            if ret != 0:
                                tkinter.messagebox.showerror('show error',
                                                                'set linetriggersoftware fail! ret = '
                                                                +self.To_hex_str(ret))


                        # ret = self.obj_cam_operation.obj_cam.MV_CC_SetEnumValue("LineSelector", 2)

                        # if ret != 0:
                        #     tkinter.messagebox.showerror('show error',
                        #                                     'Selector failed1! ret' )
                        # ret = self.obj_cam_operation.obj_cam.MV_CC_SetEnumValue("LineMode",8)

                        # if ret != 0:
                        #     tkinter.messagebox.showerror('Strobe OP error',
                        #                                     'Line Mode failed1!' )
                if param_values[0]==1:
                    #CameraOperation.white_rectangle(root,right_x,upper_y) # to place white in alert   
                    recog_correct=[]
                    if not result_save[0]:  # to check if there is detection or not
                        recog_correct.append(0)
                        # CameraOperation.rejection_trend('ND')    
                    else:
                        if len(result_save[0])!=int(number_of_lines) : #check if output bounding box matches input number of lines
                                # CameraOperation.rejection_trend('LT')
                                recog_correct.append(0)
                    line_strings=[]
                    for j in range(1,int(number_of_lines)+1):
                            line_strings.append(brand_values['line'+ str(j)])
                    b_test=[]
                    for string in line_strings:
                        if '[' in string:
                            b_test.append(1)
                        else:
                            b_test.append(0)
                    all_string=str(line_strings).replace("[","").replace("]","").replace("'","").replace(",","").replace(" ","")
                    output_string=str(rec_result).replace("[","").replace("]","").replace("'","").replace(",","").replace(" ","")
                    if 1 in b_test:
                        if CameraOperation.length_similarity('MT',all_string,output_string)>=float(brand_values['min_per_thresh']):
                                recog_correct.append(1) 
                        else:
                            recog_correct.append(0)
                            if len(rec_result)!=0:
                                pass
                                # CameraOperation.rejection_trend('MT')   
                    elif '{' in all_string:
                        pass
                    
                    else:
                        if CameraOperation.levenshtein_similarity(all_string,output_string)>=float(brand_values['min_per_thresh']): 
                            recog_correct.append(1)
                            
                        else:
                            recog_correct.append(0)
                            if len(rec_result)!=0:
                                pass
                                # CameraOperation.rejection_trend('MT')
                          
                    for string in line_strings:
                        if '[' in string:
                            if CameraOperation.length_similarity('MT',all_string,output_string)>=float(brand_values['min_per_thresh']):
                                recog_correct.append(1)
                            
                            else:
                                recog_correct.append(0)
                                if len(rec_result)!=0:
                                    pass
                                    # CameraOperation.rejection_trend('MT')   
                        else:
                            pass   
                    
                    line_result={1:0,2:0,3:0,4:0}
                    if len(rec_result)>=int(number_of_lines):
                        for j in range(0,int(number_of_lines)):

                            if CameraOperation.RecogComparison(brand_values['line'+str(j+1)],rec_result[j])==True:
                                '''
                                compare user entered recognition and output recognition values to
                                chech line parameter threshold
                                '''
                                recog_correct.append(1)
                                line_result[j+1]=2
                            elif CameraOperation.RecogComparison(brand_values['line'+str(j+1)],rec_result[j])==None:
                                recog_correct.append(2)
                                if len(rec_result)!=0:
                                    line_result[j+1]=3

                            elif CameraOperation.RecogComparison(brand_values['line'+str(j+1)],rec_result[j])==NotImplemented:
                                recog_correct.append(3)
                                if len(rec_result)!=0:
                                    line_result[j+1]=2
                                    
                            else:
                                recog_correct.append(0)
                                if len(rec_result)!=0 :
                                    line_result[j+1]=1
            
                    else:
                        recog_correct.append(0)
                        
                    for u in range(1,5): # to update value in rejection trend
                        if line_result[u]==1:
                            pass
                            # CameraOperation.rejection_trend('L'+str(u))
                        elif line_result[u]==2:
                            pass
                    
                        elif line_result[u]==3:
                            pass
                            # CameraOperation.rejection_trend('L'+str(u))
                        else:
                            pass

                    if 3 in recog_correct:
                        CameraOperation.red_blinking(self,wr,img,w,h,scale)
                        CameraOperation.change_last_image(lngiD)
                        CameraOperation.reject_count+=1
                        self.data_reset = 0
                        CameraOperation.time_nd(cl,0,'0')
                        CameraOperation.start_time=time.time()
                        single_reject()
                            

                        
                    elif 2 in recog_correct:
                        CameraOperation.red_blinking(self,wr,img,w,h,scale)
                        CameraOperation.change_last_image(lngiD)
                        CameraOperation.reject_count=0
                        self.data_reset = self.data_reset + 1
                        CameraOperation.time_nd(cl,1,CameraOperation.start_time)
                        single_reject()
                    
                    else:
                        if 0 in recog_correct: # to apply blinking function
                            CameraOperation.red_blinking(self,wr,img,w,h,scale)
                            CameraOperation.change_last_image(lngiD) 
                            CameraOperation.reject_count+=1
                            self.data_reset = 0
                            CameraOperation.time_nd(cl,0,'0')
                            CameraOperation.start_time=time.time()
                            ###### Rejection Here ##########
                            single_reject()
                        else:
                            CameraOperation.green_rectangle(self,wr)
                            CameraOperation.reject_count=0
                            self.data_reset = self.data_reset + 1
                            CameraOperation.time_nd(cl,1,CameraOperation.start_time)

                    if int(brand_values['save_ng']) and CameraOperation.reject_count !=0:
                        # print("816")
                        os.makedirs(os.path.join(brand_values['img_dir'],'images'),exist_ok=True) 
                        file_path = brand_values['img_dir']+'/images/'+ str(image_name)+'_NG' + ".jpg"
                        cv2.imwrite(file_path,fimg)
                        CameraOperation.delete_img('images')
                        if len(result_save[0]) == 0:
                            pass
                        else: # Saves detection bounding box and recognition output's txt in directory
                            if int(brand_values['save_result']) == 1:
                                lines2 = []
                                for idx in range(len(result_save)):
                                    res2 = result_save[idx]
                                    for line in res2:
                                        lines2.append(line[0])
                                result2 = result_save[0]
                                rec_dir = 'recognition_result'
                                fin_dir = brand_values['img_dir']
                                if rec_dir in str(os.listdir(fin_dir)):
                                    pass
                                else:
                                    os.makedirs(os.path.join(fin_dir,rec_dir))  
                                fi = open(brand_values['img_dir']+'/recognition_result/{}.txt'.format(str(image_name)),'a')
                                for recog_values in result2:
                                    rec_coord = str((recog_values[0])).replace('[[','').replace('[','').replace(']]','').replace(']','').replace('.0','')
                                    rec_label2 = recog_values[1][0]
                                    final_result = str(rec_coord) + ', ' + str(rec_label2)
                                    fi.write(final_result)
                                    fi.write('\n')
                                fi.close()
                    else:
                        img_dir = 'images'
                        if int(brand_values['save_img']) == 1:
                                os.makedirs(os.path.join(brand_values['img_dir'],img_dir),exist_ok=True) 
                                file_path = brand_values['img_dir']+'/images/'+str(image_name)+ '_'+'Img' + ".jpg"
                                cv2.imwrite(file_path,fimg)
                                CameraOperation.delete_img('images')
                        elif int(brand_values['save_ng']) and CameraOperation.reject_count !=0:
                                print((853))
                                os.makedirs(os.path.join(brand_values['img_dir'],img_dir),exist_ok=True) 
                                file_path = brand_values['img_dir']+'/images/'+ str(image_name)+'_NG' + ".jpg"
                                cv2.imwrite(file_path,fimg)
                                CameraOperation.delete_img('images')

                                    
                        if len(result_save[0]) == 0:
                            pass
                        else: # Saves detection bounding box and recognition output's txt in directory
                            if int(brand_values['save_result']) == 1:
                                lines2 = []
                                for idx in range(len(result_save)):
                                    res2 = result_save[idx]
                                    for line in res2:
                                        lines2.append(line[0])
                                result2 = result_save[0]
                                rec_dir = 'recognition_result'
                                fin_dir = brand_values['img_dir']
                                if rec_dir in str(os.listdir(fin_dir)):
                                    pass
                                else:
                                    os.makedirs(os.path.join(fin_dir,rec_dir))  
                                fi = open(brand_values['img_dir']+'/recognition_result/{}.txt'.format(str(image_name)),'a')
                                for recog_values in result2:
                                    rec_coord = str((recog_values[0])).replace('[[','').replace('[','').replace(']]','').replace(']','').replace('.0','')
                                    rec_label2 = recog_values[1][0]
                                    final_result = str(rec_coord) + ', ' + str(rec_label2)
                                    fi.write(final_result)
                                    fi.write('\n')
                                fi.close()
                else:      
                    #CameraOperation.white_rectangle(root,right_x,upper_y)
                    result = result[0]
                    boxes = [line[0] for line in result]
                    if (len(boxes)==0): # to check if there is detection or not
                        CameraOperation.red_blinking(self,wr,img,w,h,scale)
                        CameraOperation.change_last_image(lngiD)
                        CameraOperation.reject_count+=1
                        self.data_reset = 0
                        CameraOperation.time_nd(cl,0,'0')
                        single_reject()
                    elif (len(boxes)!=int(number_of_lines) and len(boxes)!=0): #check if output bounding box matches input number of lines
                        CameraOperation.red_blinking(self,wr,img,w,h,scale)
                        CameraOperation.change_last_image(lngiD) 
                        CameraOperation.reject_count+=1
                        self.data_reset=0
                        CameraOperation.time_nd(cl,0,'0')
                        single_reject()    
                    else:
                        CameraOperation.green_rectangle(self,wr)  
                        CameraOperation.reject_count=0
                        self.data_reset = self.data_reset + 1
                        CameraOperation.time_nd(cl,1,CameraOperation.start_time)  

                    if int(brand_values['save_ng']) and CameraOperation.reject_count!=0:
                        os.makedirs(os.path.join(brand_values['img_dir'],'images'),exist_ok=True) 
                        file_path = brand_values['img_dir']+'/images/'+ str(image_name)+'_NG' + ".jpg"
                        cv2.imwrite(file_path,fimg)
                        CameraOperation.delete_img('images')
                     
                    else:
                        if int(brand_values['save_img']) == 1:
                                os.makedirs(os.path.join(brand_values['img_dir'],'images'),exist_ok=True) 
                                file_path = brand_values['img_dir']+'/images/'+str(image_name)+ '_'+'Img' + ".jpg"
                                cv2.imwrite(file_path,fimg)
                                if int(brand_values['crop'])==1:
                                    file_path = brand_values['img_dir']+'/images/'+ str(image_name) + ".jpg"
                                    img_crop=cv2.imread(file_path)
                                    img_crop=img_crop[y11:y22,x11:x22]
                                    cv2.imwrite(file_path,img_crop)   
                         
                s=0.7
                img_ratio=fimg.shape[1]/fimg.shape[0]
                if fimg.shape[1]>= fimg.shape[0]:
                    dim=(int(display_width*s),int((display_width/img_ratio*s)))
                else:
                    dim = (int(display_height*img_ratio*s),int(display_height*s))
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img_rgb2 = cv2.resize(img_rgb, dim, interpolation = cv2.INTER_AREA)
                im_pil = PIL.Image.fromarray(img_rgb2)

                imgtk = ImageTk.PhotoImage(image=im_pil, master=root) #Pass Image to Pillow for Tkinter GUI      
                panel.imgtk = imgtk       
                panel.config(image=imgtk) 
                root.obr = imgtk
                nRet = self.obj_cam.MV_CC_FreeImageBuffer(stOutFrame)
                
                if self.b_exit == True:
                    if img_buff is not None:
                        del img_buff
                    if buf_cache is not None:
                        del buf_cache
                    break
                cv2.imwrite("current_img/1.jpg",original_image)
                CameraOperation.G_NG_update(gng,self.data_good,self.data_not_good)
                CameraOperation.count_last_nd(gng,self.data_reset)
                CameraOperation.last_ten_color(canvas,oval,color)
                detection_time1=time.time()-start
                CameraOperation.detect_time(dt,detection_time1)
                if len(os.listdir('last_10_img/'))<10:
                    pass
                else:
                    len_l10=os.listdir('last_10_img/')
                    sorted_len_l10 = sorted(len_l10, key=lambda x: int(x.split('.')[0]))
                    os.remove('last_10_img/'+sorted_len_l10[0])
                cv2.imwrite('last_10_img/'+image_name+'.jpg',cv2.cvtColor(img_rgb2, cv2.COLOR_RGB2BGR))
            else:
                ##########New Brand Created############
                self.Save_jpg(buf_cache,image_name,brand_values['img_dir'])
                if int(brand_values['crop'])==1:
                    file_path = brand_values['img_dir']+'/images/'+ str(image_name) + ".jpg"
                    img_crop=cv2.imread(file_path)
                    img_crop=img_crop[y11:y22,x11:x22]
                    cv2.imwrite(file_path,img_crop)
                s=0.5
                img_ratio=fimg.shape[1]/fimg.shape[0]
                if fimg.shape[1]>= fimg.shape[0]:
                    dim=(int(display_width*s),int((display_width/img_ratio*s)))
                else:
                    dim = (int(display_height*img_ratio*s),int(display_height*s))
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img_rgb2 = cv2.resize(img_rgb, dim, interpolation = cv2.INTER_NEAREST)
                im_pil = Image.fromarray(img_rgb2)
                imgtk = ImageTk.PhotoImage(image=im_pil, master=root) #Pass Image to Pillow for Tkinter GUI        
                panel.imgtk = imgtk       
                panel.config(image=imgtk) 
                root.obr = imgtk
                nRet = self.obj_cam.MV_CC_FreeImageBuffer(stOutFrame)    
        
          
    def Save_jpg(self,buf_cache,image_name,fin_dir):
        if(None == buf_cache):
            return
        self.buf_save_image = None
        img_dir = 'images'
        
        if img_dir in str(os.listdir(fin_dir)):
            pass
        else:
            os.makedirs(os.path.join(fin_dir,img_dir))  
        file_path = fin_dir+'/images/'+ str(image_name) + ".jpg"
        self.n_save_image_size = self.st_frame_info.nWidth * self.st_frame_info.nHeight * 3 + 2048
        
        if self.buf_save_image is None:
            self.buf_save_image = (c_ubyte * self.n_save_image_size)()
            

        stParam = MV_SAVE_IMAGE_PARAM_EX()
        stParam.enImageType = MV_Image_Jpeg;                                        # ch:需要保存的图像类型 | en:Image format to save
        stParam.enPixelType = self.st_frame_info.enPixelType                               # ch:相机对应的像素格式 | en:Camera pixel type
        stParam.nWidth      = self.st_frame_info.nWidth                                    # ch:相机对应的宽 | en:Width
        stParam.nHeight     = self.st_frame_info.nHeight                                   # ch:相机对应的高 | en:Height
        stParam.nDataLen    = self.st_frame_info.nFrameLen
        stParam.pData       = cast(buf_cache, POINTER(c_ubyte))
        stParam.pImageBuffer=  cast(byref(self.buf_save_image), POINTER(c_ubyte)) 
        stParam.nBufferSize = self.n_save_image_size                                 # ch:存储节点的大小 | en:Buffer node size
        stParam.nJpgQuality = 80;                                                    # ch:jpg编码，仅在保存Jpg图像时有效。保存BMP时SDK内忽略该参数
        return_code = self.obj_cam.MV_CC_SaveImageEx2(stParam)            

        if return_code != 0:
            tkinter.messagebox.showerror('show error','save jpg fail! ret = '+self.To_hex_str(return_code))
            self.b_save_jpg = False
            return
        file_open = open(file_path.encode('ascii'), 'wb+')
        img_buff = (c_ubyte * stParam.nImageLen)()
       
        try:
            cdll.msvcrt.memcpy(byref(img_buff), stParam.pImageBuffer, stParam.nImageLen)
            file_open.write(img_buff)
            self.b_save_jpg = False
        except Exception as e :
            self.b_save_jpg = False
            raise Exception("get one frame failed:%s" % e.message)
        if None != img_buff:
            del img_buff
        if None != self.buf_save_image:
            del self.buf_save_image

    def Save_Bmp(self,buf_cache):
        if(0 == buf_cache):
            return
        self.buf_save_image = None
        file_path = str(self.st_frame_info.nFrameNum) + ".bmp"    
        self.n_save_image_size = self.st_frame_info.nWidth * self.st_frame_info.nHeight * 3 + 2048
        if self.buf_save_image is None:
            self.buf_save_image = (c_ubyte * self.n_save_image_size)()

        stParam = MV_SAVE_IMAGE_PARAM_EX()
        stParam.enImageType = MV_Image_Bmp;                                        # ch:需要保存的图像类型 | en:Image format to save
        stParam.enPixelType = self.st_frame_info.enPixelType                               # ch:相机对应的像素格式 | en:Camera pixel type
        stParam.nWidth      = self.st_frame_info.nWidth                                    # ch:相机对应的宽 | en:Width
        stParam.nHeight     = self.st_frame_info.nHeight                                   # ch:相机对应的高 | en:Height
        stParam.nDataLen    = self.st_frame_info.nFrameLen
        stParam.pData       = cast(buf_cache, POINTER(c_ubyte))
        stParam.pImageBuffer=  cast(byref(self.buf_save_image), POINTER(c_ubyte)) 
        stParam.nBufferSize = self.n_save_image_size                                 # ch:存储节点的大小 | en:Buffer node size
        return_code = self.obj_cam.MV_CC_SaveImageEx2(stParam)            
        if return_code != 0:
            tkinter.messagebox.showerror('show error','save bmp fail! ret = '+self.To_hex_str(return_code))
            self.b_save_bmp = False
            return
        file_open = open(file_path.encode('ascii'), 'wb+')
        img_buff = (c_ubyte * stParam.nImageLen)()
        try:
            cdll.msvcrt.memcpy(byref(img_buff), stParam.pImageBuffer, stParam.nImageLen)
            file_open.write(img_buff)
            self.b_save_bmp = False
            tkinter.messagebox.showinfo('show info','save bmp success!')
        except Exception as e :
            self.b_save_bmp = False
            raise Exception("get one frame failed:%s" % e.message)
        if None != img_buff:
            del img_buff
        if None != self.buf_save_image:
            del self.buf_save_image

    def Is_mono_data(self,enGvspPixelType):
        if PixelType_Gvsp_Mono8 == enGvspPixelType or PixelType_Gvsp_Mono10 == enGvspPixelType \
            or PixelType_Gvsp_Mono10_Packed == enGvspPixelType or PixelType_Gvsp_Mono12 == enGvspPixelType \
            or PixelType_Gvsp_Mono12_Packed == enGvspPixelType:
            return True
        else:
            return False

    def Is_color_data(self,enGvspPixelType):
        if PixelType_Gvsp_BayerGR8 == enGvspPixelType or PixelType_Gvsp_BayerRG8 == enGvspPixelType \
            or PixelType_Gvsp_BayerGB8 == enGvspPixelType or PixelType_Gvsp_BayerBG8 == enGvspPixelType \
            or PixelType_Gvsp_BayerGR10 == enGvspPixelType or PixelType_Gvsp_BayerRG10 == enGvspPixelType \
            or PixelType_Gvsp_BayerGB10 == enGvspPixelType or PixelType_Gvsp_BayerBG10 == enGvspPixelType \
            or PixelType_Gvsp_BayerGR12 == enGvspPixelType or PixelType_Gvsp_BayerRG12 == enGvspPixelType \
            or PixelType_Gvsp_BayerGB12 == enGvspPixelType or PixelType_Gvsp_BayerBG12 == enGvspPixelType \
            or PixelType_Gvsp_BayerGR10_Packed == enGvspPixelType or PixelType_Gvsp_BayerRG10_Packed == enGvspPixelType \
            or PixelType_Gvsp_BayerGB10_Packed == enGvspPixelType or PixelType_Gvsp_BayerBG10_Packed == enGvspPixelType \
            or PixelType_Gvsp_BayerGR12_Packed == enGvspPixelType or PixelType_Gvsp_BayerRG12_Packed== enGvspPixelType \
            or PixelType_Gvsp_BayerGB12_Packed == enGvspPixelType or PixelType_Gvsp_BayerBG12_Packed == enGvspPixelType \
            or PixelType_Gvsp_YUV422_Packed == enGvspPixelType or PixelType_Gvsp_YUV422_YUYV_Packed == enGvspPixelType:
            return True
        else:
            return False

    def Mono_numpy(self,data,nWidth,nHeight):
        data_ = np.frombuffer(data, count=int(nWidth * nHeight), dtype=np.uint8, offset=0)
        data_mono_arr = data_.reshape(nHeight, nWidth)
        numArray = np.zeros([nHeight, nWidth, 1],"uint8") 
        numArray[:, :, 0] = data_mono_arr
        return numArray

    def Color_numpy(self,data,nWidth,nHeight):
        data_ = np.frombuffer(data, count=int(nWidth*nHeight*3), dtype=np.uint8, offset=0)
        data_r = data_[0:nWidth*nHeight*3:3]
        data_g = data_[1:nWidth*nHeight*3:3]
        data_b = data_[2:nWidth*nHeight*3:3]

        data_r_arr = data_r.reshape(nHeight, nWidth)
        data_g_arr = data_g.reshape(nHeight, nWidth)
        data_b_arr = data_b.reshape(nHeight, nWidth)
        numArray = np.zeros([nHeight, nWidth, 3],"uint8")

        numArray[:, :, 0] = data_r_arr
        numArray[:, :, 1] = data_g_arr
        numArray[:, :, 2] = data_b_arr
        return numArray

######################### Developed By Crimson Tech Pvt. Ltd. #####################################
################# Diwash Poudel , Chhabi Lal Tamang , Samvandha Pathak ############################
