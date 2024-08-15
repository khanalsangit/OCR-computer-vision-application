import tkinter as tk
from tkinter import ttk

window = tk.Tk()
window.title('jehe')
window.geometry('600x600')
# system_param_frame = tk.Frame(window, highlightbackground='#D4CDCD',bg='#ffffff',highlightthickness=2,bd=2) #border for detection result
# system_param_label = tk.Label(system_param_frame, text = 'System Settings',justify='center', font = ('Inter',11),bg='#ffffff')
# det_radio = tk.Radiobutton(system_param_frame, value=0, text = 'Detection Only',  fg = 'black', font = ('Inter', 10, 'bold' ),bg='#ffffff')
# both_radio = tk.Radiobutton(system_param_frame, value = 1, text = 'Detection & Recognition',  fg = 'black', font = ('Inter',10,'bold'),bg='#ffffff')
# line_input = tk.Label(system_param_frame, text = 'No. of Lines:',  font = ('Inter',10,'bold'),bg='#ffffff')
# linesno = ttk.Combobox(system_param_frame, width = 17,  justify='center', font= ('Inter',10,'bold'))
# line1 = tk.Label(system_param_frame, text = 'Line 1',  font = ('Inter',10,'bold'),bg='#ffffff')
# line1_input = tk.Entry(system_param_frame, font = ('Inter',10,'bold'),relief='solid',width=20,justify='center')
# line2 = tk.Label(system_param_frame, text = 'Line 2',  font = ('Inter',10,'bold'),bg='#ffffff')
# line2_input = tk.Entry(system_param_frame, font = ('Inter',10,'bold'),relief='solid',width=20,justify='center')
# line3 = tk.Label(system_param_frame, text = 'Line 3',  font = ('Inter',10,'bold'),bg='#ffffff')
# line3_input = tk.Entry(system_param_frame, font = ('Inter',10,'bold'),relief='solid',width=20,justify='center')
# line4 = tk.Label(system_param_frame, text = 'Line 4',  font = ('Inter',10,'bold'),bg='#ffffff')
# line4_input = tk.Entry(system_param_frame, font = ('Inter',10,'bold'),relief='solid',width=20,justify='center')

# system_param_frame.place(x=50,y=0)
# system_param_label.grid(row=0,column=0,sticky=tk.W)
# det_radio.grid(row=1,column=0,sticky=tk.W)
# both_radio.grid(row=2,column=0,sticky=tk.W,columnspan=4)
# line_input.grid(row=3,column=0,sticky=tk.W)
# linesno.grid(row=3,column=1,sticky=tk.W)
# line1.grid(row=4,column=0,sticky=tk.W)
# line1_input.grid(row=4,column=1,sticky=tk.W)
# line2.grid(row=5,column=0,sticky=tk.W)
# line2_input.grid(row=5,column=1,sticky=tk.W)
# line3.grid(row=6,column=0,sticky=tk.W)
# line3_input.grid(row=6,column=1,sticky=tk.W)
# line4.grid(row=7,column=0,sticky=tk.W)
# line4_input.grid(row=7,column=1,sticky=tk.W)

#################### Frame for Camera Settings #################
camera_param_frame = tk.Frame(window, highlightbackground='#D4CDCD',bg='#ffffff',highlightthickness=2,bd=2, relief='solid') #border for detection result
camera_param_frame.place(x=50,y=50)
camera_param_label = tk.Label(camera_param_frame, text = 'Camera Settings',justify='center', font = ('Inter',10,'bold'),bg='#ffffff')
camera_param_label.grid(row=0,column=0,sticky=tk.W,columnspan=2)

########## Exposure Time #############
ET = tk.Label(camera_param_frame, text = 'Exposure Time', font = ('calibre',10),bg='#ffffff')
ET.grid(row=1,column=0,sticky=tk.W)
v5 = tk.StringVar(camera_param_frame)
ET_input = tk.Entry(camera_param_frame, font = ('calibre',10),width=8, textvariable= v5,relief='solid',justify='center')
ET_input.grid(row=1,column=2,sticky=tk.E)

########## Trigger Delay #############
PT = tk.Label(camera_param_frame, text = 'Trigger Delay', font = ('calibre',10),bg='#ffffff')
PT.grid(row=2,column=0,sticky=tk.W)
v6 = tk.StringVar(camera_param_frame)
PT_input = tk.Entry(camera_param_frame, font = ('calibre',10),width=8, textvariable= v6,relief='solid',justify='center')
PT_input.grid(row=2,column=2,sticky=tk.E)

########## Camera Gain #############
CG = tk.Label(camera_param_frame, text = 'Camera Gain', font = ('calibre',10),bg='#ffffff')
CG.grid(row=3,column=0,sticky=tk.W)
v7 = tk.StringVar(camera_param_frame)
CG_input = tk.Entry(camera_param_frame, font = ('calibre',10),width=8, textvariable= v7,relief='solid',justify='center')
CG_input.grid(row=3,column=2,sticky=tk.E)

##################### image ROI ################
ROI = tk.Label(camera_param_frame , text = "ROI" , font = ('caliber', 10, 'bold'),bg='#ffffff')
ROI.grid(row=5,column=0,sticky=tk.W)
roi = tk.StringVar(camera_param_frame)
ROI_input = tk.Entry(camera_param_frame, font = ('calibre',10),relief='solid',width=10, textvariable=roi)
ROI_input.grid(row=5,column=1,columnspan=2)

# Create a button to open an image
btn_open = tk.Button(camera_param_frame, text="Open Image",bg='blue',font = ('calibre',8),command=open_image,foreground='white')
#ROI_input.place(x = left_x+40, y = upper_y+565)
btn_open.grid(row=5,column=2,sticky=tk.E)

######## Update Button For Camera Settings ##################
camera_param_btn = tk.Button(camera_param_frame, text='Update', fg='white',width=30,font=('Inter',10), bg='#3e8223', relief='flat')
camera_param_btn.grid(row=6,column=0,sticky=tk.W,columnspan=3)

window.mainloop()