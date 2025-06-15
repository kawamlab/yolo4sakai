import os
import pathlib
import sys
import time
import cv2
from datetime import datetime
from src.camera_capture_linuxpy import CameraCaptureLinuxpy

sys.modules["pathlib._local"] = pathlib
if os.name == "nt":
    pathlib.PosixPath = pathlib.WindowsPath
else:
    pathlib.WindowsPath = pathlib.PosixPath

if __name__ == "__main__":
    cam_id = 0  # カメラ番号を指定
    camera = CameraCaptureLinuxpy(cam_id)
    frame_limit = 30
    # 開始時に名前を入力
    name = input("保存する画像のベース名を入力してください: ").strip()
    if not name:
        name = "capture"
    # 保存先ディレクトリ作成（samples/auto_capture_YYYYMMDD_HHMMSS）
    root = pathlib.Path(__file__).resolve(strict=True).parent
    save_dir = root / "samples" / f"auto_capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    save_dir.mkdir(parents=True, exist_ok=True)
    print(f"保存先: {save_dir}")
    for i in range(frame_limit):
        img = camera.get_image()
        if img is None:
            print(f"No image data found, skipping frame {i + 1}.")
            continue
        filename = save_dir / f"{name}_{i + 1:04d}.jpg"
        cv2.imwrite(str(filename), img)
        print(f"Saved: {filename}")
        cv2.imshow("Camera", img)
        if cv2.waitKey(1) == 27:  # ESCで中断可
            break
        time.sleep(0.1)
    cv2.destroyAllWindows()
