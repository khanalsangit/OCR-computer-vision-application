import pickle
import os
import numpy as np
import tkinter
from tkinter import messagebox


########## Pickle file for brand name parameters
def new_brand_fun(
    brandname: str,
    nooflines: int,
    line1: str,
    line2: str,
    line3: str,
    line4: str,
    line5: str,
    minperthres: float,
    lineperthres: float,
    rej_count: int,
    rej_enable: int,
    line1_enable: int,
    line2_enable: int,
    exp_time: float,
    trigger_delay: float,
    cam_gain: float,
    ROI: str,
    save_img: int,
    save_ng: int,
    save_result: int,
    crop: int,
    img_dir: str,
    rotate_value: int,
) -> None:
    brand_param = {
        "brand_name": brandname,
        "no_of_lines": nooflines,
        "line1": line1,
        "line2": line2,
        "line3": line3,
        "line4": line4,
        "line5": line5,
        "min_per_thresh": minperthres,
        "line_per_thresh": lineperthres,
        "reject_count": rej_count,
        "reject_enable": rej_enable,
        "line1_enable": line1_enable,
        "line2_enable": line2_enable,
        "exposure_time": exp_time,
        "trigger_delay": trigger_delay,
        "camera_gain": cam_gain,
        "roi": ROI,
        "save_img": save_img,
        "save_ng": save_ng,
        "save_result": save_result,
        "crop": crop,
        "img_dir": img_dir,
        "image_rotation": rotate_value,
    }
    ####################### copy to the brands folder ################################
    dir_path = os.path.join(os.getcwd(), "Brands/Midori")
    new_pkl_dir = os.path.join(dir_path, "{}.pkl".format(brandname))
    pickle.dump(brand_param, open(new_pkl_dir, "wb"))

    ####################### copy to the pickle folder ###############################
    pickle_path = os.path.join(os.getcwd(), "Pickle")
    new_pkl_path = os.path.join(pickle_path, "{}.pkl".format(brandname))
    pickle.dump(brand_param, open(new_pkl_path, "wb"))

    ######################## copy to the system_pickles #############################s
    system_pkl_path = os.path.join(os.getcwd(), "system_pickles")
    new_system_pkl_path = os.path.join(system_pkl_path, "initial_param.pkl")
    pickle.dump(brand_param, open(new_system_pkl_path, "wb"))

    tkinter.messagebox.showinfo("Info", "Default Parameter Set Successfully")


new_brand_fun(
    "Midori",
    4,
    "[^^^^^^^^^^^^^^]",
    "[^^^^^^^^^^^^^^^]",
    "[^^^^^^^^^^^^^^^]",
    "[^^^^^^^^]",
    "[^^^^^]",
    100,
    100,
    10,
    1,
    1,
    1,
    400.0,
    0,
    23.0,
    "0:1000,0:1000",
    0,
    0,
    0,
    1,
    "C:/Users/Dell/Desktop/New_Batch_Code-2/New_Batch_Code/Brands/Midori/images",
    0
)
