import pandas as pd
import cv2
from pathlib import Path
import shutil, os, subprocess


df = pd.read_csv("../Vincom Retail (1).csv")

df_undone = df[df['Review']=="None"]
VIDEO_ROOT = Path("/media/vantix01/My Book/download_video/video/VCR/20200915")
DEST = Path("/media/vantix01/My Book/download_video/video/VCR/20200915")


def is_video_valid(file_path:str)->bool:
    fps = cv2.VideoCapture(str(file_path)).get(cv2.CAP_PROP_FPS)
    int_fps = int(fps)
    return False if int_fps == 0 else True

def convert_to_480(source:str, dest_folder:str):
    filename = source.split('/')[-1]
    filename_split_dot = filename.split('.')
    new_filename = f"{filename_split_dot[0]}_480.{filename_split_dot[-1]}"
    new_filepath = os.path.join(dest_folder, new_filename)
    subprocess.call(["ffmpeg","-y", "-i", source, "-s", "hd480", "-c:v",
        "libx264", "-crf", "23", "-c:a", "aac", "-strict", "-2", new_filepath],
         stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    return new_filepath

for i, row in df_undone.iterrows():
    video_filename = row['Video name']
    print("*"*20)
    print(f"Process video {video_filename}")
    all_vids = list(VIDEO_ROOT.rglob(video_filename))
    print(f"Found {all_vids}")
    for vid in all_vids:
        if is_video_valid(vid):
            print(vid)
            dest_filename = VIDEO_ROOT/video_filename
            if str(vid) == str(dest_filename):
                print(f"Skip, same file")
            if dest_filename.is_file():
                os.remove(str(dest_filename))
            shutil.copy2(vid, dest_filename)
            print(f"Copied new video {video_filename}")
            new_path = convert_to_480(str(vid), str(DEST))
            print(f"Converted new file {new_path}")
            continue
