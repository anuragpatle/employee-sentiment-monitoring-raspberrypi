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

# it will get the time zone
# of the specified location
IST = pytz.timezone('Asia/Kolkata')
POST_IMAGE_URL = 'http://20.102.100.20:8080/face_app/upload_for_recog'
DEVICE_ID = 'tsystem-PU-5-r1-device1'
# todays_date = today = date.today()


class CaptureAndSendImages:

    def capture_and_send_faces(self):

        # initialize the video stream and allow the camera sensor to warm up
        # Set the ser to the followng
        # src = 0 : for the build in single web cam, could be your laptop webcam
        # src = 2 : I had to set it to 2 inorder to use the USB webcam attached to my laptop
        vs = VideoStream(src=1, framerate=50).start()
        # vs = VideoStream(usePiCamera=True).start()

        # start the FPS counter
        fps = FPS().start()

        # loop over frames from the video file stream
        while True:
            time.sleep(2.0)
            # grab the frame from the threaded video stream and resize it
            # to 500px (to speedup processing)
            frame = vs.read()

            # image = cv2.imread(frame)
            image = frame
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # faceCascade = cv2.CascadeClassifier(
            #     cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

            faceCascade = cv2.CascadeClassifier(
                "haarcascade_frontalface_default.xml")
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.3,
                minNeighbors=3,
                minSize=(30, 30)
            )

            print("[INFO] Found {0} Faces.".format(len(faces)))

            if (len(faces) < 1):
                continue

            for (x, y, w, h) in faces:
                # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                roi_color = image[y:y + h, x:x + w]

                datetime_ist = datetime.now(IST)

                current_datetime = datetime_ist.strftime(
                    '%d-%m-%Y %H:%M:%S %Z %z')
                current_date = datetime_ist.strftime('%Y-%m-%d')
                current_time = datetime_ist.strftime('%H:%M:%S')
                new_image = str(datetime.timestamp(datetime_ist)) + '_face.jpg'
                print("[INFO] Object found. Saving locally.")
                cv2.imwrite("imgs_for_recog/" + new_image, roi_color)

                my_img = {
                    'file': open("imgs_for_recog/" + new_image, 'rb')
                }

                data = {
                    'current_date': current_date,
                    'current_time': current_time,
                    'current_datetime': current_datetime,
                    'device_id': DEVICE_ID
                }

                r = requests.post(POST_IMAGE_URL, files=my_img, data=data)

                # convert server response into JSON format.
                print(r)

            # status = cv2.imwrite('faces_detected.jpg', image)
            # print("[INFO] Image faces_detected.jpg written to filesystem: ", status)

            # display the image to our screen
            # cv2.imshow("Facial Recognition is Running", frame)
            key = cv2.waitKey(1) & 0xFF

            # quit when 'q' key is pressed
            if key == ord("q"):
                break

            # update the FPS counter
            fps.update()

        # stop the timer and display FPS information
        fps.stop()
        print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

        # do a bit of cleanup
        cv2.destroyAllWindows()
        vs.stop()


def send_captured_image(image_name_with_path):

    datetime_ist = datetime.now(IST)
    current_datetime = datetime_ist.strftime(
        '%d-%m-%Y %H:%M:%S %Z %z')
    current_date = datetime_ist.strftime('%Y-%m-%d')
    current_time = datetime_ist.strftime('%H:%M:%S')

    my_img = {
        'file': open(image_name_with_path, 'rb')
    }

    data = {
        'current_date': current_date,
        'current_time': current_time,
        'current_datetime': current_datetime,
        'device_id': DEVICE_ID
    }

    r = requests.post(POST_IMAGE_URL, files=my_img, data=data)

    # convert server response into JSON format.
    print(r)


if __name__ == "__main__":
    object = CaptureAndSendImages()
    object.capture_and_send_faces()
    # object.send_captured_image("some_path")
