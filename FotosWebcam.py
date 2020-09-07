import cv2
import numpy as np
import face_recognition as fr
import datetime
import os
import click
import time
from playsound import playsound


REVERSE = 640
known_people_path = f"{os.path.expanduser('~')}/Github/FotosWebcam/Identidades/"
stopmotion_base_path = f"{os.path.expanduser('~')}/Github/FotosWebcam/"
Last_photo = time.perf_counter() - 4
img_counter = 0

def get_known_faces(known_people_folder):

    known_names = []
    known_face_encodings = []

    for file in os.listdir(known_people_folder):

        basename = os.path.splitext(os.path.basename(file))[0]
        img = fr.load_image_file(f"{known_people_path}{file}")
        encodings = fr.face_encodings(img)

        if len(encodings) > 1:
            click.echo(f"WARNING: More than one face found in {file}. Only considering the first face.")

        if len(encodings) == 0:
            click.echo(f"WARNING: No faces found in {file}. Ignoring file.")
        else:
            known_names.append(basename)
            known_face_encodings.append(encodings[0])

    return known_names, known_face_encodings


cam = cv2.VideoCapture(0)

known_names, known_face_encodings = get_known_faces(known_people_path)

cv2.namedWindow("Auto Photo Camera")



while True:
    ret, frame = cam.read()

    # Flip horizontally
    frame = cv2.flip(frame, 1)

    if not ret:
        print("Failed to grab frame")
        break

    rgb_frame = frame[:, ::-1]

    face_locations = fr.face_locations(rgb_frame)
    face_encodings = fr.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

        matches = fr.compare_faces(known_face_encodings, face_encoding)

        # Correction needed because of flipped image
        right = REVERSE - right
        left = REVERSE - left

        name = "Unknow"

        face_distances = fr.face_distance(known_face_encodings, face_encoding)

        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name = f"{known_names[best_match_index]}"



        if     (left-400)in range(0, 40)\
           and (240-right)in range(0, 40)\
           and (top-150)in range(0, 40)\
           and (400-bottom)in range(0, 40):
            color = (0,255,0)
            if ( time.perf_counter() - Last_photo ) > 4:
                playsound("Beep.mp3")
                playsound("Shutter.mp3")
                img_name = f"{stopmotion_base_path}{name}/{name}_{datetime.datetime.today()}.png"
                cv2.imwrite(img_name, frame)
                print("{} written!".format(img_name))
                Last_photo = time.perf_counter()
        else:
            color = (0, 0, 255)

        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.rectangle(frame, (left, bottom), (right, bottom + 35), (255, 0, 0), cv2.FILLED)

        cv2.rectangle(frame, (200, 150), (440, 400), (0, 255, 0), 2)

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, name,(right + 6 , bottom + 25), font , 0.7, (0, 255, 255), 1)

    cv2.imshow("Auto Photo Camera", frame)

    k = cv2.waitKey(1)

    if k%256 == 27:
        #ESC is pressed
        print("Scape press, closing...")
        break

    elif k%256 == 32:
        # SPACE is pressed
        playsound("Beep.mp3")
        playsound("Shutter.mp3")
        img_name = f"{name}_{img_counter}.png"
        cv2.imwrite(img_name,frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()
cv2.destroyAllWindows()



