import time
import cv2
import numpy as np
import serial
import torch

# Serial setting
ser = serial.Serial('/dev/ttyUSB2', 115200)  # Change port number here
time.sleep(2)

# Camera settings
mtx = np.array([[472.08453552, 1, 280.64475909],
                [0, 474.26711916, 274.83454714],
                [0, 0, 1]])
dist = np.array([-0.35203611, 0.19904214, 0.00167646, -0.00205872, -0.07122155])
w, h = 640, 480

newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
newcameramtx = np.array(newcameramtx)


def get_model():
    model = torch.hub.load("../yolov5-new-main", 'custom', path="/home/kamata/Program/yolov5-new-main/models/BLweights_epoch_200.pt", source='local')
    return model


def get_result(img, model):
    result = model(img, size=640)
    return result


def yolo_detection(model, camera_index=2, exposure_value=750):
    model.conf = 0.55
    objects = [0]

    camera = cv2.VideoCapture(camera_index)
    camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    camera.set(cv2.CAP_PROP_EXPOSURE, exposure_value)

    while True:
        ret, imgs = camera.read()

        # Undistort the loaded image
        # dst = cv2.undistort(imgs, mtx, dist, None, newcameramtx)
        # dst = dst[80:410, 35:480]
        # dst = cv2.resize(dst, (640, 480))

        result = get_result(imgs, model)
        result.render()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        objects = result.pandas().xyxy[0]
        if len(objects) == 0:
            continue
        else:
            break

    objects_sorted = objects.sort_values(by='xmax')
    reverse_object = objects_sorted.iloc[0, 5]

    if reverse_object == 0:
        print("BLF")
    elif reverse_object == 1:
        print("BLB")

    print(reverse_object)
    print("yolo_done")

    return reverse_object


def main_loop():
    model = get_model()

    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        next_part = yolo_detection(model)
        print(f"next_part: {next_part}")
        ser.write(bytes(str(int(next_part)), 'utf-8'))
        print(f"sent: {int(next_part)}")
        recv = ser.readline()
        print(recv)

def main():
    try:
        main_loop()
    finally:
        ser.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
