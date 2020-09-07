import cv2
import os


known_people_path = f"{os.path.expanduser('~')}/Github/FotosWebcam/Identidades/"
stopmotion_base_path = f"{os.path.expanduser('~')}/Github/FotosWebcam/"
known_names = []


for file in os.listdir(known_people_path):
    basename = os.path.splitext(os.path.basename(file))[0]

    if os.path.exists(f"{stopmotion_base_path}{basename}/"):
        known_names.append(basename)

for name in known_names:
    for filename in os.listdir(f"{stopmotion_base_path}{name}/"):
        extension = os.path.splitext(filename)[1]

        if extension == '.png':

            frame = cv2.imread(f"{stopmotion_base_path}Sebastian/{filename}")

            print(f"Abierta {stopmotion_base_path}Sebastian/{filename}")

            cv2.imshow(name, frame)
            cv2.waitKey(200)


cv2.destroyAllWindows()
