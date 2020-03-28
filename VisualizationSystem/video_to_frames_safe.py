import numpy as np
import cv2
import os

# Set variable(s)
input_folder = 'input'
input_file = 'recording.mkv'
output_folder = 'frames'
output_description_filename  = 'description.txt'
output_frame_filename  = 'frame'
output_frame_extension  = 'jpg'


def showVideoInfo(video_path):
    """
    Print information about the input video
    """

    # Print input file
    print("[Loading] Input file: {}".format(video_path))

    # Print file stats
    try:
        vhandle = cv2.VideoCapture(video_path)
        fps = int(vhandle.get(cv2.CAP_PROP_FPS))
        count = int(vhandle.get(cv2.CAP_PROP_FRAME_COUNT))
        size = {
            'width': int(vhandle.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(vhandle.get(cv2.CAP_PROP_FRAME_HEIGHT))
        }
        ret, firstframe = vhandle.read()
        if ret:
            print("[Loading] File stats:")
            print(" - Fps: %d" % fps)
            print(" - Count: %d" % count)
            print(" - Width: %d" % size['width'])
            print(" - Height: %d" % size['height'])
            vhandle.release()
            return fps, count, size
        else:
            print("Video can not read!")
        
    except:
        "Error in showVideoInfo" 


def save_description_file(output_file_path, count):
    """
    Save video information to a description file
    """
    with open(output_file_path, 'w') as f:
        f.write(str(count))


def video_to_frames(video_path, output_folder, output_frame_filename, output_frame_extension, count):
    """
    Read each frame and store it as image
    """
    cap = cv2.VideoCapture(video_path)
    while(cap.isOpened()):
        frame_number = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        ret, frame = cap.read()
        output_frame_path = os.path.join(output_folder, output_frame_filename + '-' + str(frame_number).zfill(6) + '.' + output_frame_extension)
        cv2.imwrite(output_frame_path, frame)
        print("[Video_to_Frame] Processing {} of {}".format(frame_number, count))
    cap.release()


def video_to_frames_2(video_path, output_folder, output_frame_filename, output_frame_extension, count):
    """
    Read each frame and store it as image
    """
    cap = cv2.VideoCapture(video_path)
    success, frame = cap.read()
    frame_number = 0
    while (frame_number < count):
        output_frame_path = os.path.join(output_folder, output_frame_filename + '-' + str(frame_number).zfill(6) + '.' + output_frame_extension)
        cv2.imwrite(output_frame_path, frame)
        print("[Video_to_Frame] Processing {} of {}".format(frame_number, count))
        success, frame = cap.read()
        frame_number += 1
    cap.release()


# Show Video Information
input_file_path = os.path.join(input_folder, input_file)
fps, count, size = showVideoInfo(input_file_path)

# Create decription file
output_description_path = os.path.join(input_folder, output_description_filename)
if fps == 1000:
    count = int(30 * (count/fps))
save_description_file(output_description_path, count)

# Transform video to image frames
video_to_frames_2(input_file_path, output_folder, output_frame_filename, output_frame_extension, count)