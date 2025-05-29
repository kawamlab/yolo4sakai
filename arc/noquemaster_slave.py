import time
import cv2
import numpy as np
import serial
import torch

# serial setting

ser = serial.Serial('/dev/ttyACM_arduino_mega2560', 9600)  # ここのポート番号を変更
time.sleep(2)
object_array = []
in_the_box = 2
next_part = 2

# Camera Setting
mtx = np.array([[472.08453552,   1,         280.64475909], [0,         474.26711916, 274.83454714], [0,           0,           1]])
dist = np.array([-0.35203611,  0.19904214,  0.00167646, -0.00205872, -0.07122155])
w = 640
h = 480


newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
newcameramtx = np.array(newcameramtx)


def getModel():
    model = torch.hub.load("../yolov5", 'custom',path="/home/kamata/Program/yolov5/models/BKweights150.pt", source='local')
    return model


def getResult(img, model):
    result = model(img, size=640)

    return result

def yolo(model):
    model.conf = 0.8  # --- 検出の下限値（<1）。設定しなければすべて検出
    objects = [0]
    camera = cv2.VideoCapture(2)
    camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    camera.set(cv2.CAP_PROP_EXPOSURE, 750)

    while True:
        ret, imgs = camera.read()
        
# 読込画像をundistort
        dst = cv2.undistort(imgs, mtx, dist, None, newcameramtx)
        dst = dst[80:410, 35:480]
        dst = cv2.resize(dst, (640, 480))
        result = getResult(dst, model)
        result.render()  # レンダリング
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        objects = result.pandas().xyxy[0]
        if len(objects) == 0:
            #print("No object by YOLO")
            #time.sleep(0.01)
            continue
        else:
            #print("Object detected")
            break

    objects_s = objects.sort_values(by='xmin')
    reverse_object = objects_s.iloc[0, 5]
    if reverse_object == 2:
        print("BKF")
    elif reverse_object == 3:
        print("BKB")
    print(reverse_object)
    print("destroy done")
    objects = [0]
    result = 0
    return reverse_object

model = getModel()  # モデルを呼び出す

while True:

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    ser.write(b's')
    time.sleep(0.5)
    val_arduino = ser.readline()
    #print("sensor value: " + val_arduino.decode('utf-8'))
    val_disp = val_arduino.strip().decode('utf-8')
    if not val_disp.isdecimal():
        continue
    val_disp = int(val_disp)
    #print(val_disp)
    if val_disp == 1:
        time.sleep(0.1)
        if in_the_box == 2:
            ser.write(b'd')
            ser.readline()
            next_part = yolo(model)
            ser.write(b'l')
            ser.readline()
            ser.write(b'u')
            ser.readline()
            in_the_box = next_part
            print("left")
            #complete_message = ser.readline()
            print("in_the_box: BKF, next_part: "+ str(next_part))
            continue
        elif in_the_box  == 3:
            ser.write(b'd')
            ser.readline()
            next_part = yolo(model)
            ser.write(b'r')
            ser.readline()
            ser.write(b'u')
            ser.readline()
            in_the_box = next_part
            """
            # ser.write(b'r')
            # ser.readline()
            # #time.sleep(0.2)
            # #next_part = 0
            # next_part = yolo(model)
            # time.sleep(0.5)
            # in_the_box = next_part
            # print("right")
            # complete_message = ser.readline()
            """
            print("in_the_box: BKB, next_part: " + str(next_part))
            continue
        time.sleep(0.1)

    elif val_disp == 0:
        #print("No Object by sensor")
        continue

ser.close()
# camera.release()
cv2.destroyAllWindows()
