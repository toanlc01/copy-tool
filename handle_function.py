import os, shutil, subprocess
import cv2
from logger import logger
# move these functions here because multiprocess.Pool require to run imported functions
# or the call has to come from main
def create_destination_by_filename(dest:str, filepath:str)->str:
    filename = filepath.split('/')[-1]
    filename_split = filename.split('_')

    # if samsung filename will be 09092020_123025.mp4
    # vsmart will be VID_09092020_123025.mp4
    date_of_file = filename_split[0] if len(filename_split) == 2 else filename_split[1]
    dest_with_date = os.path.join(dest, date_of_file)
    os.makedirs(dest_with_date, exist_ok=True)
    return dest_with_date

def convert_to_480(source:str, dest_folder:str):
    filename = source.split('/')[-1]
    filename_split_dot = filename.split('.')
    new_filename = f"{filename_split_dot[0]}_480.{filename_split_dot[-1]}"
    new_filepath = os.path.join(dest_folder, new_filename)
    subprocess.call(["ffmpeg","-y", "-i", source, "-s", "hd480", "-c:v",
        "libx264", "-crf", "23", "-c:a", "aac", "-strict", "-2", new_filepath],
         stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    return new_filepath

def is_video_valid(file_path:str)->bool:
    fps = int(cv2.VideoCapture(file_path).get(cv2.CAP_PROP_FPS))
    logger.info(f"Video {file_path} has fps {fps}")
    return False if fps == 0 else True

def handle_one_phone(source_list:str, destination:str, is_delete:bool, is_convert):
    """Handle one phone at a time to avoid multiple read from a single 
    phone that can damage video"""
    logger.info(f"Start handle one phone")
    for source in source_list:
        handle_one_file(source, destination, is_delete, is_convert)

def handle_one_file(source:str, destination:str, is_delete:bool, is_convert:bool):
    dest = create_destination_by_filename(destination, source)
    filename = source.split("/")[-1]
    filename_dest = os.path.join(dest, filename)
    if not is_video_valid(source):
        logger.error(f"Video {source} is unreadable. Skipping")
        return
    while True:
        logger.info(f"Start copy video {source}")
        shutil.copy2(source, dest)
        if is_video_valid(filename_dest):
            logger.info(f"Copied file {source.split('/')[-1]} to {dest}")
            break
        else:
            logger.warning(f"Failed to copy Video {source} to {filename_dest}. Retrying")
            os.remove(filename_dest)

    # delete source after copy if needed
    if is_delete:
        os.remove(source)
        logger.info(f"Deleted {source}")

    # convert source file to mp4 and save to a new if needed
    if is_convert:
        while True:
            converted_mp4_path = convert_to_480(source, dest)
            if is_video_valid(converted_mp4_path):
                logger.info(f"Converted new file :{converted_mp4_path}")
                break
            else:
                logger.warning(f"Failed to convert_video {source}. Retrying")
                