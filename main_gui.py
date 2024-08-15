
######################### Developed By Crimson Tech Pvt. Ltd. #####################################
################# Diwash Poudel , Chhabi Lal Tamang , Samvandha Pathak ############################

############ python libraries ####################
import sys
import os
from PIL import Image,ImageTk
import PIL.Image
import pickle
import glob
import subprocess
import shutil
import os

########### tkinter libraries ################
from tkinter import * 
from tkinter.messagebox import *
import tkinter.messagebox
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


######################################## MODEL REPLACEMENT WHILE OPENING APP ########################
####################### For Detection Model Replacement #################################

computer_name='Dell' #name of user in C drive
det_brand_path = 'C:/Users/'+computer_name+'/.paddleocr/whl/det/en/en_PP-OCRv3_det_infer/' #path of default paddleocr location where detection model is saved 
det_img_path = os.getcwd() + '\\Brands'  #path of trained model of detection
def det_model_locat(file_path: str)-> None:
    '''
    Function that copies the trained detection model from its location to paddleocr default location in drive C 
    '''
    file_details = os.listdir(file_path)
    for i in file_details:
        src_path = file_path + i
        dest_path = det_brand_path
        shutil.copy(src_path, dest_path)

######################### For Recognition Model Replacement ################################
rec_brand_path = 'C:/Users/'+computer_name+'/.paddleocr/whl/rec/en/en_PP-OCRv4_rec_infer/' # path of default paddelocr location where recognition model is saved
rec_img_path =os.getcwd() +  '\\Brands' #path of trained model of recognition 
def rotation_get(value):
    # print("function vitra",value)
    return value
def rec_model_locat(file_path: str)-> None:
    '''
    Function that copies the trained recognition model from its location to paddleocr default location in drive C 
    '''
    file_details = os.listdir(file_path)
    for i in file_details:
        src_path = file_path + i
        dest_path = rec_brand_path
        shutil.copy(src_path, dest_path)

global brand_select_val
brand_files = os.listdir(det_img_path)
shamp = ''
for ik in brand_files:
    pass

# det_model_locat(det_img_path +'\\' + ik + '\\Detection\\')
# rec_model_locat(rec_img_path + '\\' + ik + '\\Recognition\\')
# print("Model replaced")

###### camera and other libraries
from new_brand_pickle import new_brand_fun
from MvCameraControl_class import *
from CamOperation_class import *

############ For sending data into cloud #####################
# os.startfile("C:/Users/User/Desktop/OCR_train/send_to_cloud.bat")

###### Function to start automatically ################
def windows_start()-> None:
    '''
    This function automatically finds and opens the camera 
    '''
    print("Auto start")
    time.sleep(3)
    enum_devices()
    time.sleep(3)
    open_device()
    # time.sleep(3)
    # start_grabbing()

#获取选取设备信息的索引，通过[]之间的字符去解析
def TxtWrapBy(start_str, end, all):
    start = all.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = all.find(end, start)
        if end >= 0:
            return all[start:end].strip()

#将返回的错误码转换为十六进制显示
def ToHexStr(num):
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

if __name__ == "__main__":
    global deviceList 
    deviceList = MV_CC_DEVICE_INFO_LIST()
    global tlayerType
    tlayerType = MV_GIGE_DEVICE | MV_USB_DEVICE
    global cam
    cam = MvCamera()
    global nSelCamIndex
    nSelCamIndex = 0
    global obj_cam_operation
    obj_cam_operation = 0
    global b_is_run
    b_is_run = False

            #绑定下拉列表至设备信息索引
    def xFunc(event):
        global nSelCamIndex
        nSelCamIndex = TxtWrapBy("[","]",device_list.get())
    
    #ch:枚举相机 | en:enum devices
    def enum_devices():
        global deviceList
        global obj_cam_operation
        deviceList = MV_CC_DEVICE_INFO_LIST()
        tlayerType = MV_GIGE_DEVICE | MV_USB_DEVICE
        ret = MvCamera.MV_CC_EnumDevices(tlayerType, deviceList)
        if ret != 0:
            tkinter.messagebox.showerror('show error','enum devices fail! ret = '+ ToHexStr(ret))

        if deviceList.nDeviceNum == 0:
            tkinter.messagebox.showinfo('show info','find no device!')

        print ("Find %d devices!" % deviceList.nDeviceNum)

        devList = []
        for i in range(0, deviceList.nDeviceNum):
            mvcc_dev_info = cast(deviceList.pDeviceInfo[i], POINTER(MV_CC_DEVICE_INFO)).contents
            if mvcc_dev_info.nTLayerType == MV_GIGE_DEVICE:
                print ("\ngige device: [%d]" % i)
                chUserDefinedName = ""
                for per in mvcc_dev_info.SpecialInfo.stGigEInfo.chUserDefinedName:
                    if 0 == per:
                        break
                    chUserDefinedName = chUserDefinedName + chr(per)
                print ("device model name: %s" % chUserDefinedName)

                nip1 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0xff000000) >> 24)
                nip2 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x00ff0000) >> 16)
                nip3 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x0000ff00) >> 8)
                nip4 = (mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x000000ff)
                print ("current ip: %d.%d.%d.%d\n" % (nip1, nip2, nip3, nip4))
                devList.append("["+str(i)+"]GigE: "+ chUserDefinedName +"("+ str(nip1)+"."+str(nip2)+"."+str(nip3)+"."+str(nip4) +")")
            elif mvcc_dev_info.nTLayerType == MV_USB_DEVICE:
                print ("\nu3v device: [%d]" % i)
                chUserDefinedName = ""
                for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chUserDefinedName:
                    if per == 0:
                        break
                    chUserDefinedName = chUserDefinedName + chr(per)
                print ("device model name: %s" % chUserDefinedName)

                strSerialNumber = ""
                for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chSerialNumber:
                    if per == 0:
                        break
                    strSerialNumber = strSerialNumber + chr(per)
                print ("user serial number: %s" % strSerialNumber)
                devList.append("["+str(i)+"]USB: "+ chUserDefinedName +"(" + str(strSerialNumber) + ")")
        device_list["value"] = devList
        device_list.current(0)
    
        #ch:打开相机 | en:open device
    def open_device(operation_method=CameraOperation):
        global deviceList
        global nSelCamIndex
        global obj_cam_operation
        global b_is_run
        obj_cam_operation = operation_method(cam,deviceList,nSelCamIndex)
        ret = obj_cam_operation.Open_device()
        if  0!= ret:
            b_is_run = False
        else:
            model_val.set('triggermode')
            obj_cam_operation.Set_trigger_mode("triggermode")
            # obj_cam_operation.Set_trigger_mode("continuous")
            label_cam_status.config(text='Camera On', bg='#019065')
            b_is_run = True
            start_grabbing()
            btn_open_device = tk.Button(window, text='Open Camera', width=18, height=4,
                                command = camera_open, bg = '#80ced7', font = ('Inter',10,'bold'))
            btn_open_device.place(x=left_x+310, y=upper_y-25)
    
    # ch:开始取流 | en:Start grab image
    def start_grabbing():
        global obj_cam_operation
        obj_cam_operation.Start_grabbing(window,panel,ltc,wr,dt,gng,rtc,wtc,label_NGD,cl)

    # ch:停止取流 | en:Stop grab image
    def stop_grabbing():
        global obj_cam_operation
        obj_cam_operation.Stop_grabbing()    

    # ch:关闭设备 | Close device   
    def close_device():
        global b_is_run
        global obj_cam_operation
        obj_cam_operation.Close_device()
        b_is_run = False 
        #清除文本框的数值
        text_frame_rate.delete(1.0, tk.END)
        text_exposure_time.delete(1.0, tk.END)
        text_gain.delete(1.0, tk.END)
        label_cam_status.config(text='Camera Off', bg='#D9305C',fg='#ffffff')
        # label_cam_status = tk.Label(window, 
        #                             text='Camera Off'
        #                             ,width=15
        #                             ,bg = 'red'
        #                             ,height=4
        #                             ,font = ('Inter',10,'bold'))
        # label_cam_status.place(x=left_x+595, y=5)
        btn_open_device = tk.Button(window, text='Open Camera', width=18, height=4,
                                command = camera_open, bg = '#80ced7', font = ('Inter',10,'bold'))
        btn_open_device.place(x=left_x+310, y=upper_y-25)
        
        
    #ch:设置触发模式 | en:set trigger 
    def set_triggermode():
        global obj_cam_operation
        strMode = model_val.get()
        #strMode = "triggermode"
        obj_cam_operation.Set_trigger_mode(strMode)

    #ch:设置触发命令 | en:set trigger software
    def trigger_once():
        global triggercheck_val
        global obj_cam_operationload
        nCommand = triggercheck_val.get()
        obj_cam_operation.Trigger_once(nCommand)
    
    #ch:保存bmp图片 | en:save bmp image
    def bmp_save():
        global obj_cam_operation
        obj_cam_operation.b_save_bmp = True

    #ch:保存jpg图片 | en:save jpg image
    def jpg_save():
        global obj_cam_operation
        obj_cam_operation.b_save_jpg = True
   ###################### GUI Code Starts from here #######################
        #############################################################
            ####################################################
                ###########################################
                    ###################################detect_recog_\_btn
    window = tk.Tk()
    window.title('Batch Code Inspection System')
    window.geometry('1366x768')
    
    ############### Reference Coordinates for GUI ########################
    left_x=35 # left value of x ,reference find cameras
    left_x2=420
    right_x=1000 # reference detection result
    upper_y=30 # y of find cameras
    rej_coord=480 #y coordinate of rejection coord 

############### Variables for GUI ################
    model_val = tk.StringVar()
    label_val = tk.StringVar()
    sticker_val = tk.StringVar()
    crown_val = tk.StringVar()
    reject_radiobtn_variable = tk.StringVar()
    detect_recog_variable = tk.StringVar()
    brandsel_val = tk.StringVar()
    line2_reject_variable = StringVar()
    line1_reject_variable = StringVar()
    save_img_variable = StringVar()
    savedet_check_val = StringVar()
    save_result_variable = StringVar()
    save_ng_variable = StringVar()
    crop_img_variable=StringVar()
    brand_name_var = StringVar()
    global triggercheck_val
    triggercheck_val = tk.IntVar()
    page = Frame(window,height=400,width=60,relief=GROOVE,bd=5,borderwidth=4)
    page.pack(expand=True, fill=BOTH)
    panel = Label(page)
    panel.place(x=300, y=100,height=600,width=590)

################ Loading pickle values for OCR models i.e only detection and both detection and recognition ####################
    with open("system_pickles/ocr_values.pkl","rb") as file:
        param_values = pickle.load(file) 

############### Loading existing pickle values for all the parameters of GUI ###############################
    pkl_file = glob.glob('Pickle/*')  
    if len(pkl_file)==0:
        with open('system_pickles/initial_param.pkl','rb') as f:
            brand_values = pickle.load(f) 
    else:
        for p in pkl_file:
            with open(p,"rb") as file:
                brand_values = pickle.load(file)
    ############# Functions of GUI ##########################
    def choose_directory()-> None:
        '''Function that open directory from local computer
        '''
        global directory
        dir_display = filedialog.askdirectory()
        
        directory=dir_display
        choose_dir_variable.set(directory)
    def white_rectangle(root,right_x:int,upper_y:int)-> str:
        '''
        It places white rectangle that is change into red and green according to the result of the system
        '''
        rectangle_box = tk.Label(master=root, bg = 'white', width=18, height=4,relief='solid',justify='center')
        rectangle_box.grid(row=1,column=0,padx=7,columnspan=2)
        return rectangle_box
    
    def detection_time(root,right_x:int)-> float:
        '''
        This function displays the total time to detect one product.
        '''
        total_time = tk.Label(root, text = '0 sec',font = ('Inter',10,'bold'),bg = '#ffffff')
        total_time.grid(row=2,column=1,columnspan=2,sticky=tk.E,padx=3)
        return total_time

    
    def time_ND(root,upper_y:int,right_x:int)-> str:
        '''
        This function displays the last not good counter time.
        '''
        clock_label = tk.Label(root,text = '0',  anchor='center',font = ('Inter',10,'bold'),bg = 'white')
        clock_label.grid(row=3,column=1)
        return clock_label
        
    def G_NG_count(root,right_x:int,upper_y:int)-> str:
         '''
         This function displays the Good Not Counter.
         '''
         good = tk.Label(root, text = 0, anchor='center',font= ('Inter',10,'bold'),bg = 'white') #for good count
         good.grid(row=0,column=1)
         not_good = tk.Label(root, text = 0, anchor='center',font = ('Inter',10,'bold'),bg = 'white') #for not good count
         not_good.grid(row=1,column=1)
         count_nd = tk.Label(root, text = 0, anchor='center',font = ('Inter',10,'bold'),bg = 'white')
         count_nd.grid(row=2,column=1)
         return [good,not_good,count_nd]
    
    def white_rejection_trend(root,left_x:int,upper_y:int,rej_coord:int)->None:
        '''
        This function places white line in each rejection trend heading
        '''     
        pass

    def rejection_trend_count(root,left_x:int,upper_y:int,rej_coord:int)->None:
        '''
        This function places count in each rejection trend heading
        ''' 
        pass

    last10_win=None
    def last_ten_circle(nroot,right_x:int,upper_y:int)->None:
        '''
        This function places color of circles according to result. Red for critical error,
        yellow for minor error, green for no error
        '''
        def button_clicked(button_name):
            global last10_win
            if last10_win is not None:
                last10_win.destroy()

            len_l10=os.listdir('last_10_img/')
            sorted_len_l10 = sorted(len_l10, key=lambda x: int(x.split('.')[0]))
            img_10_raw='last_10_img/'+sorted_len_l10[10-int(button_name)]
            img10=PIL.Image.open(img_10_raw)
            last10_win = tk.Toplevel()
            last10_win.title(str(button_name)+' circle selected')
            last10_win.resizable(True, True)
            window_size=str(img10.size[0]+20)+"x"+str(img10.size[1]+20)
            last10_win.geometry(window_size) 
            photo = ImageTk.PhotoImage(img10.resize((img10.size[0],img10.size[1])))
            label10 = tk.Label(last10_win, image=photo)
            label10.place(x=10,y=10)
            last10_win.mainloop()
        
        ############## Creating last 10 ovals for last 10 images ###############################
        last_10_list = []
        for i in range(1,3):
            for j in range(0,5):
                canvas = tk.Canvas(nroot, bg='#ffffff', highlightbackground='#ffffff',width=20,height=20)
                canvas.grid(row=i,column=j,sticky=tk.W,padx=i+3,pady=j,columnspan=1)
                o = canvas.create_oval(5,5,18,18, fill='white')
                canvas.tag_bind(o,'<ButtonPress-1>', lambda event: button_clicked('{}'.format(i)))
                last_10_list.append(canvas)
                last_10_list.append(o)
        return last_10_list
    
    def silence_line(file_name: str, model_value: int) -> None:
        '''
        Function that silences the line entry box according to the number of lines entry box
        '''
        if int(model_value) == 1:
            if file_name == str(1):
                line1_entry.config(state = 'normal')
                line2_entry.config(state = 'disabled')
                line3_entry.config(state = 'disabled')
                line4_entry.config(state = 'disabled') 
                line5_entry.config(state = 'disabled') 

            if file_name == str(2):
                line1_entry.config(state = 'normal')
                line2_entry.config(state = 'normal')
                line3_entry.config(state = 'disabled')
                line4_entry.config(state = 'disabled')
                line5_entry.config(state = 'disabled')
            
            if file_name == str(3):
                line1_entry.config(state = 'normal')
                line2_entry.config(state = 'normal')
                line3_entry.config(state = 'normal')
                line4_entry.config(state = 'disabled')
                line5_entry.config(state = 'disabled') 
                
            if file_name == str(4):
                line1_entry.config(state = 'normal')
                line2_entry.config(state = 'normal')
                line3_entry.config(state = 'normal')
                line4_entry.config(state = 'normal')
                line5_entry.config(state = 'disabled') 

            if file_name == str(5):
                line1_entry.config(state = 'normal')
                line2_entry.config(state = 'normal')
                line3_entry.config(state = 'normal')
                line4_entry.config(state = 'normal')
                line5_entry.config(state = 'normal') 

        elif int(model_value) == 0:
            line1_entry.config(state = 'disabled')
            line2_entry.config(state = 'disabled')
            line3_entry.config(state = 'disabled')
            line4_entry.config(state = 'disabled')
            line5_entry.config(state = 'disabled') 
            
            

    def select_brand() -> None:
        '''
        Function that selects the brand name and copies all the trained models of OCR respectively
        '''
        pass
        global directory
        combo_label = brandsel_val.get()
        if combo_label == brandsel_val.get():
            brands_dir = 'Brands/{}'.format(brandsel_val.get()) + '/'
            brand_combo = pickle.load(open(brands_dir + '{}.pkl'.format(brandsel_val.get()),'rb'))
            src = os.path.join(os.getcwd(),brands_dir + '{}.pkl'.format(brandsel_val.get()))
            dest = os.path.join(os.getcwd(),'Pickle')
            dir_path = os.path.join(os.getcwd(),'Pickle/*')
            dir_file = glob.glob(dir_path)
            if len(dir_file) == 0:
                shutil.copy(src,dest)
            else:
                for f in dir_file:
                    os.remove(f)
                    shutil.copy(src, dest)
            brand_name_variable.set(brand_combo['brand_name'])
            no_of_line_variable.set(brand_combo['no_of_lines'])
            line1_variable.set(brand_combo['line1'])
            line2_variable.set(brand_combo['line2'])
            line3_variable.set(brand_combo['line3'])
            line4_variable.set(brand_combo['line4'])
            line5_variable.set(brand_combo['line5'])
            min_per_thresh_variable.set(brand_combo['min_per_thresh'])
            line_per_thresh_variable.set(brand_combo['line_per_thresh'])
            reject_count_variable.set(brand_combo['reject_count'])
            reject_radiobtn_variable.set(brand_combo['reject_enable'])
            line1_reject_variable.set(brand_combo['line1_enable'])
            line2_reject_variable.set(brand_combo['line2_enable'])
            exposure_time_variable.set(brand_combo['exposure_time'])
            trigger_delay_variable.set(brand_combo['trigger_delay'])
            camera_gain_variable.set(brand_combo['camera_gain'])
            roi_variable.set(brand_combo['roi'])
            save_img_variable.set(brand_combo['save_img'])
            save_ng_variable.set(brand_combo['save_ng'])
            save_result_variable.set(brand_combo['save_result'])
            crop_img_variable.set(brand_combo['crop'])
            choose_dir_variable.set(brand_combo['img_dir'])
            center_image_name.config(text = brandsel_val.get())
            silence_line(brand_combo[13], param_values[0]) ##### function call for silencing lines entry text
            # print("{{{{{{}}}}{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}",brand_combo['image_rotation'])
            image_rotation_variable.set(brand_combo['image_rotation'])

            
            global brand_select_val
            det_model_locat(det_img_path +'\\' + brand_combo[0] + '\\Detection\\')
            rec_model_locat(rec_img_path + '\\' + brand_combo[0] + '\\Recognition\\')
            center_image_name.config(text = brandsel_val.get())
            tkinter.messagebox.showinfo("Models Replaced ", "Program will restart")
            close_device()
            window.destroy()
            subprocess.Popen(['python', 'main_gui.py'])

    ######################### Function to save all the parameters ########################
        ###########################################################################
            ##################################################################

    def save_gui_values()-> None:
        '''
        Function that takes all the user inputs values from GUI and saved in pickle file
        '''
        global param_values
        global save_image_sel_val
        global save_ocr_sel_val
        global rej_enable_status
        global line1_enable_status
        global line2_enable_status
        global save_img_status
        global save_ng_status 
        global save_det_status
        global save_result_status
        global crop_save
        global brand_values
        global image_rotation_variable
        
        ################## Loading Login Pickle #####################
        with open('login.pkl','rb') as f:
            login_values = pickle.load(f) 
          
         ################### Password Frame ###############################
        login_frame = tk.Frame(window, highlightbackground='#D4CDCD',bg='#ffffff',highlightthickness=1,bd=1,relief='solid',height=200,width=300)
        login_frame.place(x = left_x + 280, y = upper_y+150)
        
        login_label = tk.Label(login_frame, text = 'Admin Page', font = ('Inter',12,'bold'),bg='#ffffff')
        login_label.place(x = 100,y = 10)

        username_label = tk.Label(login_frame, text = 'Username :', font = ('Inter',10),bg='#ffffff')
        username_label.place(x = 40, y= 60)

        username_entry = tk.Entry(login_frame, font = ('Inter',10),width=13,relief='solid',justify='center')
        username_entry.place(x = 130, y= 60)
        
        password_label = tk.Label(login_frame, text = 'Password :', font = ('Inter',10),bg='#ffffff')
        password_label.place(x = 40, y= 90)

        password_entry = tk.Entry(login_frame, font = ('Inter',10),width=13,relief='solid',justify='center',show='*')
        password_entry.place(x = 130, y= 90)
        
        def login_form():
        
            username = username_entry.get()
            password = password_entry.get()

            if username == '' and password == '':
                tkinter.messagebox.showerror("Error",'Please fill the data')
            elif username == login_values['username'] and password == login_values['password']:
                tkinter.messagebox.showinfo("Login","Parameter Save Successfully")
                pkl_dir = glob.glob('Pickle/*.pkl')
                for pkl in pkl_dir:
                    pass
                    
                with open(pkl, 'rb') as brand:
                    brand_values = pickle.load(brand)

                brand_param_dict = {'brand_name':BN_entry.get()
                            ,'no_of_lines':no_of_line_combo.get()
                            ,'line1':str(line1_entry.get()) 
                            ,'line2':str(line2_entry.get())
                            ,'line3':str(line3_entry.get())
                            ,'line4':str(line4_entry.get())
                            ,'line5':str(line5_entry.get())
                            ,'min_per_thresh':min_per_thresh_entry.get()
                            ,'line_per_thresh':line_per_thresh_entry.get()
                            ,'reject_count':reject_count_entry.get()
                            ,'reject_enable':rej_enable_status
                            ,'line1_enable':line1_enable_status
                            ,'line2_enable':line2_enable_status
                            ,'exposure_time':float(exposure_time_entry.get())
                            ,'trigger_delay':int(trigger_delay_entry.get())
                            ,'camera_gain':float(camera_gain_entry.get())
                            ,'roi':str(roi_entry.get())
                            ,'save_img':save_img_status
                            ,'save_ng':save_ng_status 
                            ,'save_result':save_result_status
                            ,'crop':crop_save
                            ,'img_dir':str(choose_dir_entry.get())
                            ,'image_rotation':int(image_rotation_variable.get())
                        }

                with open(pkl,'wb') as new_brand:
                    pickle.dump(brand_param_dict, new_brand) #writing pickle files for brand parameters
                srcs = pkl
                pik_lst = pkl.split('.')
                pik_str = str(pik_lst[0])
                pik_str = pik_str.split('\\')
                dests = os.getcwd() + '/Brands/' + pik_str[1]
                shutil.copy(srcs, dests)

                with open('system_pickles/ocr_values.pkl', 'rb') as file:
                    param_values = pickle.load(file) #loading pickle files for ocr models
                
                array1 = np.array([save_ocr_sel_val,save_image_sel_val])
                
                with open('system_pickles/ocr_values.pkl','wb') as f:
                    pickle.dump(array1, f)  
                
                with open('system_pickles/ocr_values.pkl', 'rb') as file:
                    param_values = pickle.load(file) #loading pickle files for ocr models
                    
                silence_line(no_of_line_combo.get(),param_values[0]) ##### Function call to silence the some specific lines according to no. of lines
                # tkinter.messagebox.showinfo("Login","Parameter Save Successfully")
                login_frame.place_forget()
            else:
                tkinter.messagebox.showerror("Login Failed","Please type correct Username and Password")

        submit_btn = tk.Button(login_frame, text="Login",bg='blue',font = ('Inter',10,'bold'),foreground='white',width=10, command=login_form)
        submit_btn.place(x = 45, y = 120)

        def close_login_form():
            login_frame.place_forget()
        close_btn = tk.Button(login_frame, text="Close",bg='red',font = ('Inter',10,'bold'),foreground='white',width=10, command=close_login_form)
        close_btn.place(x = 100, y = 150)

        def password_forgot():
            def password_verify():
                reset_frame.place_forget()
                companyname = company_name_entry.get()
                comanynumber = company_num_entry.get()

                if companyname == '' and comanynumber == '':
                    tkinter.messagebox.showerror("Error",'Please fill the data')
                
                elif companyname == 'crimsontech' and comanynumber == '9849506992':
                    def submit_new_login():
                        global username,password
                        new_username = new_username_entry.get()
                        new_password = new_password_entry.get()
                        new_login = { 'username':new_username,
                                        'password':new_password
                        }
                        with open('login.pkl','wb') as new_brand:
                            pickle.dump(new_login, new_brand) #writing new login data 

                        if new_username == '' and new_password == '':
                            tkinter.messagebox.showerror("Error",'Please fill the data')
                        else:
                            tkinter.messagebox.showinfo("Info","Username and Password set successfully")
                            new_password_frame.place_forget()
                            login_frame.place_forget()
                            
                    new_password_frame = tk.Frame(window, highlightbackground='#D4CDCD',bg='#ffffff',highlightthickness=1,bd=1,relief='solid',height=200,width=300)
                    new_password_frame.place(x = left_x + 280, y = upper_y+150)
                    login_label = tk.Label(new_password_frame, text = 'New Login Data', font = ('Inter',12,'bold'),bg='#ffffff')
                    login_label.place(x = 100,y = 10)
                    new_username_label = tk.Label(new_password_frame, text = ' New Username:', font = ('Inter',10),bg='#ffffff')
                    new_username_label.place(x = 27, y= 60)
                    new_username_entry = tk.Entry(new_password_frame, font = ('Inter',10),width=13,relief='solid',justify='center')
                    new_username_entry.place(x = 130, y= 60)
                    
                    new_password_label = tk.Label(new_password_frame, text = 'New Password:', font = ('Inter',10),bg='#ffffff')
                    new_password_label.place(x = 30, y= 90)

                    new_password_entry = tk.Entry(new_password_frame, font = ('Inter',10),width=13,relief='solid',justify='center')
                    new_password_entry.place(x = 130, y= 90)

                    submit_btn = tk.Button(new_password_frame, text="Submit",bg='blue',font = ('Inter',10,'bold'),foreground='white',width=10, command=submit_new_login)
                    submit_btn.place(x = 132, y = 120)

                    def close_new_login_form():
                        new_password_frame.place_forget()
                    close_btn = tk.Button(new_password_frame, text="Close",bg='red',font = ('Inter',10,'bold'),foreground='white',width=10, command=close_new_login_form)
                    close_btn.place(x = 132, y = 150)
                else:
                    tkinter.messagebox.showerror("Verification Failed","Please type correct data")
            reset_frame = tk.Frame(window, highlightbackground='#D4CDCD',bg='#ffffff',highlightthickness=1,bd=1,relief='solid',height=200,width=300)
            reset_frame.place(x = left_x + 280, y = upper_y+150)

            reset_label = tk.Label(reset_frame, text = 'Password Reset', font = ('Inter',12,'bold'),bg='#ffffff')
            reset_label.place(x = 100,y = 10)

            company_name = tk.Label(reset_frame, text = 'Company Name', font = ('Inter',10,'bold'),bg='#ffffff')
            company_name.place(x = 40, y= 60)

            company_name_entry = tk.Entry(reset_frame, font = ('Inter',10),width=13,relief='solid',justify='center')
            company_name_entry.place(x = 150, y= 60)

            company_num = tk.Label(reset_frame, text = 'Company Ph.No', font = ('Inter',10,'bold'),bg='#ffffff')
            company_num.place(x = 40, y= 90)

            company_num_entry = tk.Entry(reset_frame, font = ('Inter',10),width=13,relief='solid',justify='center')
            company_num_entry.place(x = 150, y= 90)

            verify_btn = tk.Button(reset_frame, text="Verify",bg='blue',font = ('Inter',10,'bold'),foreground='white',width=10, command=password_verify)
            verify_btn.place(x = 152, y = 120)

            def verification_form():
                reset_frame.place_forget()
            close_btn = tk.Button(reset_frame, text="Close",bg='red',font = ('Inter',10,'bold'),foreground='white',width=10, command=verification_form)
            close_btn.place(x = 152, y = 150)

        submit_btn = tk.Button(login_frame, text="Reset",bg='blue',font = ('Inter',10,'bold'),foreground='white',width=10, command=password_forgot)
        submit_btn.place(x = 135, y = 120)

    ########################### Function to Open Image and Select the ROI ################################  
    dragging = False
    roi = None
    def open_image()-> None:
        '''
        Function that opens the image to select the ROI to be used and display in the GUI
        '''
        file_path="current_img/1.jpg"
        started = 0
        if file_path:
            image = cv2.imread(file_path)
            r_image=cv2.resize(image,(int(0.25*image.shape[1]),int(0.25*image.shape[0])))
            ###### mouse click event########
            drawing = True
            ix,iy = -1,-1
            endy , endy = 0 ,0 
            def draw_rectangle(event, x, y, flags, param):
                try:
                    global ix,iy,drawing,roi, started, r_image,drawing
                    if event == cv2.EVENT_LBUTTONDOWN:
                        drawing = True
                        ix = x
                        iy = y
                        endx = x
                        endy = y
                    elif event == cv2.EVENT_MOUSEMOVE and drawing  == True:
                        endx = x
                        endy = y
                        r_image=cv2.resize(image,(int(0.25*image.shape[1]),int(0.25*image.shape[0])))
                        cv2.rectangle(r_image, (ix, iy),(endx, endy),(0, 255, 255),3)
                        cv2.imshow("ROI Selection", r_image)
                    elif event == cv2.EVENT_LBUTTONUP:
                        drawing = False
                        x1 = int(ix * image.shape[1] / r_image.shape[1])
                        y1 = int(iy * image.shape[0] / r_image.shape[0])
                        x2 = int((x) * image.shape[1] / r_image.shape[1])
                        y2 = int((y) * image.shape[0] / r_image.shape[0])
                        cv2.rectangle(r_image, (ix, iy),(x, y),(0, 255, 255),3)
                        cv2.imshow("ROI Selection", r_image)
                        cv2.waitKey(1500)
                        roi=str(int(y1))+':'+str(int(y2))+','+str(int(x1))+':'+str(int(x2))
                
                        cv2.destroyAllWindows()
                        started = 0
                except NameError as ne:
                    pass
            cv2.namedWindow("ROI Selection",cv2.WINDOW_AUTOSIZE)
            cv2.setMouseCallback("ROI Selection", draw_rectangle)
                # display the window
            while True:
                # print("hello",r_image)
                cv2.imshow("ROI Selection", r_image)
                cv2.waitKey(0) == ord('q')
                break
            cv2.destroyAllWindows()
            roi_entry.delete(0, tk.END)  # clear any existing text in the entry box
            roi_entry.insert(0, roi)
            cv2.destroyAllWindows()

    def reset_counter(root,right_x:int,upper_y:int) -> None: 
        '''
        This function changes value inside data.pickle to 0,0. It is used by Reset button to reset G and NG.
        '''
        with open("system_pickles/data_reset.pkl", "rb") as file:
                data_reset = pickle.load(file)
        obj_cam_operation.reset_counter_values() 
        data_reset={'G':0,'NG':0,'LNG':0}
        with open("system_pickles/data_reset.pkl", "wb") as file:
            pickle.dump(data_reset, file)
        gng[0].configure(text=data_reset['G'], font = ('Inter',10,'bold'))
        gng[1].configure(text=data_reset['NG'], font = ('Inter',10,'bold')) 
        gng[2].configure(text=data_reset['LNG'], font = ('Inter',10,'bold'))  
        
    ########################### Functions of all the radiobuttons ######################################
        ##########################################################################################
            #################################################################################
    def detect_image()-> None:
        '''
       Function that takes a 0 or 1 value from the detection radiobutton of the GUI and saves it in its variable
        '''
        global save_ocr_sel_val
        ocr_sel = str(detect_recog_variable.get())
        save_ocr_sel_val = int(ocr_sel)
       
    def sel_rej()-> None:
        '''
        Function that takes 0 or 1 value from Rejection Enable radiobutton of the GUI and saves it in its variable
        '''
        global rej_enable_status
        rej_enable_status = (str(reject_radiobtn_variable.get()))

    def line1_rej()-> None:
        '''
        Function that takes 0 or 1 value from Line1 Rejection Enable radiobutton of the GUI and saves it in its variable
        '''
        global line1_enable_status
        line1_enable_status = (str(line1_reject_variable.get()))

    def line2_rej()-> None:
        '''
        Function that takes 0 or 1 value from Line2 Rejection Enable radiobutton of the GUI and saves it in its variable
        '''
        global line2_enable_status
        line2_enable_status = (str(line2_reject_variable.get()))
    

    def save_img_btn()-> None:
        '''
        Function that takes 0/1 value from Save Image Radiobutton of the GUI and saves it in its variable
        '''
        global save_img_status
        save_img_status = int(str(save_img_variable.get()))

    def save_imgnd()-> None:
        '''
        Function that takes 0/1 value from Save Image Radiobutton of the GUI and saves it in its variable
        '''
        global save_ng_status
        save_ng_status = int(str(save_ng_variable.get()))

    def savedet_img()-> None:
        '''
        Function that takes 0/1 value from Save Detection Radiobutton of the GUI and saves it in its variable
        '''
        global save_det_status
        save_det_status = int(str(savedet_check_val.get()))

    def saverec_img()-> None:
        '''
        Function that takes 0/1 value from Save Recognition Radiobutton of the GUI and saves it in its variable
        '''
        global save_result_status
        save_result_status = int(str(save_result_variable.get()))
    
    def save_crop_img()-> None:
        '''
        Function that takes 0/1 value from crop Radiobutton of the GUI and saves it in its variable
        '''
        global crop_save
        crop_save= int(str(crop_img_variable.get()))
        
    def camera_open()-> None:
        open_device(CameraOperation)  #Calling the function that open the camera and load both detect and recognize models

    ######################### Frames for all the parameters of GUI ########################################
        ##############################################################################################
            ###################################################################################
                ##########################################################################
        
    ################################# Frame for System Settings #############################
    system_param_frame = tk.Frame(window, highlightbackground='#D4CDCD',bg='#ffffff',highlightthickness=1,bd=1,relief='solid') #border for detection result
    system_param_frame.place(x=left_x,y=upper_y+65)

    ################################# Frame for Rejection Settings ##########################
    reject_param_frame = tk.Frame(window, highlightbackground='#D4CDCD',bg='#ffffff',highlightthickness=1,bd=1,relief='solid') #border for detection result
    reject_param_frame.place(x=left_x,y=upper_y+340)

    ################################# Frame for Camera Settings ##############################
    camera_param_frame = tk.Frame(window, highlightbackground='#D4CDCD',bg='#ffffff', relief='solid',bd=1) #border for detection result
    camera_param_frame.place(x = left_x+1, y = upper_y+490)

    ################################# Frame for Camera Settings Button and Save Data Settings ########
    camera_save_frame = tk.Frame(camera_param_frame, highlightbackground='#D4CDCD',bg='#ffffff') #border for detection result
    camera_save_frame.grid(row=0,column=0,columnspan=2)

    ################################# Frame for Detection Result ############################
    detection_result_frame = tk.Frame(window, highlightbackground='#D4CDCD',bg='#ffffff',highlightthickness=1,bd=1,relief='solid')
    detection_result_frame.place(x = right_x, y = upper_y+65)

    ################################ Frame for Last 10 results ##############################
    last_10_frame = tk.Frame(window, highlightbackground='#D4CDCD',bg='#ffffff',highlightthickness=1,bd=1,relief='solid')
    last_10_frame.place(x = right_x, y = upper_y+195)

    ################################### Frame for Detection analysis ###########################
    detection_analysis_frame = tk.Frame(window, highlightbackground='#D4CDCD',bg='#ffffff',highlightthickness=1,bd=1,relief='solid')
    detection_analysis_frame.place(x = right_x, y = upper_y+300)

    gng=G_NG_count(detection_analysis_frame,right_x,upper_y)
    rtc=rejection_trend_count(window,left_x2,upper_y,rej_coord)
    wtc=white_rejection_trend(window,left_x2,upper_y,rej_coord)
    cl=time_ND(detection_analysis_frame,upper_y,right_x)
    ltc=last_ten_circle(last_10_frame,right_x,upper_y)
    wr=white_rectangle(detection_result_frame,right_x,upper_y)
    dt=detection_time(detection_result_frame,right_x)

    ####################################### Reading and Displaying the Last Not Good Image #################
    if len(os.listdir('PNGI/'))!=0:
        try:
            img_cv_Ng = cv2.imread("PNGI/PNGID.jpg")
            img_cv_Ng_w, img_cv_NG_h = img_cv_Ng.shape[1], img_cv_Ng.shape[0]
            ratio_NG = img_cv_Ng_w/img_cv_NG_h
            NG_width = 300
            NG_height = 200
            width1 = NG_width
            height1 = NG_height
            if img_cv_Ng_w>= img_cv_NG_h:
                width1 = NG_width
                height1 = NG_width/ratio_NG
            img_NGD = ImageTk.PhotoImage(PIL.Image.open("PNGI/PNGID.jpg").resize((int(width1),int(height1))))
            label_NGD = Label(window, image = img_NGD)
            label_NGD.place(x= right_x, y = upper_y+450)
        except Exception as e:
            label_NGD=Label(window,text='No Image')
            label_NGD.place(x= right_x-40, y = upper_y+460)
            pass
    else:
        label_NGD=Label(window,text='No Image')
        label_NGD.place(x= right_x-40, y = upper_y+460)

    data={'G':0,'NG':0,'LNG':0} #pickle value that save good and not good value 
    with open("system_pickles/data_reset.pkl", "wb") as file:
        pickle.dump(data, file) 
    
    RT={'LT':0,'ND':0,'L1':0,'L2':0,'L3':0,'L4':0,'MT':0} #pickle values for relative trand chart
    with open("system_pickles/RT.pkl", "wb") as file:
        pickle.dump(RT, file)

    RTD={'LT':0,'ND':0} #pickle values for good or not good label
    with open("system_pickles/RTD.pkl", "wb") as file:
        pickle.dump(RTD, file)

    xVariable = tkinter.StringVar()
    device_list = ttk.Combobox(window, textvariable=xVariable,width=35, font = ('Inter',10 , 'bold'),)
    device_list.place(x=left_x,y=upper_y-25)
    device_list.bind("<<ComboboxSelected>>", xFunc)

    label_exposure_time = tk.Label(window, text='Exposure Time',width=15)
    text_exposure_time = tk.Text(window,width=15)

    label_gain = tk.Label(window, text='Gain', width=15)
    text_gain = tk.Text(window,width=15)

    label_frame_rate = tk.Label(window, text='Frame Rate', width=15)
    text_frame_rate  = tk.Text(window,width=15)
    btn_enum_devices = tk.Button(window, text='Find Cameras', width=32,bg='white', command = enum_devices, font = ('Inter',10,'bold'),fg = '#263B90')
    btn_enum_devices.place(x=left_x, y=upper_y+10)
    btn_open_device = tk.Button(window, text='Open Camera', width=18, height=4,
                                command = camera_open, bg = '#80ced7', font = ('Inter',10,'bold'))
    btn_open_device.place(x=left_x+310, y=upper_y-25)
    btn_close_device = tk.Button(window, text='Close Camera', bg = '#D9305C',fg='#ffffff',
                                 width=18, height=4, command = close_device, font = ('Inter',10,'bold'))
    btn_close_device.place(x=left_x+510, y=upper_y-25)
    y_design = 180

    ############### Camera Status ##############################
    label_cam_status = tk.Label(window, text='Camera Status', width=18, font = ('Inter',10,'bold'),bg='#ffd670')
    label_cam_status.place(x=left_x+710, y=upper_y-25,relheight=0.0985)
    
    btn_start_grabbing = tk.Button(window, text='Start Grabbing', width=15,
                                   command = start_grabbing )
    btn_stop_grabbing = tk.Button(window, text='Stop Grabbing', width=15, command = stop_grabbing)

    ##################### Displaying the Company the logo #########################
    img=PIL.Image.open("main logo.png")
    img_logo = ImageTk.PhotoImage(PIL.Image.open("main logo.png").resize((int(img.size[0]*0.35),int(img.size[1]*0.35))))
    label_logo = Label(window, image = img_logo)
    label_logo.place(x= right_x, y = upper_y-20)

    ################## Parameters of System Settings start here #################################detect_recog_radio_btn
        ####################################################################################
            ##########################################################################

    system_param_label = tk.Label(system_param_frame, text = 'System Settings', height = 1,justify='center', font = ('Inter',10,'bold'),bg='#ffffff')
    system_param_label.grid(row=0,column=0,sticky=tk.W,columnspan=2)

    ######## Detection ##########################
    ocr_value = int(param_values[0])
    global save_ocr_sel_val
    save_ocr_sel_val = ocr_value
    if ocr_value == 0:
        ocr_status = 0
    else:
        ocr_status = 1
    ############################## Detection Only ################################
    detection_radio_btn = tk.Radiobutton(system_param_frame, value=0, text = 'Detection Only',command = detect_image, height= 1, fg = 'black', font = ('Inter', 10),variable = detect_recog_variable,bg='#ffffff')
    detection_radio_btn.grid(row=1,column=0,sticky=tk.W,columnspan=2)

    ############################## Detection and Recogniton ######################
    detect_recog_radio_btn = tk.Radiobutton(system_param_frame, value = 1, text = 'Detection & Recognition', command = detect_image, height= 1, fg = 'black', font = ('Inter',10),variable = detect_recog_variable,bg='#ffffff')
    detect_recog_radio_btn.grid(row=2,column=0,sticky=tk.W,columnspan=2)
    detect_recog_variable.set(ocr_status)

    ############################### Entry button for number of lines ############
    no_of_line_label = tk.Label(system_param_frame, text = 'No. of Lines:', font = ('Inter',10),bg='#ffffff')
    no_of_line_label.grid(row=3,column=0,sticky=tk.W)
    no_of_line_variable = tk.StringVar(system_param_frame, value = int(brand_values['no_of_lines']))
    no_of_line_combo = ttk.Combobox(system_param_frame, width = 20, textvariable = no_of_line_variable, justify='center', font= ('Inter',10))
    no_of_line_combo['values'] = [1,2,3,4,5]
    lines_chosen = no_of_line_variable.get()
    no_of_line_combo.grid(row=3,column=1,sticky=tk.E, padx=3)
    no_of_line_combo.current()

    ############################### First Line ###################################
    line1_label = tk.Label(system_param_frame, text = 'Line 1', font = ('Inter',10),bg='#ffffff')
    line1_label.grid(row=4,column=0,sticky=tk.W)
    line1_variable = tk.StringVar(system_param_frame, value = str(brand_values['line1']))
    line1_entry = tk.Entry(system_param_frame, font = ('Inter',10),relief='solid',width=23,justify='center',textvariable=line1_variable)
    line1_entry.grid(row=4,column=1,sticky=tk.E,padx=3)

    ########################### Second Line ######################################
    line2_label = tk.Label(system_param_frame, text = 'Line 2', font = ('Inter',10),bg='#ffffff')
    line2_label.grid(row=5,column=0,sticky=tk.W)
    line2_variable = tk.StringVar(system_param_frame, value = str(brand_values['line2']))
    line2_entry = tk.Entry(system_param_frame, font = ('Inter',10),relief='solid',width=23,justify='center',textvariable= line2_variable)
    line2_entry.grid(row=5,column=1,sticky=tk.E,padx=3)

    ########################### Third Line ########################################
    line3_label = tk.Label(system_param_frame, text = 'Line 3', font = ('Inter',10),bg='#ffffff')
    line3_label.grid(row=6,column=0,sticky=tk.W)
    line3_variable = tk.StringVar(system_param_frame, value = str(brand_values['line3']))
    line3_entry = tk.Entry(system_param_frame, font = ('Inter',10),relief='solid',width=23,justify='center',textvariable= line3_variable)
    line3_entry.grid(row=6,column=1,sticky=tk.E,padx=3)

    ########################### Fourth Line ########################################
    line4_label = tk.Label(system_param_frame, text = 'Line 4', font = ('Inter',10),bg='#ffffff')
    line4_label.grid(row=7,column=0,sticky=tk.W)
    line4_variable = tk.StringVar(system_param_frame, value = str(brand_values['line4']))
    line4_entry = tk.Entry(system_param_frame, font = ('Inter',10),relief='solid',width=23,justify='center',textvariable = line4_variable)
    line4_entry.grid(row=7,column=1,sticky=tk.E,padx=3)

        ########################### Fourth Line ########################################
    line5_label = tk.Label(system_param_frame, text = 'Line 5', font = ('Inter',10),bg='#ffffff')
    line5_label.grid(row=8,column=0,sticky=tk.W)
    line5_variable = tk.StringVar(system_param_frame, value = str(brand_values['line5']))
    line5_entry = tk.Entry(system_param_frame, font = ('Inter',10),relief='solid',width=23,justify='center',textvariable = line5_variable)
    line5_entry.grid(row=8,column=1,sticky=tk.E,padx=3)    ########################### Fourth Line ########################################
    

    ############################ Update Button For System Srettings ##################
    system_update_btn = tk.Button(system_param_frame, text='Update', fg='white',width=30,font=('Inter',10,'bold'), bg='#019065',command = save_gui_values, relief='flat')
    system_update_btn.grid(row=9,column=0,sticky=tk.W,columnspan=2)

    ############################# Brand Name  #######################################
    brand_name_variable =  tk.StringVar(window, value = str(brand_values['brand_name']))
    BN_entry = tk.Entry(window, font = ('Inter',10,'bold'), width = 10, textvariable = brand_name_variable)

    #################################### Parameters of Rejection Settings ###################################################
        ##############################################################################################################
            ###################################################################################################
    
    reject_param_label = tk.Label(reject_param_frame, text = 'Rejection Settings', height = 1,justify='center', font = ('Inter',10,'bold'),bg='#ffffff')
    reject_param_label.grid(row=0,column=0,sticky=tk.W,columnspan=7)

    ############################## Min Percent Thresh ################################
    min_per_thresh_label = tk.Label(reject_param_frame, text = 'Min % Thresh', font = ('Inter',10),bg='#ffffff')
    min_per_thresh_label.grid(row=1,column=0,sticky=tk.W,columnspan=3)
    min_per_thresh_variable = tk.StringVar(reject_param_frame, value = str(brand_values['min_per_thresh']))
    min_per_thresh_entry = tk.Entry(reject_param_frame, font = ('Inter',9),width=8, textvariable= min_per_thresh_variable,relief='solid',justify='center')
    min_per_thresh_entry.grid(row=1,column=6,sticky=tk.E,padx=3)
    
    ############################## Line Percent Thresh ###############################
    line_per_thresh_label = tk.Label(reject_param_frame, text = 'Line % Thresh', font = ('Inter',10),bg='#ffffff')
    line_per_thresh_label.grid(row=2,column=0,sticky=tk.W,columnspan=3)
    line_per_thresh_variable = tk.StringVar(reject_param_frame, value=str(brand_values['line_per_thresh']))
    line_per_thresh_entry = tk.Entry(reject_param_frame, font = ('Inter',10),width=8, textvariable=line_per_thresh_variable,relief='solid',justify='center')
    line_per_thresh_entry.grid(row=2,column=6,sticky=tk.E,padx=3)
    ############################## Reject Count ######################################
    reject_count_label = tk.Label(reject_param_frame, text = 'Reject Count', font = ('Inter',10),bg='#ffffff')
    # reject_count_label.grid(row=3,column=0,sticky=tk.W,columnspan=3)
    reject_count_variable = tk.StringVar(reject_param_frame, value=int(brand_values['reject_count']))
    reject_count_entry = tk.Entry(reject_param_frame, font = ('Inter',10),width=8, textvariable=reject_count_variable,relief='solid',justify='center')
    # reject_count_entry.grid(row=3,column=6,sticky=tk.E,padx=3)
    
    ############################# Rejection Enable ####################################
    reject_enable_label = tk.Label(reject_param_frame, text = 'Rejection Enable', font = ('Inter',10),bg='#ffffff')
    reject_enable_label.grid(row=3,column=0,sticky=tk.W,columnspan=3)
    reject_enable_value = int(brand_values['reject_enable'])
    global rej_enable_status
    rej_enable_status = reject_enable_value
    if reject_enable_value == 0:
        rejection_status = 0
    else:
        rejection_status = 1
    reject_on_radiobtn = tk.Radiobutton(reject_param_frame, text='Yes',variable=reject_radiobtn_variable, command = sel_rej,
                                      value=1, width=4, fg = 'green', font = ('Inter',10),bg='#ffffff')
    reject_on_radiobtn.grid(row=3,column=5)
    reject_off_radiobtn = tk.Radiobutton(reject_param_frame, text='No',variable=reject_radiobtn_variable, command = sel_rej,
                                      value=0, width=4, fg = 'red', font = ('Inter',10),bg='#ffffff')
    reject_off_radiobtn.grid(row=3,column=6)
    reject_radiobtn_variable.set(rejection_status)
    
    ################################## Line 1 Rejection Enable ##############################
    line1_reject_label = tk.Label(reject_param_frame, text = 'Line 1 Enable', font = ('Inter',10),bg='#ffffff')
    # line1_reject_label.grid(row=5,column=0,sticky=tk.W)
    line1_reject_value = int(brand_values['line1_enable'])
    global line1_enable_status
    line1_enable_status = line1_reject_value
    if line1_reject_value == 0:
        line1_reject_status = 0
    else:
        line1_reject_status = 1
    
    line1_reject_on = tk.Radiobutton(reject_param_frame, text='Yes',variable=line1_reject_variable, command = line1_rej,
                                      value=1, width=4, fg = 'green', font = ('Inter',10),bg='#ffffff')
    # line1_reject_on.grid(row=5,column=1,sticky=tk.E)
    line1_reject_off = tk.Radiobutton(reject_param_frame, text='No',variable=line1_reject_variable, command = line1_rej,
                                      value=0, width=4, fg = 'red', font = ('Inter',10),bg='#ffffff')
    # line1_reject_off.grid(row=5,column=2,sticky=tk.E)
    line1_reject_variable.set(line1_reject_status)
    
    ################################### Line 2 Rejection Enable ###############################
    line2_reject_label = tk.Label(reject_param_frame, text = 'Line 2 Enable', font = ('Inter',10),bg='#ffffff')
    # line2_reject_label.grid(row=6,column=0,sticky=tk.W)
    line2_reject_value = int(brand_values['line2_enable'])
    global line2_enable_status
    line2_enable_status = line2_reject_value
    if line2_reject_value == 0:
        line2_reject_status = 0
    else:
        line2_reject_status = 1
    line2_reject_on = tk.Radiobutton(reject_param_frame, text='Yes',variable=line2_reject_variable, command = line2_rej,
                                      value=1, width=4, fg = 'green', font = ('Inter',10),bg='#ffffff')
    # line2_reject_on.grid(row=6,column=1,sticky=tk.E)
    line2_reject_off = tk.Radiobutton(reject_param_frame, text='No',variable=line2_reject_variable, command = line2_rej,
                                      value=0, width=4, fg = 'red', font = ('Inter',10),bg='#ffffff')
    # line2_reject_off.grid(row=6,column=2,sticky=tk.E)
    line2_reject_variable.set(line2_reject_status)
    
    ################################### Update Button For Rejection Settings ######################
    reject_update_btn = tk.Button(reject_param_frame, text='Update', fg='white',command=save_gui_values,width=30,font=('Inter',10,'bold'), bg='#019065', relief='flat')
    reject_update_btn.grid(row=5,column=0,sticky=tk.W,columnspan=7)

    ############################################ Parameters for Camera Settings ######################################################
        ########################################################################################################################
            ###############################################################################################################
    
    ####################################### Logos for Camera ##########################################
    camera_logo = PIL.Image.open('./gui_images/camera_icon.png')
    save_logo = PIL.Image.open('./gui_images/save_icon.png')
    camera_icon = ImageTk.PhotoImage(camera_logo)
    save_data_icon = ImageTk.PhotoImage(save_logo)

    def camera_param_display():
        save_img_checkbox.grid_forget()
        crop_checkbox.grid_forget()
        save_ng_checkbox.grid_forget()
        choose_dir_label.grid_forget()
        choose_dir_entry.grid_forget()
        save_result_checkbox.grid_forget()
        exposure_time_label.grid(row=1,column=0, sticky=tk.W)
        exposure_time_entry.grid(row=1,column=1, sticky=tk.E, padx=2)
        # trigger_delay_label.grid(row=2,column=0,sticky=tk.W)
        # trigger_delay_entry.grid(row=2,column=1, sticky=tk.E, padx=2)
        camera_gain_label.grid(row=3,column=0,sticky=tk.W)
        camera_gain_entry.grid(row=3,column=1, sticky=tk.E, padx=2)
        roi_label.grid(row=4,column=0,sticky=tk.W,columnspan=2)
        roi_entry.grid(row=4,column=0,padx=7)
        open_image_btn.grid(row=4,column=1,sticky=tk.E,padx=2)
        camera_param_btn.config(state=DISABLED)
        data_save_label.config(state=ACTIVE)

            # Display Image Rotation section with radio buttons
        image_rotation_label.grid(row=5, column=0, sticky=tk.W)

        image_rotation_0.grid(row=6, column=0, sticky=tk.W, padx=1)
        image_rotation_90.grid(row=6, column=1, sticky=tk.W, padx=1)
        image_rotation_neg90.grid(row=7, column=0, sticky=tk.W, padx=1)
        image_rotation_180.grid(row=7, column=1, sticky=tk.W, padx=1)

    camera_param_btn = tk.Button(camera_save_frame,image=camera_icon,text = 'Camera Settings',font = ('Inter',10,'bold'),width=120,bg='#ffffff', command=camera_param_display,state=DISABLED,compound=LEFT)
    camera_param_btn.grid(row=0,column=0,sticky=tk.W)


    ########################################### Exposure Time ###############################################
    exposure_time_label = tk.Label(camera_param_frame, text = 'Brightness', font = ('Inter',10),bg='#ffffff')
    exposure_time_label.grid(row=1,column=0, sticky=tk.W)
    exposure_time_variable = tk.StringVar(camera_param_frame, value=str(brand_values['exposure_time']))
    exposure_time_entry = tk.Entry(camera_param_frame, font = ('Inter',10),width=8, textvariable= exposure_time_variable,relief='solid',justify='center')
    exposure_time_entry.grid(row=1,column=1, sticky=tk.E, padx=2)

    ########################################## Trigger Delay ################################################
    trigger_delay_label = tk.Label(camera_param_frame, text = 'Trigger Delay', font = ('Inter',10),bg='#ffffff')
    # trigger_delay_label.grid(row=2,column=0,sticky=tk.W)
    trigger_delay_variable = tk.StringVar(camera_param_frame, value = str(brand_values['trigger_delay']))
    trigger_delay_entry = tk.Entry(camera_param_frame, font = ('Inter',10),width=8, textvariable= trigger_delay_variable,relief='solid',justify='center')
    # trigger_delay_entry.grid(row=2,column=1, sticky=tk.E, padx=2)

    ########################################### Camera Gain #################################################
    camera_gain_label = tk.Label(camera_param_frame, text = 'Camera Gain', font = ('Inter',10),bg='#ffffff')
    camera_gain_label.grid(row=2,column=0,sticky=tk.W)
    camera_gain_variable = tk.StringVar(camera_param_frame, value = str(brand_values['camera_gain']))
    camera_gain_entry = tk.Entry(camera_param_frame, font = ('Inter',10),width=8, textvariable= camera_gain_variable,relief='solid',justify='center')
    camera_gain_entry.grid(row=2,column=1, sticky=tk.E, padx=2)



    ############################################ image ROI ##################################################
    roi_label = Label(camera_param_frame , text = "ROI" , font = ('Inter', 10),bg='#ffffff')
    roi_label.grid(row=3,column=0,sticky=tk.W,columnspan=2)
    roi_variable = tk.StringVar(camera_param_frame, value=str(brand_values['roi']))
    roi_entry = tk.Entry(camera_param_frame, font = ('Inter',8),relief='solid',width=14, textvariable=roi_variable)
    roi_entry.grid(row=3,column=0,padx=7)


    ########################################### Button for Open Image #######################################
    open_image_btn = tk.Button(camera_param_frame, text="Open Image",bg='#E8C6FD',fg ='black',font = ('Inter',8),command=open_image)
    open_image_btn.grid(row=3,column=1,sticky=tk.E,padx=2)


    # def on_rotation_change(*args):
    #     print(f"Selected Rotation Value: {image_rotation_variable.get()}")
        # rotation_get(image_rotation_variable.get())


    # Image Rotation Label
    image_rotation_label = tk.Label(camera_param_frame, text='Image Rotation:', font=('Inter', 10), bg='#ffffff')
    image_rotation_label.grid(row=4, column=0, sticky=tk.W)

    # Image Rotation Variable
    # image_rotation_variable = tk.IntVar(value=0)  # Set default value, e.g., 0
    # image_rotation_variable.trace("w", on_rotation_change)

    with open('Brands/Midori/Midori.pkl', 'rb') as file:
        data = pickle.load(file)

    image_rotation_variable = tk.IntVar(value=data['image_rotation'])


    # Trace the variable to detect changes

    # Radio Buttons for Image Rotation (0, 90, -90, 180)
    image_rotation_0 = tk.Radiobutton(camera_param_frame, text="0", variable=image_rotation_variable, value=0, bg='#ffffff', font=('Inter', 10))
    image_rotation_90 = tk.Radiobutton(camera_param_frame, text="90(CW)", variable=image_rotation_variable, value=90, bg='#ffffff', font=('Inter', 10))
    image_rotation_neg90 = tk.Radiobutton(camera_param_frame, text="-90(CCW)", variable=image_rotation_variable, value=-90, bg='#ffffff', font=('Inter', 10))
    image_rotation_180 = tk.Radiobutton(camera_param_frame, text="180", variable=image_rotation_variable, value=180, bg='#ffffff', font=('Inter', 10))

    # Positioning the Radio Buttons
    image_rotation_0.grid(row=5, column=0, sticky=tk.W, padx=1)
    image_rotation_90.grid(row=5, column=1, sticky=tk.W, padx=1)
    image_rotation_neg90.grid(row=6, column=0, sticky=tk.W, padx=1)
    image_rotation_180.grid(row=6, column=1, sticky=tk.W, padx=1)

    # image_rotation_variable.set(image_rotation_variable)
    

    






    # reject_on_radiobtn = tk.Radiobutton(reject_param_frame, text='Yes',variable=reject_radiobtn_variable, command = sel_rej,
    #                                   value=1, width=4, fg = 'green', font = ('Inter',10),bg='#ffffff')
    # reject_on_radiobtn.grid(row=4,column=0)
    
    ############################################ Parameters for Save Data Settings ######################################################
        ########################################################################################################################
            ###############################################################################################################
    def save_data_frame_display():
        exposure_time_label.grid_forget()
        exposure_time_entry.grid_forget()
        # trigger_delay_label.grid_forget()
        # trigger_delay_entry.grid_forget()
        camera_gain_label.grid_forget()
        camera_gain_entry.grid_forget()
        roi_label.grid_forget()
        roi_entry.grid_forget()
        open_image_btn.grid_forget()
        # image_rotation_label.grid_forget()
        
        save_img_checkbox.grid(row=1,column=0,sticky=tk.W)
        crop_checkbox.grid(row=1,column=1,sticky=tk.E,padx=3)
        save_ng_checkbox.grid(row=2,column=0,sticky=tk.W)
        choose_dir_label.grid(row=2,column=1,sticky=tk.E,padx=3)
        choose_dir_entry.grid(row=3,column=1,sticky=tk.E,padx=3)
        save_result_checkbox.grid(row=3,column=0,sticky=tk.W)
        data_save_label.config(state=DISABLED)
        camera_param_btn.config(state=ACTIVE)

    data_save_label = tk.Button(camera_save_frame, text = 'Save Data',justify='center',image=save_data_icon, width=114 ,font = ('Inter',10,'bold'),bg='#ffffff',compound=LEFT, command=save_data_frame_display)
    data_save_label.grid(row=0,column=1,sticky=tk.W)

    ##################################################### Save Image ###################################################
    save_img_value = int(brand_values['save_img'])
    global save_img_status
    save_img_status = save_img_value
    if save_img_value == 0:
        img_status = 0
    else:
        img_status = 1
    save_img_checkbox = tk.Checkbutton(camera_param_frame, text="Save Image", variable=save_img_variable, onvalue= 1, offvalue = 0, command = save_img_btn,bg='#ffffff')
    save_img_variable.set(img_status)

    ##################################################### crop image save ###############################################
    crop_img_save_value = int(brand_values['crop'])
    global crop_save
    crop_save = crop_img_save_value
    if crop_img_save_value == 0:
        crop_status = 0
    else:
        crop_status = 1
    crop_checkbox = tk.Checkbutton(camera_param_frame, text="Crop", variable=crop_img_variable, onvalue= 1, offvalue = 0, command = save_crop_img,bg='#ffffff')
    crop_img_variable.set(crop_status)

    ##################################################### Save Not Good Image #################################################
    save_ng_value = int(brand_values['save_ng'])
    global save_ng_status
    save_ng_status = save_ng_value
    if save_ng_value== 0:
        imgnd_status = 0
    else:
        imgnd_status = 1
    save_ng_checkbox = tk.Checkbutton(camera_param_frame, text="Save NG Image", variable=save_ng_variable, onvalue= 1, offvalue = 0, command = save_imgnd,bg='#ffffff')
    save_ng_variable.set(imgnd_status)

    ######################################################### Choose Directory #####################################################
    choose_dir_label = tk.Button(camera_param_frame, text="Choose Folder", command=choose_directory,bg='yellow')
    choose_dir_variable = tk.StringVar(camera_param_frame, value = str(brand_values['img_dir']))
    choose_dir_entry = tk.Entry(camera_param_frame, font = ('Inter',8), textvariable = choose_dir_variable,relief='solid')

    ############################################################ Save Result ###################################################
    save_result_value = int(brand_values['save_result'])
    global save_result_status
    save_result_status = save_result_value
    if save_result_value == 0:
        result_status = 0
    else:
        result_status = 1
    save_result_checkbox = tk.Checkbutton(camera_param_frame, text="Save Result", variable=save_result_variable, onvalue= 1, offvalue = 0, command = saverec_img,bg='#ffffff')
    save_result_variable.set(result_status)
   
    ########################################################### Update Button For Camera Settings Save Data ###########################
    camera_update_btn = tk.Button(camera_param_frame, text='Update', fg='white',width=30,font=('Inter',10,'bold'), bg='#019065', relief='flat',command = save_gui_values)
    camera_update_btn.grid(row=8,column=0,sticky=tk.W,columnspan=2)

    ########################################### New Brand Creation Parameter #########################################
        ##########################################################################################################
            #################################################################################################
    new_brand_frame = tk.Frame(window, highlightbackground='#D4CDCD',bg='#ffffff',highlightthickness=1,bd=1,relief='solid')
    # new_brand_frame.place(x=left_x+740, y = upper_y-25)
    def new_brand(): 
        toplevel = Toplevel(window)
        toplevel.title("New Brand")
        toplevel.geometry("300x100")
        new_brand_lbl = Label(toplevel, text = 'New Brand Name:' ,font = ('Inter',10,'bold'),bg = 'white')
        new_brand_lbl.place(x = left_x-25, y = upper_y-20)
        brand_name_val = tk.StringVar(toplevel, value = brand_values['brand_name'])
     
        new_brand_entry = Entry(toplevel, font = ('Inter',10,'bold'),textvariable= brand_name_val)
        new_brand_entry.place(x =left_x+105, y = upper_y-20)
        def add_brand():
            os.makedirs(os.getcwd()+'/Brands/'+new_brand_entry.get()+'/recognition_result')
            os.makedirs(os.getcwd()+'/Brands/'+new_brand_entry.get()+'/detection_result')
            new_brand_fun(new_brand_entry.get()
                         ,no_of_line_combo.get()
                         ,'None'
                         ,'None'
                         ,'None'
                         ,'None'
                        ,min_per_thresh_entry.get()
                        ,line_per_thresh_entry.get()
                        ,reject_count_entry.get()
                        ,0
                        ,0
                        ,0
                        ,float(exposure_time_entry.get())
                        ,int(trigger_delay_entry.get())
                        ,float(camera_gain_entry.get())
                        ,'500:750,200:1800'
                        ,0
                        ,0
                        ,0
                        ,1
                        ,'None'
                        )
            tkinter.messagebox.showinfo('Info',"Successfully created a new brand")
            toplevel.destroy() 
        new_brand_window = Button(toplevel, text = 'Add',command = add_brand, font = ('Inter',10,'bold'), bg = 'blue',fg = 'white')
        new_brand_window.place(x = left_x+125, y = upper_y+10)
        
    ##################################### For Silencing the Line Entry Boxes according to no. of lines entry box ###############
    silence_line(brand_values['no_of_lines'], param_values[0])
  
    ######################################### Combo Box for New Brand #####################################################
    brandsel_val.set("Brand")
    brand_chosen = ttk.Combobox(new_brand_frame, width = 14, textvariable = brandsel_val, font= ('Inter',10,'bold'))
    chosen_brand = brandsel_val.get()

    ######################################### Adding combobox drop down list #############################################
    brand_dirs = 'Brands'
    def update(event):
        all_brands = os.listdir(os.path.join(os.getcwd(),brand_dirs))
        brand_chosen['values'] = all_brands
    brand_chosen.bind("<Button-1>", update)
    brand_chosen.grid(row=0,column=0,columnspan=2,rowspan=2)

    new_brand_btn = tk.Button(new_brand_frame, text = 'New\nBrand', font=('Inter',8,'bold'), command = new_brand, bg = '#caf0f8')
    new_brand_btn.grid(row=2,column=0,pady=4)
    button = Button(new_brand_frame, text = "Confirm\nHere" , command = select_brand , bg = '#bde0fe', font=('Inter',8,'bold'))
    button.grid(row=2,column=1)
    
    ######################################### Detection Result Analysis Parameters ################################################
        ######################################################################################################################
            #############################################################################################################
    
    ########################################### Detection Result #####################################################
    detect_result_label = tk.Label(detection_result_frame, text = 'Detection Result', font = ('Inter',10,'bold'),bg='#ffffff')
    detect_result_label.grid(row=0, column=0,columnspan=3)

    ########################################### Detection Time #######################################################
    detect_time_label = tk.Label(detection_result_frame, text = 'Time', font = ('Inter',10,'bold'),bg='#ffffff')
    detect_time_label.grid(row=2,column=0,columnspan=2,sticky=tk.W)

    ########################################### Center Image Name ####################################################
    center_image_name = Label( window , text = brand_values['brand_name'] , font = ('Inter', 10, 'bold'))
    center_image_name.place(x = left_x+515, y = upper_y+60)  

    ########################################### Last 10 Results #####################################################
    last_ten_label = tk.Label(last_10_frame, text = 'Last 10 Results', font = ('Inter',10,'bold'),bg='#ffffff')
    last_ten_label.grid(row=0, column=0,columnspan=5)

    ############################################ Good ##############################################################
    good_count_label = tk.Label(detection_analysis_frame, text = 'Good:', font = ('Inter',10,'bold'),bg='#ffffff')
    good_count_label.grid(row=0,column=0,sticky=tk.W,pady=2)
    
    ############################################ Not Good ############################################################
    not_good_count_label = tk.Label(detection_analysis_frame, text = 'Not Good:', font = ('Inter',10,'bold'),bg='#ffffff')
    not_good_count_label.grid(row=1,column=0,sticky=tk.W)

    ############################################## Count Since Last ND ##################################################
    last_ng_count_label = tk.Label(detection_analysis_frame, text = 'Last NG Count', font = ('Inter',10,'bold'),bg='#ffffff')
    last_ng_count_label.grid(row=2,column=0,sticky=tk.W,pady=2)

    ############################################### Time Since Last ND ##################################################
    last_ng_time_label = tk.Label(detection_analysis_frame, text = 'Last NG Time', font = ('Inter',10,'bold'),bg ='#ffffff')
    last_ng_time_label.grid(row=3,column=0,sticky=tk.W)

    v15 = int(param_values[1])
    global save_image_sel_val
    save_image_sel_val = v15
    if v15 == 0:
        image_status = 0
    else:
        image_status = 1
   
    ################################################# Reset Counter Button ##################################################
    reset_counter_btn = tk.Button(detection_analysis_frame, text='Reset Counter', fg='white',width=27,font=('Inter',7,'bold','bold'), bg='#D9305C', relief='flat',command=lambda: reset_counter(window, right_x, upper_y))

    reset_counter_btn.grid(row=4,column=0,columnspan=2)

    ################### Previous Not Good Image ###########
    previous_ng_img_label = tk.Label(window, text = 'Last NG Image', font = ('Inter',10,'bold'))
    previous_ng_img_label.place(x = right_x, y = upper_y+425)

windows_start()
window.mainloop()
    
######################### Developed By Crimson Tech Pvt. Ltd. #####################################
################# Diwash Poudel , Chhabi Lal Tamang , Samvandha Pathak ############################
    
