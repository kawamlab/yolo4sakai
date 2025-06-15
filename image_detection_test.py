import io
import os
import pathlib
import sys
import time

import cv2
from src.yolo_detector import YoloDetector, YoloModel
from src.camera_capture_linuxpy import CameraCaptureLinuxpy

sys.modules["pathlib._local"] = pathlib
if os.name == "nt":
    pathlib.PosixPath = pathlib.WindowsPath
else:
    pathlib.WindowsPath = pathlib.PosixPath

if __name__ == "__main__":
    root = pathlib.Path(__file__).resolve(strict=True).parent

    # YOLO Detectorの初期化
    detector = YoloDetector(model_type=YoloModel.BLUE_NEW, conf=0.55, iou=0.45)

    frame_limit = 10
    end_count = 0
    cam_id = 2  # カメラ番号を指定
    camera = CameraCaptureLinuxpy(cam_id)

    while end_count < frame_limit:
        img = camera.get_image()
        if img is None:
            print("No image data found, skipping frame.")
            end_count += 1
            continue

        print(f"取得した画像の形状: {img.shape}")

        # YOLO推論
        results = detector.detect_on_image(img, show=True)

        print(f"検出された物体の個数: {len(results)}")
        for det in results:
            print(
                f"物体 {det.index}: クラス {det.label}, 信頼度 {det.confidence:.2f}, "
                f"座標 ({det.x1:.0f}, {det.y1:.0f}) - ({det.x2:.0f}, {det.y2:.0f})"
            )
        end_count += 1
