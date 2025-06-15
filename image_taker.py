import os
import pathlib
import sys
import time

import cv2
from src.camera_capture_linuxpy import CameraCaptureLinuxpy

sys.modules["pathlib._local"] = pathlib
if os.name == "nt":
    pathlib.PosixPath = pathlib.WindowsPath
else:
    pathlib.WindowsPath = pathlib.PosixPath

if __name__ == "__main__":
    cam_id = 0  # カメラ番号を指定
    camera = CameraCaptureLinuxpy(cam_id)
    frame_limit = 120
    for i in range(frame_limit):
        img = camera.get_image()
        if img is None:
            print(f"No image data found, skipping frame {i + 1}.")
            continue
        print(f"Frame {i + 1}: shape={img.shape}")
        cv2.imshow("Camera", img)
        if cv2.waitKey(1) == 27:  # ESCで中断可
            break
        time.sleep(0.1)
    cv2.destroyAllWindows()
