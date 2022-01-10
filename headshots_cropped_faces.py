import cv2
from pathlib import Path
import requests
import json
import change_camera_resolution as cam_res

# Rest api end points
ROOT_SENTI_API_URI = "http://20.102.100.20:5000/facial-senti-api"
NEW_EMP_SENTI_API_URI = ROOT_SENTI_API_URI + "/add_emp"
headers_ = {'Content-Type': 'application/json'}


def capture_headshots():
    # Ask name for the person
    first_name = input(
        "\nPlease enter the first name of the person this face belongs to: ")
    first_name = first_name.strip()
    last_name = input("Please enter the last name: ")
    last_name = last_name.strip()

    name = first_name + "_" + last_name
    emp_id = input("Please enter employee id: ")
    images_dir_name = name + "-" + emp_id
    Path("dataset/" + images_dir_name).mkdir(parents=True, exist_ok=True)
    data_ = {"emp_id": emp_id, "emp_name": name}
    data_ = json.dumps(data_, indent=4)

    # r = requests.post(url=NEW_EMP_SENTI_API_URI, data=data_, headers=headers_)
    # print("Return of post request", r)

    cam = cv2.VideoCapture(1)

    # How to reduce image size
    # Try: #1
    res = cam_res.ChangeResolution(cam)
    res.make_480p()
    # Try: #1
    # ret, frame = cam.read()
    # scale_percent = 60 # percent of original size
    # width = int(frame.shape[1] * scale_percent / 100)
    # height = int(frame.shape[0] * scale_percent / 100)
    # dim = (width, height)
    # image
    # resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

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
            img_name = "dataset/" + images_dir_name + \
                "/image_{}.jpg".format(img_counter)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faceCascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.3,
                minNeighbors=3,
                minSize=(30, 30)
            )

            print("[INFO] Found {0} Faces.".format(len(faces)))

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                roi_color = frame[y:y + h, x:x + w]
                print("[INFO] Object found. Saving locally.")
                cv2.imwrite(str(w) + str(h) + '_faces.jpg', roi_color)
                cv2.imwrite(img_name, frame)
                print("{} written!".format(img_name))
                img_counter += 1

            # status = cv2.imwrite('faces_detected.jpg', frame)
            # print("[INFO] Image faces_detected.jpg written to filesystem: ", status)

            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1

    cam.release()

    cv2.destroyAllWindows()


if __name__ == '__main__':
    capture_headshots()