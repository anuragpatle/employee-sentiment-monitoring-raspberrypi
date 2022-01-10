#! /usr/bin/python
import requests
from imutils.video import VideoStream
from imutils.video import FPS
import imutils
import time
import cv2
import sys
from datetime import datetime
import pytz
from pathlib import Path
import json

# it will get the time zone
# of the specified location
IST = pytz.timezone('Asia/Kolkata')
POST_IMAGE_URL = 'http://20.102.100.20:8080/face_app/upload_for_training'
DEVICE_ID = 'tsystem-PU-5-r1-device1'
# todays_date = today = date.today()


def capture_headshots():
    # Ask name for the person
    first_name = input(
        "\nPlease enter the first name of the person this face belongs to: ")
    first_name = first_name.strip()
    last_name = input("Please enter the last name: ")
    last_name = last_name.strip()

    emp_name = first_name + "_" + last_name
    emp_id = input("Please enter employee id: ")
    images_dir_name = emp_name + "-" + emp_id
    Path("dataset/" + images_dir_name).mkdir(parents=True, exist_ok=True)

    cam = cv2.VideoCapture(1)

    cv2.namedWindow("press space to take a photo", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("press space to take a photo", 500, 300)

    img_counter = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("press space to take a photo", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:
            # SPACE pressed

            datetime_ist = datetime.now(IST)

            current_datetime = datetime_ist.strftime(
                '%d-%m-%Y %H:%M:%S %Z %z')
            current_date = datetime_ist.strftime('%Y-%m-%d')
            current_time = datetime_ist.strftime('%H:%M:%S')
            current_timestamp = datetime.timestamp(datetime_ist)
            # new_image = str(current_timestamp) + '_face.jpg'

            # print("[INFO] Object found. Saving locally.")
            # cv2.imwrite("imgs_for_recog/" + new_image, roi_color)

            img_name = "dataset/" + images_dir_name + \
                "/image_{}.jpg".format(current_timestamp)
            cv2.imwrite(img_name, frame)

            print("{} written!".format(img_name))

            my_img = {
                'file': open(img_name, 'rb')
            }
            data = {
                'current_date': current_date,
                'current_time': current_time,
                'current_datetime': current_datetime,
                'device_id': DEVICE_ID,
                'emp_name': emp_name,
                'emp_id': emp_id
            }

            r = requests.post(POST_IMAGE_URL, files=my_img, data=data)

            # convert server response into JSON format.
            print(r)

    cam.release()

    cv2.destroyAllWindows()


if __name__ == '__main__':
    capture_headshots()
