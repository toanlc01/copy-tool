import tkinter
import os
import glob
from tkinter import filedialog
import subprocess
from multiprocessing import Pool, cpu_count
from handle_function import *
from logger import logger

from datetime import datetime
import pytz
import random
import csv
import cv2

VARIABLE = {}

def get_mp4_list(phone_name: str) -> list:
    # Function returns the list of all mp4 4 file paths
    # search for file that ends with mp4
    path = '/run/user/1000/gvfs/'       # Path that contains the phones
    base_path = os.path.join(path, phone_name)
    mp4_list = glob.glob(f"{base_path}/*/Camera*/*mp4")
    # find in SD cards
    mp4_list.extend(glob.glob(f'{base_path}/*/DCIM/Camera*/*mp4'))
    return mp4_list

def all_mp4_list()-> list:
    all_mp4_list = ['video']
    for phone in VARIABLE:
        for mp4 in get_mp4_list(phone):
            all_mp4_list.append(mp4)
    return all_mp4_list

def get_video_duration_list():
    video_duration_list = ['duration']
    mp4_list = all_mp4_list()
    logger.debug(f"mp4 list {mp4_list}")
    for mp4 in mp4_list[1:]:
        video_duration_list.append(get_video_duration(mp4))
    return video_duration_list


def get_size(phones_list:list) -> str:
    # return the the size of videos of chosen device
    size = 0
    for phone in phones_list:
        mp4_list = get_mp4_list(phone)
        for mp4 in mp4_list:
            size += os.path.getsize(mp4)
    if size/100 <= 1024:
        size = str(round(size/1000, 1)) + "KB"
    elif size/100 <= 1048576:
        size = str(round(size/(1024*1000), 1)) + "MB"
    else:
        size = str(round(size/(1048576*1000), 1)) + "GB"
    return size


DESTINATION = ''
def browse():
    # Allow user to select a directory and store it in global var
    # called folder_path
    filename = filedialog.askdirectory(initialdir="/media/vantix01/My Book/download_video/video/VCR")
    DESTINATION = filename
    return filename


def making_video_duration_csv(video_list, video_duration_list):
    # Make a csv file
    today_date = datetime.now(pytz.timezone("Asia/Ho_Chi_Minh")).strftime("%Y%m%d")
    output_filename = f"{today_date}.csv"
    with open(output_filename, 'w') as vid:
        writer = csv.writer(vid)
        writer.writerows(zip(video_list, video_duration_list))
    logger.info(f"Created a duration mapping {output_filename}")

def get_video_duration(filename:str)-> str:
    video = cv2.VideoCapture(filename)
    fps = video.get(cv2.CAP_PROP_FPS)
    logger.debug(f"{filename} has fps: {fps}")
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count/fps
    minutes = round(duration/60, 2)
    video.release()
    return str(minutes) + ' mins'



def go(is_delete:bool, is_update:bool, destination):
    video_list = all_mp4_list()
    video_duration_list = get_video_duration_list()
    making_video_duration_csv(video_list, video_duration_list)

    list_phones_video= []
    for phone in VARIABLE:
        if VARIABLE[phone].get() == 1: # if the phone is chosen
            mp4_list = get_mp4_list(phone)
            list_phones_video.append(mp4_list)

    with Pool(len(list_phones_video)) as p:
        p.starmap(handle_one_phone, [
            (source, destination, is_delete, is_update)
            for source in list_phones_video 
        ])



